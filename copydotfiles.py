import os
import shutil
import subprocess
from pathlib import Path


def get_size(start_path):
    total_size = 0
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp) and os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
    return total_size


def get_size_in_gb(size_in_bytes):
    return size_in_bytes / (1024 * 1024 * 1024)


def copy_if_under_9gb(source, destination, copied_items, max_size_gb):
    size_bytes = get_size(source)
    size_gb = get_size_in_gb(size_bytes)
    if size_gb <= max_size_gb:
        try:
            dest_path = os.path.join(destination, os.path.basename(source))
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


def rename_copied_items(copied_items):
    for item in copied_items:
        try:
            os.rename(item, f"{item}.bak")
            print(f"Renamed {item} to {item}.bak")
        except Exception as e:
            print(f"Error renaming {item}. Reason: {str(e)}")


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


def delete_symlinks_and_restore_bak_files(source_dir):
    """
    Delete symbolic links and restore .bak files to their original state in the given directory.
    """
    for item in source_dir.iterdir():
        if item.is_symlink():
            # Delete the symlink
            item.unlink()
            print(f"Deleted symlink: {item}")
        elif item.name.endswith(".bak"):
            # Construct the original file/directory name by removing '.bak'
            original_name = str(item)[:-4]
            # Rename the .bak file/directory back to its original name
            item.rename(original_name)
            print(f"Restored {item} to {original_name}")


def main():
    print(
        "READ: This script will copy all dotfiles from your source directory to a new directory named 'dotfiles' in the same directory."
    )
    print(
        "It will also rename the original copied dotfiles to have a '.bak' extension."
    )
    print(
        "After copying, it will initialize a new git repository in the 'dotfiles' directory and run 'stow .' to symlink the dotfiles."
    )
    print(
        "Please make sure to have a backup of your dotfiles before running this script."
    )
    print("If you have already made a backup, please type 'y' when prompted.")
    print(
        "You may need to run this script in sudo priviliges to copy and symlink dotfiles which require root access. (highly recommended to run in sudo)"
    )
    print("You must have git and stow (gnu stow) installed on your system.")

    sourcedir = Path(
        input("Enter the source directory [default: /Users/berserk]: ")
        or "/Users/berserk"
    )  # Change this to your actual home directory or any other directory containing your dotfiles
    dest_dir = sourcedir / "dotfiles"

    backup_prompt = (
        input("Did you make a Backup? (highly recommended) (y/N): ").lower().strip()
    )
    if backup_prompt == "n":
        print("Backup chosen. Exiting program")
        return
    else:
        destination = Path(sourcedir) / "dotfiles"
        # Check if the source directory exists and is a directory
        if not os.path.exists(sourcedir) or not os.path.isdir(sourcedir):
            print(f"Error: {sourcedir} doesn't exist or isn't a directory.")
            return

        # Check if the destination already exists and ask for confirmation to overwrite
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
    max_size_gb = (
        input("Enter the maximum size of a file/directory to copy in GB [default: 9]: ")
        or 9
    )
    for item in sourcedir.iterdir():
        if item.name.startswith(".") and item.name not in [".", ".."]:
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
