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

from helper.utils import (
    install_file,
    install_folder,
    install_files,
    install_credentials,
)


if __name__ == "__main__":
    repository_folder_path = os.environ.get(
        "NUUNAMNIR_REPOSITORY_PATH",
        os.path.join("~", "repositories", "nuunamnir.dot-files"),
    )
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
    source_folder_path = os.path.join(configuration_folder_path, "icc")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "icc")
    install_folder(source_folder_path, destination_folder_path, "icc")

    # install vim configuration
    source_file_path = os.path.join(configuration_folder_path, "vim", ".vimrc")
    destination_file_path = os.path.join(os.path.expanduser("~"), ".vimrc")
    install_file(source_file_path, destination_file_path, "vim")

    # install starship configuration
    source_file_path = os.path.join(
        configuration_folder_path, "starship", "starship.toml"
    )
    destination_file_path = os.path.join(
        os.path.expanduser("~"), ".config", "starship.toml"
    )
    install_file(source_file_path, destination_file_path, "starship")

    # install qtile configuration
    source_folder_path = os.path.join(configuration_folder_path, "qtile")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "qtile")
    install_folder(source_folder_path, destination_folder_path, "qtile")

    # install picom configuration
    source_folder_path = os.path.join(configuration_folder_path, "picom")
    destination_folder_path = os.path.join(os.path.expanduser("~"), ".config", "picom")
    install_folder(source_folder_path, destination_folder_path, "picom")

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
    source_file_path = os.path.join(
        configuration_folder_path, "qutebrowser", "config.py"
    )
    destination_file_path = os.path.join(
        os.path.expanduser("~"), ".config", "qutebrowser", "config.py"
    )
    install_file(source_file_path, destination_file_path, "qutebrowser")

    # install Visual Studio Code configuration
    source_folder_path = os.path.join(configuration_folder_path, "vscode")
    destination_folder_path = os.path.join(
        os.path.expanduser("~"), ".config", "Code", "User"
    )
    install_file(
        os.path.join(source_folder_path, "settings.json"),
        os.path.join(destination_folder_path, "settings.json"),
        "Visual Studio Code settings",
    )

    # install credentials
    # check if user wants to install credentials
    user_input = input("Do you want to install credentials? (y/n): ")
    if user_input.lower() == "y":
        credentials = ["IPINFO_TOKEN"]
        install_credentials(credentials)

    # install configuration
    source_file_path = os.path.join(assets_folder_path, "theme.pkl")
    destination_file_path = os.path.join(
        os.path.expanduser("~"), ".config", "theme.pkl"
    )
    install_file(source_file_path, destination_file_path, "theme")

    configuration = json.load(
        open(os.path.join(assets_folder_path, "nuunamnir.json"), "r")
    )

    monitors = helper.screen_configuration.get()
    configuration["monitors"] = monitors

    colors = pickle.load(
        open(os.path.expanduser(os.path.join("~", ".config", "theme.pkl")), "rb")
    )
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
    global_configuration_path = os.path.expanduser(
        os.path.join("~", ".config", "nuunamnir.json")
    )
    if os.path.exists(global_configuration_path):
        logger.info(
            f"Global configuration already exists at {global_configuration_path}."
        )
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
