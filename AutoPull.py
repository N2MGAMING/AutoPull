from os import listdir, chdir
from os.path import isdir
from subprocess import run

config_src = "/etc/AutoPull.conf"
default_config = "#This file should be modified with caution, misconfiguration can result in complete disfunction of the program\n#The src value should point to the folder containing all the GitHub repositories that the user wishes to Auto-Update\n\n[Settings]\n\nsrc = {}\nVerboseGit = on\nDebugging = off"

FileNotFoundErrorMessage = "\n--------------------------------------------\nAutoPull.conf doesn't exist ! Recreating a default configuration file at {}".format(config_src)
WritePermisionMessage = "Couldn't write the config file to {} ! You don't have write permission, switch to root ".format(config_src)
FileCreationMessage = "Config file successfully created !\nRestart AutoPull !"
NotDirectoryWarningMessage = "Warning : {} isn't a directory, it will be skipped !"
InputMessage = "Please enter the path of the folder containing the GitHub repositories : "

try:
    with open(config_src, 'r') as config : # Opening Config.txt to get the settings
        Lines = config.readlines()
except FileNotFoundError: # Recreating Config file if it doesn't exist
    print(FileNotFoundErrorMessage)
    try:
        with open(config_src, 'x+') as config:
            src = input(InputMessage)
            while isdir(src)==False:
                print("Invalid Path !!!")
                input(InputMessage)
            if src[-1]!="/":
                src = src + "/"
            config.write(default_config.format(src))
    except Exception: # Problem in the creation (Write Permission)
        print(WritePermisionMessage)
        quit()
    else:
        print(FileCreationMessage)
        quit()
else:
    src = Lines[5].replace("src = ", "").replace("\n", "").replace("'", "")
    verbose = bool(Lines[6].replace("VerboseGit = ", "").replace("\n", "").replace("on", "1").replace("off", "0")=="1") # Look if the VerboseGit value was On or Off
    debugging = bool(Lines[7].replace("Debugging = ", "").replace("on", "1").replace("off", "0")=="1") # Look if the debugging value was On or Off
    if debugging:
        print("src = {}\nVerboseGit = {}\nDebugging = {}\n".format(src, verbose, debugging)) # For debugging purpose 

BuildsFolder = listdir(src)
repos = []

if debugging:
    print(BuildsFolder) # For debugging purpose
for name in BuildsFolder:
    path = src+name
    if debugging:
        print(path) # For debugging purpose
    IsDir = isdir(path)
    if IsDir:
        repos.append(path+"/")
    else:
        print(NotDirectoryWarningMessage.format(path))
if debugging:
    print(repos) # For debugging purpose

for repo in repos :
    repo_name = repo.replace(src, "").replace("/", "")
    print("\n--------------------------------------\nUpdating {} : ".format(repo_name))
    chdir(repo)
    if verbose:
        run(["git", "pull", "--verbose"])
    else:
        run(["git", "pull"])
