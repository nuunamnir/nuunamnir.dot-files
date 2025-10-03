import json
import os
import pickle
import time

import helper.screen_configuration
import helper.patch_configurations


def install_qtile():
    configuration_path = os.path.join(os.getcwd(), "configuration", "qtile")
    print(f"Installing Qtile configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/qtile")
    if os.path.exists(default_path):
        print("Qtile is already installed.")
        if os.path.islink(default_path):
            print("Qtile configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_rofi():
    configuration_path = os.path.join(os.getcwd(), "configuration", "rofi")
    print(f"Installing Rofi configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/rofi")
    if os.path.exists(default_path):
        print("Rofi is already installed.")
        if os.path.islink(default_path):
            print("Rofi configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_dunst():
    configuration_path = os.path.join(os.getcwd(), "configuration", "dunst")
    print(f"Installing Dunst configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/dunst")
    if os.path.exists(default_path):
        print("Dunst is already installed.")
        if os.path.islink(default_path):
            print("Dunst configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_kitty():
    configuration_path = os.path.join(os.getcwd(), "configuration", "kitty")
    print(f"Installing kitty configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/kitty")
    if os.path.exists(default_path):
        print("kitty is already installed.")
        if os.path.islink(default_path):
            print("kitty configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_tmux():
    configuration_path = os.path.join(os.getcwd(), "configuration", "tmux")
    print(f"Installing tmux configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/tmux")
    if os.path.exists(default_path):
        print("tmux is already installed.")
        if os.path.islink(default_path):
            print("tmux configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_starship():
    configuration_path = os.path.join(
        os.getcwd(), "configuration", "starship", "starship.toml"
    )
    print(f"Installing starship configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/starship.toml")
    if os.path.exists(default_path):
        print("starship is already installed.")
        if os.path.islink(default_path):
            print("starship configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_vim():
    configuration_path = os.path.join(os.getcwd(), "configuration", "vim", ".vimrc")
    print(f"Installing vim configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.vimrc")
    if os.path.exists(default_path):
        print("vim is already installed.")
        if os.path.islink(default_path):
            print("vim configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_bash():
    configuration_path = os.path.join(os.getcwd(), "configuration", "bash", ".bashrc")
    print(f"Installing bash configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.bashrc")
    if os.path.exists(default_path):
        print("bash is already installed.")
        if os.path.islink(default_path):
            print("bash configuration is already linked.")
            os.unlink(default_path)
            os.symlink(configuration_path, default_path)
        return
    else:
        os.symlink(configuration_path, default_path)


def install_xorg():
    for file_name in os.listdir(os.path.join(os.getcwd(), "configuration", "xorg")):
        configuration_path = os.path.join(
            os.getcwd(), "configuration", "xorg", file_name
        )
        print(f"Installing xorg configuration from {configuration_path}...")
        default_path = os.path.expanduser(f"~/{file_name}")
        if os.path.exists(default_path):
            print(f"xorg file {file_name} is already installed.")
            if os.path.islink(default_path):
                print(f"xorg file {file_name} configuration is already linked.")
                os.unlink(default_path)
                os.symlink(configuration_path, default_path)
            continue
        else:
            os.symlink(configuration_path, default_path)


def install_qutebrowser():
    configuration_path = os.path.join(os.getcwd(), "configuration", "qutebrowser")
    print(f"Installing qutebrowser configuration from {configuration_path}...")
    default_path = os.path.expanduser("~/.config/qutebrowser")
    os.makedirs(default_path, exist_ok=True)
    if os.path.exists(os.path.join(default_path, "config.py")):
        print("qutebrowser is already installed.")
        if os.path.islink(os.path.join(default_path, "config.py")):
            print("qutebrowser configuration is already linked.")
            os.unlink(os.path.join(default_path, "config.py"))
            os.symlink(os.path.join(configuration_path, "config.py"), os.path.join(default_path, "config.py"))
        else:
            print("Backing up existing qutebrowser configuration.")
            timestamp = int(time.time())
            os.rename(
                os.path.join(default_path, "config.py"),
                os.path.join(default_path, f"config.py.{timestamp}.bak"),
            )
            print(
                f"Backed up existing qutebrowser configuration to {os.path.join(default_path, f'config.py.{timestamp}.bak')}."
            )
            os.symlink(os.path.join(configuration_path, "config.py"), os.path.join(default_path, "config.py"))
    else:
        os.symlink(os.path.join(configuration_path, "config.py"), os.path.join(default_path, "config.py"))


if __name__ == "__main__":
    global_configuration_path = os.path.join("~/.config/nuunamnir.json")
    configuration = {}
    monitors = helper.screen_configuration.get()
    configuration["monitors"] = monitors

    configuration["font"] = dict()
    configuration["font"]["size"] = 14
    configuration["font"]["family"] = "Iosevka Nerd Font"

    if os.path.exists(os.path.expanduser("~/.config/theme.pkl")):
        colors = pickle.load(open(os.path.expanduser("~/.config/theme.pkl"), "rb"))
        configuration["colors"] = colors
    else:
        configuration["colors"] = dict()
        configuration["colors"]["light"] = dict()
        configuration["colors"]["light"]["positive"] = "#5f823f"
        configuration["colors"]["light"]["negative"] = "#ab5c56"
        configuration["colors"]["light"]["neutral"] = "#5e73b3"
        configuration["colors"]["light"]["foreground"] = "#191919"
        configuration["colors"]["light"]["grey"] = "#767676"
        configuration["colors"]["light"]["background"] = "#d2d2d2"
        configuration["colors"]["light"]["cursor"] = "#000000"

        configuration["colors"]["dark"] = dict()
        configuration["colors"]["dark"]["positive"] = "#5f823f"
        configuration["colors"]["dark"]["negative"] = "#ab5c56"
        configuration["colors"]["dark"]["neutral"] = "#5e73b3"
        configuration["colors"]["dark"]["foreground"] = "#c1c1c1"
        configuration["colors"]["dark"]["grey"] = "#767676"
        configuration["colors"]["dark"]["background"] = "#191919"
        configuration["colors"]["dark"]["cursor"] = "#d2d2d2"

    configuration["wallpapers"] = dict()
    configuration["wallpapers"]["dark"] = "~/.config/qtile/wallpaper-dark-4k.png"
    configuration["wallpapers"]["light"] = "~/.config/qtile/wallpaper-light-4k.png"
    configuration["wallpapers"]["dark-urgent"] = (
        "~/.config/qtile/wallpaper-dark-urgent-4k.png"
    )
    configuration["wallpapers"]["light-urgent"] = (
        "~/.config/qtile/wallpaper-light-urgent-4k.png"
    )

    configuration["state"] = dict()
    configuration["state"]["theme"] = "light"
    configuration["state"]["urgency"] = "normal"
    configuration["state"]["mode"] = "automatic"

    if os.path.exists(os.path.expanduser(global_configuration_path)):
        print(f"Global configuration already exists at {global_configuration_path}.")
        # Backing up the existing configuration
        timestamp = int(time.time())
        os.rename(
            os.path.expanduser(global_configuration_path),
            os.path.expanduser(global_configuration_path + f".{timestamp}.bak"),
        )
        print(
            f"Backed up existing global configuration to {global_configuration_path + f'.{timestamp}.bak'}."
        )
    json.dump(
        configuration,
        open(os.path.expanduser(global_configuration_path), "w"),
        indent=4,
    )
    install_qtile()
    install_rofi()
    install_dunst()
    install_kitty()
    install_tmux()
    install_starship()
    install_vim()
    install_bash()
    install_xorg()
    install_qutebrowser()

    helper.patch_configurations.patch_all(configuration)
