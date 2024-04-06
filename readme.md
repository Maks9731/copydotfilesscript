# Dotfiles Management Script

## Overview

This script is designed for managing and backing up your dotfiles to a new directory, initializing a git repository for version control, and using GNU Stow for managing symbolic links. Dotfiles are configuration files in Unix-based systems, usually prefixed with a dot (.), and they configure the behavior of your environment and applications. This script simplifies the process of backing up, copying, and restoring these files, ensuring your environment can be replicated or restored easily.

## Features

- **Backup and Copy**: Copies dotfiles from your specified source directory to a new directory named `dotfiles`, while renaming the original files with a `.bak` extension for backup purposes.
- **Size Check**: Skips copying files or directories larger than a specified size (default is 9GB) to manage space efficiently.
- **Version Control**: Initializes a git repository in the `dotfiles` directory, allowing for easy versioning and management of your dotfiles.
- **Symbolic Link Management**: Uses GNU Stow to create symbolic links from the `dotfiles` directory back to your home directory, making the restoration or deployment of your environment straightforward.
- **Reversion**: Provides an option to delete symbolic links and restore original files from their `.bak` versions, in case of any issues.

## Prerequisites

- **Python 3**: This script is written in Python and requires Python 3 to run.
- **Git**: Git must be installed on your system for version control features.
- **GNU Stow**: GNU Stow is used for managing symbolic links and must be installed.
- **Sudo Privileges**: Depending on your dotfiles' permissions, you might need sudo privileges to copy and symlink dotfiles that require root access.

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
## Knows issues: 
If you have a file with the same name in the source directory and the destination directory, the script will not create a symlink for that file. Usually this is not an issue unless you have a programm like atuin which creates a new file with the same name as the original file while the script is running. That way the script can't create a symlink for the new file because there is already a file with the same name in the source directory.

You can fix this by disabling programms like atuin which are running in the background and constantly creating new files with the same name as the original files temporarily while the script is running.


## Conclusion

This script is a powerful tool for managing your Unix environment's dotfiles, making backup, restoration, and version control streamlined and efficient. By following the detailed instructions and ensuring all prerequisites are met, you can easily manage your configuration files with confidence.
