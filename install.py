import json
import os
import pickle
import time

try:
    import loguru
    logger = loguru.logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

import helper.screen_configuration
import helper.patch_configurations


def install_folders(folders_paths, name=None):
    logger.info(f"Installing {name if name is not None else 'folders'}...")
    for source_folder_path in folders_paths:
        install_folder(source_folder_path, folders_paths[source_folder_path], name)


def install_files(files_paths, name=None):
    logger.info(f"Installing {name if name is not None else 'files'}...")
    for source_file_path in files_paths:
        install_file(source_file_path, files_paths[source_file_path], name) 


def install_file(source_path, destination_path, name=None):
    source_path = os.path.expanduser(source_path)
    destination_path = os.path.expanduser(destination_path)
    # check if file exists
    if os.path.exists(destination_path) or os.path.islink(destination_path):
        logger.info(f"File {destination_path} already exists.")
        # check if it is a symlink
        if os.path.islink(destination_path):
            logger.info(f"File {destination_path} is already linked.")
            os.unlink(destination_path)
            os.symlink(source_path, destination_path)
        else:
            logger.info(f"Backing up existing file {destination_path}.")
            timestamp = int(time.time())
            os.rename(
                destination_path,
                f"{destination_path}.{timestamp}.bak",
            )
            logger.info(
                f"Backed up existing file to {destination_path}.{timestamp}.bak."
            )
            logger.info(f"Linking {source_path} to {destination_path}.")
            os.symlink(source_path, destination_path)
    else:
        # check if parent folder exists
        parent_destination_folder = os.path.dirname(destination_path)
        if not os.path.exists(parent_destination_folder):
            logger.info(f"Creating parent folder {parent_destination_folder}.")
            os.makedirs(parent_destination_folder, exist_ok=True)
        logger.info(f"Linking {source_path} to {destination_path}.")
        os.symlink(source_path, destination_path)
    if name is not None:
        logger.info(f"Installed {name} configuration.")


def install_folder(source_path, destination_path, name=None):
    source_path = os.path.expanduser(source_path)
    destination_path = os.path.expanduser(destination_path)
    # check if folder exists
    if os.path.exists(destination_path):
        logger.info(f"Folder {destination_path} already exists.")
        # check if it is a symlink
        if os.path.islink(destination_path):
            logger.info(f"Folder {destination_path} is already linked.")
            os.unlink(destination_path)
            os.symlink(source_path, destination_path, target_is_directory=True)
        else:
            logger.info(f"Backing up existing folder {destination_path}.")
            timestamp = int(time.time())
            os.rename(
                destination_path,
                f"{destination_path}.{timestamp}.bak",
            )
            logger.info(
                f"Backed up existing folder to {destination_path}.{timestamp}.bak."
            )
            logger.info(f"Linking {source_path} to {destination_path}.")
            os.symlink(source_path, destination_path, target_is_directory=True)
    else:
        # check if parent folder exists
        parent_destination_folder = os.path.dirname(destination_path)
        if not os.path.exists(parent_destination_folder):
            logger.info(f"Creating parent folder {parent_destination_folder}.")
            os.makedirs(parent_destination_folder, exist_ok=True)
        logger.info(f"Linking {source_path} to {destination_path}.")
        os.symlink(source_path, destination_path, target_is_directory=True)
    if name is not None:
        logger.info(f"Installed {name} configuration.")


def install_credentials(credentials, destination_path=os.path.join("~", ".config", "credentials.json")):
    secrets = {}
    logger.info("Installing credentials...")
    for credential in credentials:
        secret = input(f"Enter the value for {credential}: ")
        secrets[credential] = secret
    destination_path = os.path.expanduser(destination_path)
    if os.path.exists(destination_path):
        logger.info(f"Credentials file {destination_path} already exists.")
        timestamp = int(time.time())
        os.rename(
            destination_path,
            f"{destination_path}.{timestamp}.bak",
        )
        # change file permissions of the backup file to read only for the user
        os.chmod(f"{destination_path}.{timestamp}.bak", 0o600)
        logger.info(
            f"Backed up existing credentials file to {destination_path}.{timestamp}.bak."
        )
    json.dump(
        secrets,
        open(destination_path, "w"),
        indent=4,
    )
    logger.info(f"Installed credentials to {destination_path}.")
    # change file permissions to read only for the user
    os.chmod(destination_path, 0o600)


if __name__ == "__main__":
    repository_folder_path = os.environ.get("NUUNAMNIR_REPOSITORY_PATH", os.path.join("~", "repositories", "nuunamnir.dot-files"))
    repository_folder_path = os.path.expanduser(repository_folder_path)
    configuration_folder_path = os.path.join(repository_folder_path, "configuration")
    assets_folder_path = os.path.join(repository_folder_path, "assets")
    # install bash configuration
    source_file_path = os.path.join(configuration_folder_path, "bash", ".bashrc")
    destination_file_path = os.path.join(os.path.expanduser("~"), ".bashrc")
    install_file(source_file_path, destination_file_path, "bash")

    # install xorg configuration
    files_paths = {
        os.path.join(configuration_folder_path, "xorg", ".xinitrc"): os.path.join(
            os.path.expanduser("~"), ".xinitrc"
        ),
        os.path.join(configuration_folder_path, "xorg", ".Xresources"): os.path.join(
            os.path.expanduser("~"), ".Xresources"
        ),
    }
    install_files(files_paths, "xorg")

    # install vim configuration
    source_file_path = os.path.join(configuration_folder_path, "vim", ".vimrc")
    destination_file_path = os.path.join(os.path.expanduser("~"), ".vimrc")
    install_file(source_file_path, destination_file_path, "vim")

    # install starship configuration
    source_file_path = os.path.join(
        configuration_folder_path, "starship", "starship.toml"
    )
    destination_file_path = os.path.join(os.path.expanduser("~"), ".config", "starship.toml")
    install_file(source_file_path, destination_file_path, "starship")

    # install qtile configuration
    source_folder_path = os.path.join(configuration_folder_path, "qtile")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "qtile")
    install_folder(source_folder_path, destination_folder_path, "qtile")

    # install tmux configuration
    source_folder_path = os.path.join(configuration_folder_path, "tmux")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "tmux")
    install_folder(source_folder_path, destination_folder_path, "tmux")

    # install kitty configuration
    source_folder_path = os.path.join(configuration_folder_path, "kitty")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "kitty")
    install_folder(source_folder_path, destination_folder_path, "kitty")

    # install dunst configuration
    source_folder_path = os.path.join(configuration_folder_path, "dunst")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "dunst")
    install_folder(source_folder_path, destination_folder_path, "dunst")
    
    # install rofi configuration
    source_folder_path = os.path.join(configuration_folder_path, "rofi")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "rofi")
    install_folder(source_folder_path, destination_folder_path, "rofi")

    # install qutebrowser configuration
    source_file_path = os.path.join(configuration_folder_path, "qutebrowser", "config.py")
    destination_file_path = os.path.join(os.path.expanduser("~"), ".config", "qutebrowser", "config.py")
    install_file(source_file_path, destination_file_path, "qutebrowser")


    # install credentials
    # check if user wants to install credentials
    user_input = input("Do you want to install credentials? (y/n): ")
    if user_input.lower() == "y":
        credentials = ["IPINFO_TOKEN"]
        install_credentials(credentials)


    # install configuration
    source_file_path = os.path.join(assets_folder_path, "theme.pkl")
    destination_file_path = os.path.join(os.path.expanduser("~"), ".config", "theme.pkl")
    install_file(source_file_path, destination_file_path, "theme")

    configuration = json.load(open(os.path.join(assets_folder_path, "nuunamnir.json"), "r"))

    monitors = helper.screen_configuration.get()
    configuration["monitors"] = monitors

    colors = pickle.load(open(os.path.expanduser(os.path.join("~", ".config", "theme.pkl")), "rb"))
    configuration["colors"] = colors

    configuration["wallpapers"] = dict()
    configuration["wallpapers"]["dark"] = "~/.config/qtile/wallpaper-dark-4k.png"
    configuration["wallpapers"]["light"] = "~/.config/qtile/wallpaper-light-4k.png"
    configuration["wallpapers"]["dark-urgent"] = (
        "~/.config/qtile/wallpaper-dark-urgent-4k.png"
    )
    configuration["wallpapers"]["light-urgent"] = (
        "~/.config/qtile/wallpaper-light-urgent-4k.png"
    )

    configuration["font"] = dict()
    configuration["font"]["size"] = 14
    configuration["font"]["family"] = "Iosevka Nerd Font"

    configuration["state"] = dict()
    configuration["state"]["theme"] = "light"
    configuration["state"]["urgency"] = "normal"
    configuration["state"]["mode"] = "automatic"

    # if configuration file already exists, back it up
    global_configuration_path = os.path.expanduser(os.path.join("~", ".config", "nuunamnir.json"))
    if os.path.exists(global_configuration_path):
        logger.info(f"Global configuration already exists at {global_configuration_path}.")
        # Backing up the existing configuration
        timestamp = int(time.time())
        os.rename(
            global_configuration_path,
            f"{global_configuration_path}.{timestamp}.bak",
        )
        logger.info(
            f"Backed up existing global configuration to {global_configuration_path}.{timestamp}.bak."
        )
    json.dump(
        configuration,
        open(global_configuration_path, "w"),
        indent=4,
    )
    logger.info(f"Installed global configuration to {global_configuration_path}.")
