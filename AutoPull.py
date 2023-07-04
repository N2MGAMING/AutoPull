from os import listdir, chdir
from os.path import isdir
from subprocess import run

ConfigFolder = "/etc/AutoPull/"
allowed_src = "/etc/AutoPull/AllowedRepos" 
config_src = "/etc/AutoPull/AutoPull.conf"
default_config = "#This file should be modified with caution, misconfiguration can result in complete disfunction of the program\n#The src value should point to the folder containing all the GitHub repositories that the user wishes to Auto-Update\n\n[Settings]\n\nsrc = {}\nVerboseGit = on\nDebugging = off"

FileNotFoundErrorMessage = "\n--------------------------------------------\n{} doesn't exist ! Recreating a default file at {}"
WritePermisionMessage = "Couldn't write the {} ! You don't have write permission, switch to root "
FileCreationMessage = "{} successfully created !\nRestart AutoPull !"
NotDirectoryWarningMessage = "Warning : {} isn't a directory, it will be skipped !"
InputMessage = "Please enter the path of the folder containing the GitHub repositories : "
NewFolderDetection = "AutoPull detected a new Git repository in {}"

# Recreating the Configuration Folder if it doesn't exist
if isdir(ConfigFolder)==False:
    try:
        run(["mkdir", ConfigFolder])
    except Exception as e: # Problem in the creation (Write Permission)
        print(WritePermisionMessage.format("config folder to " + ConfigFolder))
        print(e)
        quit()
    else:
        print(FileCreationMessage.format("config folder").replace("\nRestart AutoPull !", ""))

# Retrieving Configuration From AutoPull.conf
try:
    with open(config_src, 'r') as config : # Opening AutoPull.conf to get the settings
        Lines = config.readlines()
except FileNotFoundError: # Recreating Config file if it doesn't exist
    print(FileNotFoundErrorMessage.format("AutoPull.conf", config_src))
    try:
        with open(config_src, 'x+') as config:
            src = input(InputMessage)
            while isdir(src)==False:
                print("Invalid Path !!!")
                input(InputMessage)
            if src[-1]!="/":
                src = src + "/"
            config.write(default_config.format(src))
    except Exception as e: # Problem in the creation (Write Permission)
        print(WritePermisionMessage.format("config file to " + config_src))
        print(e)
        quit()
    else:
        print(FileCreationMessage.format("AutoPull.conf"))
        quit()
else:
    src = Lines[5].replace("src = ", "").replace("\n", "").replace("'", "")
    verbose = bool(Lines[6].replace("VerboseGit = ", "").replace("\n", "").replace("on", "1").replace("off", "0")=="1") # Look if the VerboseGit value was On or Off
    debugging = bool(Lines[7].replace("Debugging = ", "").replace("on", "1").replace("off", "0")=="1") # Look if the debugging value was On or Off
    if debugging:
        print("src = {}\nVerboseGit = {}\nDebugging = {}\n".format(src, verbose, debugging)) # For debugging purpose 

# Verifying Directories Validity And Preparing Repos List
BuildsFolder = listdir(src)
repos = []
allowed_repos = []
not_allowed_repos = []

if debugging:
    print(BuildsFolder) # For debugging purpose
for name in BuildsFolder:
    path = src+name
    if debugging:
        print(path) # For debugging purpose
    IsDir = isdir(path)
    if IsDir:
        repos.append(path)
    else:
        print(NotDirectoryWarningMessage.format(path))
if debugging:
    print(repos) # For debugging purpose

try:
    with open(allowed_src, 'r') as AllowedRepos : # Opening AllowedRepos to get the specific GitHub repositories to update
        AllowedReposLines = AllowedRepos.readlines()
except FileNotFoundError: # Recreating AllowedRepos file if it doesn't exist
    print(FileNotFoundErrorMessage.format("AllowedRepos", allowed_src))
    try:
        with open(allowed_src, 'x+') as AllowedRepos:
            for repo in repos:
                Value = input("Allow updating " + repo + " (Y/n) : ")
                if Value.upper()=="Y":
                    AllowedRepos.write(repo + " = Allowed\n")
                else:
                    AllowedRepos.write(repo + " = NotAllowed\n")

    except Exception: # Problem in the creation (Write Permission)
        print(WritePermisionMessage.format("AllowedRepos file to " + allowed_src))
        quit()
    else:
        print(FileCreationMessage.format("AllowedRepos"))
        quit()
else:
    for line in AllowedReposLines: # Check if the repo value is True or False
        repo_boolean_value = line.replace("\n", "").split(" = ")
        if repo_boolean_value[1]=="Allowed":
            allowed_repos.append(repo_boolean_value[0])
        elif repo_boolean_value[1]=="NotAllowed":
            not_allowed_repos.append(repo_boolean_value[0])
    if debugging:
        print(allowed_repos) # For debugging purpose 

# Adding the repositories non present in the src folder to the repos list
for repo in allowed_repos:
    if repo not in repos:
        repos.append(repo)

# Updating The Repos
for repo in repos :
    if src in repo :
        repo_name = repo.replace(src, "").replace("/", "")
    elif src not in repo :    
        repo_name = repo.split("/")[-1]
    if repo in allowed_repos:
        print("\n--------------------------------------\nUpdating {} : ".format(repo_name))
        chdir(repo)
        if verbose:
            run(["git", "pull", "--verbose"])
        else:
            run(["git", "pull"])
    elif repo not in not_allowed_repos:
        print("\n" + NewFolderDetection.format(src))
        add = input("Would you like to allow AutoPull to update {} (Y/n) : ".format(repo_name))
        try:
            with open(allowed_src, "a") as AllowedRepos:
                if add.upper()=="Y":
                    AllowedRepos.write(repo + " = Allowed\n")
                else:
                    AllowedRepos.write(repo + " = NotAllowed\n")
        except PermissionError:
            print(WritePermisionMessage.format("AllowedRepos file to " + allowed_src))
            quit()
        else:
            print("The folder has been successfully configured !")