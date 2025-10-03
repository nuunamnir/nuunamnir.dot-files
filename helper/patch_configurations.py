import json
import os
import subprocess
import configparser
import time

import toml


def patch_rofi(configuration):
    theme = configuration["state"]["theme"]

    widths = list()
    scaling_factors = list()
    for monitor in configuration["monitors"]:
        widths.append(configuration["monitors"][monitor]["width"])
        scaling_factors.append(configuration["monitors"][monitor]["scaling_factor"])
    average_width = int(round(sum(widths) / len(widths)))
    average_scaling_factor = sum(scaling_factors) / len(scaling_factors)

    patched_configuration = {
        "FONT": f'"{configuration["font"]["family"]} {int(round(configuration["font"]["size"] * 1.214))}"',
        "COLOR0": f"{configuration['colors'][theme]['background']}",
        "COLOR1": f"{configuration['colors'][theme]['grey']}",
        "COLOR2": f"{configuration['colors'][theme]['negative']}",
        "COLOR3": f"{configuration['colors'][theme]['foreground']}",
        "COLOR4": f"{configuration['colors'][theme]['neutral']}",
        "WIDTH": f"{average_width}px",
        "YOFFSET": f"{int(round(configuration['font']['size'] * average_scaling_factor * 2.75))}px",
    }
    with open(
        os.path.expanduser("~/.config/rofi/theme_config.rasi"), "w"
    ) as output_handle:
        output_handle.write("* {\n")
        for key, value in patched_configuration.items():
            output_handle.write(f"    {key}: {value};\n")
        output_handle.write("}\n")
    print("Patched rofi configuration ...")


def patch_xorg(configuration):
    dpis = []
    with open(os.path.expanduser("~/.Xresources"), "w") as output_handle:
        for monitor in configuration["monitors"]:
            dpis.append(configuration["monitors"][monitor]["diagonal_dpi"])
        average_dpi = int(round(sum(dpis) / len(dpis)))
        output_handle.write(f"Xft.dpi: {average_dpi}\n")
    print(f"Patched .Xresources with average DPI: {average_dpi}.")


def patch_kitty(configuration):
    theme = configuration["state"]["theme"]
    patched_configuration = {
        "allow_remote_control": "yes",
        "enable_audio_bell": "no",
        "font_size": int(round(configuration["font"]["size"] * 0.714)),
    }
    with open(os.path.expanduser("~/.config/kitty/kitty.conf"), "w") as output_handle:
        for key, value in patched_configuration.items():
            output_handle.write(f"{key} {value}\n")

    patched_configuration = {
        "background": configuration["colors"][theme]["background"],
        "selection_background": configuration["colors"][theme]["foreground"],
        "foreground": configuration["colors"][theme]["foreground"],
        "selection_foreground": configuration["colors"][theme]["background"],
        "font_family": configuration["font"]["family"],
        "cursor": configuration["colors"][theme]["cursor"],

        # black = 0/8
        # red = 1/9
        # green = 2/10
        # yellow = 3/11
        # blue = 4/12
        # magenta = 5/13
        # cyan = 6/14
        # white = 7/15

        "color0": configuration["colors"][theme]["cursor"],
        "color1": configuration["colors"][theme]["red"],
        "color2": configuration["colors"][theme]["green"],
        "color3": configuration["colors"][theme]["yellow"],
        "color4": configuration["colors"][theme]["blue"],
        "color5": configuration["colors"][theme]["magenta"],
        "color6": configuration["colors"][theme]["cyan"],
        "color7": configuration["colors"][theme]["background"],
        "color8": configuration["colors"][theme]["foreground"],
        "color9": configuration["colors"][theme]["pastel_red"],
        "color10": configuration["colors"][theme]["pastel_green"],
        "color11": configuration["colors"][theme]["pastel_blue"],
        "color12": configuration["colors"][theme]["pastel_yellow"],
        "color13": configuration["colors"][theme]["pastel_magenta"],
        "color14": configuration["colors"][theme]["pastel_cyan"],
        "color15": configuration["colors"][theme]["light_muted"],
    }
    with open(
        os.path.expanduser("~/.config/kitty/themes/nuunamnir.conf"), "w"
    ) as output_handle:
        for key, value in patched_configuration.items():
            output_handle.write(f"{key} {value}\n")

    print("Patched kitty configuration ...")


def patch_tmux(configuration):
    configuration_path = os.path.expanduser("~/.config/tmux/tmux.conf")

    theme = configuration["state"]["theme"]
    output = list()
    with open(configuration_path, "r") as input_handle:
        for line in input_handle:
            if line.startswith("color"):
                continue
            output.append(line)

    patched_configuration = {
        "color0": configuration["colors"][theme]["background"],
        "color1": configuration["colors"][theme]["grey"],
        "color2": configuration["colors"][theme]["grey"],
        "color3": configuration["colors"][theme]["neutral"],
        "color4": configuration["colors"][theme]["foreground"],
    }

    with open(configuration_path, "w") as output_handle:
        for key, value in patched_configuration.items():
            output_handle.write(f"{key}={value}\n")
        for line in output:
            output_handle.write(line)
    print("Patched tmux configuration ...")


def patch_starship(configuration):
    configuration_path = os.path.expanduser("~/.config/starship.toml")

    theme = configuration["state"]["theme"]
    with open(configuration_path, "r") as input_handle:
        starship_configuration = toml.load(input_handle)

    starship_configuration["palettes"]["theme"]["color0"] = configuration["colors"][theme]["foreground"]
    starship_configuration["palettes"]["theme"]["color1"] = configuration["colors"][theme]["cursor"]
    starship_configuration["palettes"]["theme"]["color2"] = configuration["colors"][theme]["positive"]
    starship_configuration["palettes"]["theme"]["color3"] = configuration["colors"][theme]["negative"]
    starship_configuration["palettes"]["theme"]["color4"] = configuration["colors"][theme]["neutral"]

    with open(configuration_path, "w") as output_handle:
        toml.dump(starship_configuration, output_handle)
    print("Patched starship configuration ...")


def patch_dunst(configuration):
    configuration_path = os.path.expanduser("~/.config/dunst/dunstrc")

    theme = configuration["state"]["theme"]
    with open(configuration_path, "r") as input_handle:
        dunst_configuration = configparser.ConfigParser(interpolation=None)
        dunst_configuration.read_file(input_handle)

    dunst_configuration["global"]["foreground"] = f'"{configuration["colors"][theme]["foreground"]}"'
    dunst_configuration["global"]["background"] = f'"{configuration["colors"][theme]["background"]}"'
    dunst_configuration["global"]["separator_color"] = f'"{configuration["colors"][theme]["background"]}"'
    dunst_configuration["global"]["font"] = f'"{configuration["font"]["family"]} {int(round(configuration["font"]["size"] * 0.714))}"'

    scaling_factors = list()
    for monitor in configuration["monitors"]:
        scaling_factors.append(configuration["monitors"][monitor]["scaling_factor"])
    average_scaling_factor = sum(scaling_factors) / len(scaling_factors)
    dunst_configuration["global"]["offset"] = f'0x{int(round(configuration["font"]["size"] * average_scaling_factor * 3))}'

    dunst_configuration["urgency_normal"]["foreground"] = f'"{configuration["colors"][theme]["foreground"]}"'
    dunst_configuration["urgency_normal"]["format"] = f"\" <span foreground='{configuration["colors"][theme]["neutral"]}'>%s</span>\\n  %b\""

    dunst_configuration["urgency_critical"]["foreground"] = f'"{configuration["colors"][theme]["foreground"]}"'
    dunst_configuration["urgency_critical"]["format"] = f"\" <span foreground='{configuration["colors"][theme]["negative"]}'>%s</span>\\n  %b\""

    dunst_configuration["urgency_low"]["foreground"] = f'"{configuration["colors"][theme]["foreground"]}"'
    dunst_configuration["urgency_low"]["format"] = f"\" <span foreground='{configuration["colors"][theme]["grey"]}'>%s</span>\\n  %b\""

    with open(configuration_path, "w") as output_handle:
        dunst_configuration.write(output_handle)
    print("Patched dunst configuration ...")


def patch_all(configuration):
    patch_rofi(configuration)
    patch_xorg(configuration)
    patch_kitty(configuration)
    patch_tmux(configuration)
    patch_starship(configuration)
    patch_dunst(configuration)


if __name__ == "__main__":
    with open(os.path.expanduser("~/.config/nuunamnir.json"), "r") as input_handle:
        configuration = json.load(input_handle)
    patch_all(configuration)

    subprocess.Popen(
        args=[
            "tmux",
            "source-file",
            os.path.expanduser(os.path.join("~", ".config", "tmux", "tmux.conf")),
        ]
    )
    subprocess.Popen(args=["kitty", "+kitten", "themes", "--reload-in=all", "nuunamnir"])
    subprocess.Popen(args=["killall", "dunst"])
    time.sleep(1)
    subprocess.Popen(args=["notify-send", "-u", "normal", "Patching", "All configurations reloaded ..."])
    subprocess.Popen(args=["kill", "-1", "`pgrep qutebrowser`"])
