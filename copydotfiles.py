import os
import shutil
import subprocess
from pathlib import Path


# Calculate the total size of files within a directory
def get_size(start_path):
    total_size = 0
    # Check if the start path is a file and get its size
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        # Traverse the directory tree
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Sum the sizes of non-symlink files
                if not os.path.islink(fp) and os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
    return total_size


# Convert size from bytes to gigabytes
def get_size_in_gb(size_in_bytes):
    return size_in_bytes / (1024 * 1024 * 1024)


# Copy source to destination if its size is under 9GB
def copy_if_under_9gb(source, destination, copied_items, max_size_gb):
    size_bytes = get_size(source)
    size_gb = get_size_in_gb(size_bytes)
    # Check if the size is within the limit
    if size_gb <= max_size_gb:
        try:
            dest_path = os.path.join(destination, os.path.basename(source))
            # Copy directory trees or individual files accordingly
            if os.path.isdir(source):
                shutil.copytree(
                    source,
                    dest_path,
                    symlinks=True,
                    ignore=shutil.ignore_patterns("*.sock", "*.socket"),
                )
            elif os.path.isfile(source):
                shutil.copy2(source, dest_path)
            print(f"Copied {source} to {destination}")
            copied_items.append(source)
        except Exception as e:
            print(f"Error copying {source}. Reason: {str(e)}")
    else:
        print(f"Skipped {source} because it's larger than 9GB")


# Rename copied items to have a .bak extension
def rename_copied_items(copied_items):
    for item in copied_items:
        try:
            os.rename(item, f"{item}.bak")
            print(f"Renamed {item} to {item}.bak")
        except Exception as e:
            print(f"Error renaming {item}. Reason: {str(e)}")


# Check if GNU Stow is installed
def is_stow_installed():
    try:
        subprocess.run(
            ["stow", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except Exception:
        return False


# Initialize a git repository and optionally run stow
def initialize_git_and_stow(dest_dir):
    git_init_success = False
    stow_success = False
    try:
        subprocess.run(["git", "init"], cwd=str(dest_dir), check=True)
        print(f"Initialized a new git repository in {dest_dir}")
        git_init_success = True
    except subprocess.CalledProcessError as e:
        print(f"Error during git initialization. {e}")

    if git_init_success and is_stow_installed():
        try:
            subprocess.run(["stow", "."], cwd=str(dest_dir), check=True)
            print("Executed 'stow .' successfully.")
            stow_success = True
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'stow .'. {e}")

    return git_init_success and (not is_stow_installed() or stow_success)


# Delete symlinks and restore .bak files
def delete_symlinks_and_restore_bak_files(source_dir):
    """
    Delete symbolic links and restore .bak files to their original state in the given directory.
    """
    for item in source_dir.iterdir():
        if item.is_symlink():
            item.unlink()  # Delete the symlink
            print(f"Deleted symlink: {item}")
        elif item.name.endswith(".bak"):
            original_name = str(item)[:-4]  # Remove '.bak' extension
            item.rename(original_name)  # Restore to original name
            print(f"Restored {item} to {original_name}")


# Main function to orchestrate the script's operations
def main():
    print("Introduction and instructions for the script")
    sourcedir = Path(
        input("Enter the source directory [default: /Users/berserk]: ")
        or "/Users/berserk"
    )
    dest_dir = sourcedir / "dotfiles"

    # Prompt for backup confirmation
    backup_prompt = (
        input("Did you make a Backup? (highly recommended) (y/N): ").lower().strip()
    )
    if backup_prompt == "n":
        print("Backup chosen. Exiting program")
        return
    else:
        destination = Path(sourcedir) / "dotfiles"
        if not os.path.exists(sourcedir) or not os.path.isdir(sourcedir):
            print(f"Error: {sourcedir} doesn't exist or isn't a directory.")
            return

        # Overwrite confirmation if destination exists
        if destination.exists():
            overwrite = (
                input(f"The directory {destination} already exists. Overwrite? (y/N): ")
                .lower()
                .strip()
            )
            if overwrite != "y":
                print("Operation cancelled by the user.")
                return

    copied_items = []
    max_size_gb = (  # Set the default maximum size of a file/directory to copy
        input("Enter the maximum size of a file/directory to copy in GB [default: 9]: ")
        or 9
    )
    for item in sourcedir.iterdir():
        if item.name.startswith("."):  # Copy dotfiles
            copy_if_under_9gb(item, dest_dir, copied_items, max_size_gb)

    rename_copied_items(copied_items)
    if initialize_git_and_stow(dest_dir):
        print("success")
    else:
        try:
            print("Reverting due to previous errors.")
            delete_symlinks_and_restore_bak_files(sourcedir)
        except Exception as e:
            print("Reverting failed.")


# Choose action based on user input
action = input(
    "Enter action which should be performed (copydotfiles/revertcopydotfiles)"
)
if action == "copydotfiles":
    main()
elif action == "revertcopydotfiles":
    sourcedir = Path(
        input("Enter the source directory [default: /Users/berserk]: ")
        or "/Users/berserk"
    )
    delete_symlinks_and_restore_bak_files(sourcedir)
    if (
        input("Do you want to delete the dotfiles directory? (y/N): ").lower().strip()
        == "y"
    ):
        shutil.rmtree(sourcedir / "dotfiles")
else:
    print("Invalid action")
