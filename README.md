# AutoPull

AutoPull is a Python script that manages a configuration file and automates the process of updating multiple GitHub repositories using the `git` command.

## Prerequisites

- Python 3.x
- Git installed and configured

## Getting Started

1. Clone the repository or download the `AutoPull.py` file to your local machine.

2. Configure the `AutoPull.conf` file:
 * Automatic Configuration :
   (You need to run the script as root to create the /etc/AutoPull/AutoPull.conf automatically. If you don't have root access, you can change AutoPull.conf path in the script `config_src` variable.)
   - If the `AutoPull.conf` file doesn't exist, the script will recreate it with default settings.
 * Manual Configuration :
   (You can copy the default configuration presented below.)
   - Create the `AutoPull.conf` at the chosen path (config_src).
   - Open the `AutoPull.conf` file in a text editor.
   - Modify the `src` value to specify the path of the folder containing the GitHub repositories you want to update.
   - Optionally, adjust the `VerboseGit` and `Debugging` settings according to your preferences.

3. First run of the script:

   ```
   python AutoPull.py
   ```

   The script will read the configuration file, retrieve the repository paths and then ask the user for each repository found if they want to allow the Auto-update.

4. Run the script:

   ```
   python AutoPull.py
   ```

   The script will read the configuration file, retrieve the repository paths and the allowed paths in order to compare them and add new folders if they are
   detected, and then, it will update the allowed repositories using the `git pull` command.

5. Review the output:

   - The script will provide updates and status messages for each repository being updated.
   - If the `VerboseGit` setting is enabled, detailed output from the `git pull` command will be displayed.

## Configuration

1. The configuration file (`AutoPull.conf`) is used to specify the settings for AutoPull. Here's an example of the default configuration:

```
#This file should be modified with caution, misconfiguration can result in complete disfunction of the program
#The src value should point to the folder containing all the GitHub repositories that the user wishes to Auto-Update

[Settings]

src = /path/to/repositories/
VerboseGit = on
Debugging = off
```

- `src`: The path of the folder containing the GitHub repositories to update.
- `VerboseGit`: Determines whether to display verbose output from the `git pull` command.
- `Debugging`: Enables or disables debugging mode for additional output and information.

2. `AllowedRepos` file contains all the repositories that AutoPull detected in the src folder specified in `AutoPull.conf`. The user can disable the update of a
specific Git repository by changing the `Allowed` value stated next to the repository's path in this file. As a result, the script will ignore this repository.

N.B : 
- AutoPull will detect new folders and ask the user if they want to allow the Auto-update .
- You can include folders not present in the src folder by adding their path in `AllowedRepos` followed by ` = Allowed`. Don't change the file structure. This can lead to a break of the script, read the Troubleshooting section if this occurs .

## Troubleshooting

- If the `AutoPull.conf` file is missing, and you don't have write permission to recreate it, make sure to switch to the root user or an account with sufficient privileges.
- If any errors occur during the execution of the script, ensure that you have the necessary permissions and that Git is properly installed and configured. If it's the case, then, the problem is due to the configuration of the script. All you have to do is deleting AutoPull.conf and AllowedRepos.

## Limitations

- The script assumes that Git is installed and configured correctly on your system.
- It only supports updating repositories using the `git pull` command.
- The script doesn't handle all possible error scenarios, such as network issues or conflicts during the update process.

## Contributing

Contributions to AutoPull are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

Feel free to modify and customize this README file according to your project's specific requirements and guidelines.
