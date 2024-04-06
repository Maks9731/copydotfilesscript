# Dotfiles Management Script

## Overview
This Python script automates the management of Unix-based system dotfiles, enabling easy backup, version control with Git, and symlink management with GNU Stow. It's designed to copy dotfiles to a new directory, track changes using Git, and use Stow for easy symlink creation, ensuring a manageable and replicable environment setup.

## Features
- **Automatic Backup**: Copies dotfiles to a `dotfiles` directory, renaming originals with `.bak` for safety.
- **Selective Copying**: Only copies files/directories under 9GB by default, to avoid unnecessary space consumption.
- **Version Control Integration**: Initializes a Git repository in the `dotfiles` directory for change tracking.
- **Symlink Management with Stow**: Utilizes GNU Stow for efficient symlink creation, linking dotfiles back to their original locations.
- **Easy Reversion**: Offers an option to delete symlinks and restore files to their original state if needed.

## Prerequisites
- Python 3
- Git and GNU Stow installed
- Sudo privileges may be required for certain operations.

## Usage Instructions
1. **Prepare**: Ensure a backup of your dotfiles exists. Install Git and GNU Stow if not already present.
2. **Run the Script**: Follow the prompts to specify the source directory, confirm backup, and set the maximum file size for copying.
3. **Choose Action**:
   - `copydotfiles`: To backup and manage your dotfiles.
   - `revertcopydotfiles`: To revert changes, restoring original files.

<<<<<<< HEAD
## How to Use

### Preparations

1. **Backup**: Ensure you have a backup of your current dotfiles. This script will modify files and you should be able to restore them if needed.
2. **Install Git and GNU Stow**: Make sure both Git and GNU Stow are installed on your system.

### Running the Script

1. **Start the Script**: Run the script and follow the prompts. It will first ask for the source directory of your dotfiles. The default is `/Users/berserk`, but you should replace this with the path to your actual dotfiles directory.
2. **Backup Confirmation**: Confirm that you have backed up your dotfiles. This is crucial to prevent accidental loss of data.
3. **Specify Size Limit**: You can specify the maximum size (in GB) for the files/directories to be copied. The default is 9GB.
4. **Action Choice**: Choose the action to perform:
   - `copydotfiles`: To backup, copy, and manage your dotfiles.
   - `revertcopydotfiles`: To revert any changes made by the script, restoring original files and removing symlinks.

### Post-Operation

- **Check Output**: The script provides detailed output about the operations performed, including any files copied, renamed, or skipped.
- **Verify Symlinks**: If you ran the `copydotfiles` action, check that the symbolic links are correctly pointing to the new `dotfiles` directory.
- **Git and Stow**: The script initializes a git repository and attempts to use GNU Stow for symlink management. Verify that these operations completed successfully.

## Troubleshooting

- If the script encounters permissions issues, you might need to run it with sudo privileges.
- Check the script's output for any error messages or skipped files due to size constraints.
- If reverting changes, confirm that `.bak` files are correctly restored and symlinks are removed.
=======
## Post-Operation
- Verify that dotfiles are copied, and symlinks are correctly created.
- Ensure the Git repository is initialized in the `dotfiles` directory, and changes are tracked.
- In case of errors, the script outputs detailed messages for troubleshooting.
>>>>>>> 93efe6b50812a9c4b18de5874e81b50ead91b7b8

## Conclusion
This concise script streamlines the dotfiles management process, enhancing the backup, restoration, and version control of your Unix-based system's configuration files.
