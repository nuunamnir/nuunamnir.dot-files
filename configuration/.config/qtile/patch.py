import os
import io
import json
import tomlkit
import logging
import configparser
import subprocess


def _patch_starship(theme_data, target_directory_path=os.path.expanduser(os.path.join("~", ".config"))):
    with io.open(os.path.join(target_directory_path, "starship.toml"), "r", encoding='utf-8') as input_handle:
        config = tomlkit.parse(input_handle.read())
    config['palettes']['nuunamnir']['alert1'] = theme_data['colors']['alert1']
    config['palettes']['nuunamnir']['alert2'] = theme_data['colors']['alert2']
    config['palettes']['nuunamnir']['alert3'] = theme_data['colors']['alert3']
    config['palettes']['nuunamnir']['grey1'] = theme_data['colors']['grey1']
    config['palettes']['nuunamnir']['grey2'] = theme_data['colors']['grey2']
    config['palettes']['nuunamnir']['grey3'] = theme_data['colors']['grey3']
    with io.open(os.path.join(target_directory_path, "starship.toml"), "w", encoding='utf-8') as output_handle:
        output_handle.write(tomlkit.dumps(config))


def _patch_gtk(theme_data, target_directory_path=os.path.expanduser(os.path.join("~", ".config", "gtk-3.0"))):
    config = configparser.ConfigParser()
    config.read(os.path.join(target_directory_path, "settings.ini"))
    config["Settings"]["gtk-cursor-theme-size"] = str(int(round(theme_data['dpi_diagonal'] / 6)))
    config["Settings"]["gtk-application-prefer-dark-theme"] = "true" if theme_data["mode"] == "dark" else "false"
    with io.open(
        os.path.join(target_directory_path, "settings.ini"), "w", encoding="utf-8"
    ) as output_handle:
        config.write(output_handle)


def _patch_dunst(
    theme_data,
    target_directory_path=os.path.expanduser(os.path.join("~", ".config", "dunst")),
):
    config = configparser.ConfigParser()
    config.read(os.path.join(target_directory_path, "dunstrc"))
    config["global"][
        "font"
    ] = f'{theme_data["fonts"]["console"]} {theme_data["fonts"]["console_size"]}'
    config["global"]["frame_width"] = "0"
    offset_x = int(round(theme_data["dpi_width"] / 2.54) * 0.5)
    offset_y = 2 * int(round(theme_data["dpi_height"] / 2.54) * 0.5) + int(
        round(theme_data["dpi_height"] / 2.54 * theme_data["bar_scaling"])
    )
    config["global"]["offset"] = f"{offset_x}x{offset_y}"
    config["global"]["width"] = str(int(round(theme_data["dpi_width"] / 2.54) * 16))
    config["global"]["gap_size"] = str(
        int(round(theme_data["dpi_height"] / 2.54) * 0.125)
    )
    config["global"]["corner_radius"] = "0"

    config["urgency_critical"]["background"] = f"\"{theme_data['colors']['alert1']}\""
    config["urgency_critical"]["foreground"] = f"\"{theme_data['colors']['white']}\""
    config["urgency_critical"][
        "frame_color"
    ] = f"\"{theme_data['colors']['bright-white']}\""
    config["urgency_normal"]["background"] = f"\"{theme_data['colors']['grey1']}\""
    config["urgency_normal"]["foreground"] = f"\"{theme_data['colors']['black']}\""
    config["urgency_normal"][
        "frame_color"
    ] = f"\"{theme_data['colors']['bright-white']}\""
    config["urgency_low"]["background"] = f"\"{theme_data['colors']['grey1']}\""
    config["urgency_low"]["foreground"] = f"\"{theme_data['colors']['white']}\""
    config["urgency_low"]["frame_color"] = f"\"{theme_data['colors']['bright-white']}\""
    with io.open(
        os.path.join(target_directory_path, "dunstrc"), "w", encoding="utf-8"
    ) as output_handle:
        config.write(output_handle)
    subprocess.run(["killall", "dunst"])


if __name__ == "__main__":
    theme_path = os.path.expanduser(
        os.path.join(
            "~",
            ".config",
            "qtile",
            "assets",
            "themes",
            "default",
            "light_default",
            "theme.json",
        )
    )
    with io.open(theme_path, "r", encoding="utf-8") as input_handle:
        theme_data = json.load(input_handle)
        theme_data["fonts"]["console_size"] = 18
        theme_data["dpi_width"] = 96
        theme_data["dpi_height"] = 96
        theme_data["bar_scaling"] = 1.25
    # _patch_dunst(theme_data)
    _patch_starship(theme_data)
