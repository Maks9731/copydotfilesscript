# Dotfiles Management Script

## Overview
This Python script automates the management of Unix-based system dotfiles, enabling easy backup, version control with Git, and symlink management with GNU Stow. It's designed to copy dotfiles to a new directory, track changes using Git, and use Stow for easy symlink creation, ensuring a manageable and replicable environment setup.

![](assets/img/scriptimg.png)

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

## Post-Operation
- Verify that dotfiles are copied, and symlinks are correctly created.
- Ensure the Git repository is initialized in the `dotfiles` directory, and changes are tracked.
- In case of errors, the script outputs detailed messages for troubleshooting.

## Knows issues: 
If you have a file with the same name in the source directory and the destination directory, the script will not create a symlink for that file. Usually this is not an issue unless you have a programm like atuin which creates a new file with the same name as the original file while the script is running. That way the script can't create a symlink for the new file because there is already a file with the same name in the source directory.

You can fix this by disabling programms like atuin which are running in the background and constantly creating new files with the same name as the original files temporarily while the script is running.

## Conclusion
This concise script streamlines the dotfiles management process, enhancing the backup, restoration, and version control of your Unix-based system's configuration files.
