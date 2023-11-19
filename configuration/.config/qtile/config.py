# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
import os
import io
import collections
import subprocess
import logging
import json
import uuid
import pickle
import zoneinfo
import datetime

from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, logger

logger.setLevel(logging.WARNING)

import screeninfo

import utils
import debug

debugger = debug.Debugger()

import parse_sensors
import parse_xset
import parse_sun
import parse_battery

import widgets.bluetooth
import widgets.logitech
import widgets.audio

import patch


SYS_VARIABLES = utils.load_system_variables()
SYS_ID = uuid.getnode()
debugger.log(f"sys-id = {SYS_ID}")
if SYS_ID == 9190538989478:  # stationary computer
    SYS_VARIABLES["system_temperature"] = ["asusec-isa-", "T_Sensor"]
elif SYS_ID == 74780420245850:  # mobile computer
    SYS_VARIABLES["system_temperature"] = ["acpitz-acpi-", "temp1"]
debugger.log(f'font-scaling = {SYS_VARIABLES["font-scaling"]}')
debugger.log(f'font-scaling-console = {SYS_VARIABLES["font-scaling-console"]}')
debugger.log(f'bar-scaling = {SYS_VARIABLES["bar-scaling"]}')

try:
    QTILE_THEME_MODE, QTILE_THEME_MODE_LOCK, sunrise, now, sunset, tzinfo = pickle.load(
        open(
            os.path.expanduser(
                os.path.join("~", ".config", "qtile", "sunlight.pickle")
            ),
            "rb",
        )
    )
except:
    tzinfo = zoneinfo.ZoneInfo("UTC")
    QTILE_THEME_MODE = "dark"
    QTILE_THEME_MODE_LOCK = False
    now = datetime.datetime.now(tz=tzinfo)
    sunrise = datetime.datetime.now(tz=tzinfo).replace(hour=6, minute=0)
    sunset = datetime.datetime.now(tz=tzinfo).replace(hour=18, minute=0)
debugger.log(f"tzinfo = {str(tzinfo)}")
debugger.log(f"qtile-theme-mode = {QTILE_THEME_MODE}")
debugger.log(f"qtile-theme-mode-lock = {QTILE_THEME_MODE_LOCK}")
debugger.log(f"now = {now.isoformat()}")
debugger.log(f"sunrise = {sunrise.isoformat()}")
debugger.log(f"sunset = {sunset.isoformat()}")


# window manager theming
THEME_NAME = "default"
THEME_MODE = QTILE_THEME_MODE
# os.environ['QTILE_THEME_MODE'] = THEME_MODE

THEME = f"{THEME_MODE}_{THEME_NAME}"
logger.info(f"trying to apply {THEME}")

theme_path = os.path.expanduser(
    os.path.join(
        "~", ".config", "qtile", "assets", "themes", THEME_NAME, THEME, "theme.json"
    )
)
if not os.path.exists(theme_path):
    logger.warning(f"{THEME} not available, applying default")
    THEME_NAME = "default"
    THEME_MODE = QTILE_THEME_MODE
    # os.environ['QTILE_THEME_MODE'] = THEME_MODE
    THEME = f"{THEME_MODE}_{THEME_NAME}"
    theme_path = os.path.expanduser(
        os.path.join(
            "~", ".config", "qtile", "assets", "themes", THEME_NAME, THEME, "theme.json"
        )
    )

debugger.log(f"theme-name = {THEME_NAME}")
debugger.log(f"theme-mode = {THEME_MODE}")
debugger.log(f"theme = {THEME}")

with io.open(theme_path, "r", encoding="utf-8") as input_handle:
    theme_data = json.load(input_handle)
theme_data["colors"]["transparent"] = "#FFFFFF00"

if THEME_MODE == "light":
    theme_data["mode"] = "light"
else:
    theme_data["mode"] = "dark"

auto_template_assets_path = os.path.expanduser(
    os.path.join("~", ".config", "qtile", "assets", "auto_template")
)
auto_assets_path = os.path.expanduser(
    os.path.join("~", ".config", "qtile", "assets", "auto_instance")
)
try:
    os.makedirs(auto_assets_path)
except FileExistsError:
    pass
for asset in os.listdir(auto_template_assets_path):
    with io.open(
        os.path.join(auto_template_assets_path, asset), "r", encoding="utf-8"
    ) as input_handle:
        data = input_handle.read()
    data = data.replace("#100001", theme_data["colors"]["background"])
    with io.open(
        os.path.join(auto_assets_path, asset), "w", encoding="utf-8"
    ) as output_handle:
        output_handle.write(data)


monitors = screeninfo.get_monitors()[::-1]


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


group_names = "12345678"
chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
groups_by_screen = collections.defaultdict(list)
for i, chunk in enumerate(chunks):
    for name in chunk:
        groups_by_screen[i].append(name)

screens = []
dpi_diagonal_collector = []

layouts = {}
for i, monitor in enumerate(monitors):
    diagonal_mm = (monitor.width_mm**2 + monitor.height_mm**2) ** 0.5
    diagonal = (monitor.width**2 + monitor.height**2) ** 0.5

    diagonal_in = diagonal_mm / 25.4
    try:
        dpi_diagonal = diagonal / diagonal_in
    except ZeroDivisionError:
        dpi_diagonal = 96
    dpi_diagonal_collector.append(dpi_diagonal)

    width_in = monitor.width_mm / 25.4
    height_in = monitor.height_mm / 25.4

    try:
        dpi_width = monitor.width / width_in
    except ZeroDivisionError:
        dpi_width = 96
    try:
        dpi_height = monitor.height / height_in
    except ZeroDivisionError:
        dpi_height = 96

    layouts[i] = [
        layout.Columns(
            border_normal=theme_data["colors"]["background"],
            border_focus=theme_data["colors"]["bright-white"],
            border_focus_stack=theme_data["colors"]["white"],
            border_width=1,
            margin=[
                0,
                int(round(dpi_width / 2.54) * 0.5),
                int(round(dpi_height / 2.54) * 0.5),
                int(round(dpi_width / 2.54) * 0.5),
            ],
            margin_on_single=[
                0,
                int(round(dpi_width / 2.54) * 0.5),
                int(round(dpi_height / 2.54) * 0.5),
                int(round(dpi_width / 2.54) * 0.5),
            ],
        ),
        layout.Max(
            margin=[
                0,
                int(round(dpi_width / 2.54) * 0.5),
                int(round(dpi_height / 2.54) * 0.5),
                int(round(dpi_width / 2.54) * 0.5),
            ],
        ),
    ]

    widget_defaults = dict(
        font=theme_data["fonts"]["standard"],
        fontsize=int(round(dpi_height / 2.54 * SYS_VARIABLES["font-scaling"])),
        # padding=int(round(dpi_diagonal / 2.54 * 0.125)),
        background=theme_data["colors"]["background"],
    )
    extension_defaults = widget_defaults.copy()

    if i == 0:
        theme_data["fonts"]["console_size"] = str(
            int(
                round(
                    dpi_height
                    / 2.54
                    * SYS_VARIABLES["font-scaling"]
                    * SYS_VARIABLES["font-scaling-console"]
                )
            )
        )
        theme_data["dpi_width"] = dpi_width
        theme_data["dpi_height"] = dpi_height
        theme_data["dpi_diagonal"] = dpi_diagonal
        theme_data["bar-scaling"] = SYS_VARIABLES["bar-scaling"]

    b = bar.Bar(
        [
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.GroupBox(
                active=theme_data["colors"]["highlight-00"],
                block_highlight_text_color=theme_data["colors"]["highlight"],
                this_current_screen_border=theme_data["colors"]["background-00"],
                highlight_method="block",
                rounded=True,
                hide_unused=False,
                visible_groups=groups_by_screen[i],
                this_screen_border=theme_data["colors"]["background"],
                other_current_screen_border=theme_data["colors"]["background-02"],
                other_screen_border=theme_data["colors"]["background-02"],
                background=theme_data["colors"]["background"],
                inactive=theme_data["colors"]["background-00"],
                urgent_border=theme_data["colors"]["background-02"],
                urgent_text=theme_data["colors"]["highlight-00"],
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Spacer(background=theme_data["colors"]["transparent"]),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Prompt(
                background=theme_data["colors"]["background"],
                foreground=theme_data["colors"]["foreground"],
                cursor_color=theme_data["colors"]["background-02"],
                prompt=" ",
                fmt='<span color="'
                + theme_data["colors"]["background-02"]
                + '"></span> {}',
                cursor=True,
                rounded=True,
            ),
            widget.WindowName(
                fmt='<span rise="8pt">{}</span>',
                background=theme_data["colors"]["background"],
                foreground=theme_data["colors"]["foreground"],
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Spacer(background=theme_data["colors"]["transparent"]),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Clock(
                fmt='<span rise="8pt">{}</span>',
                format="%Y-%m-%d %a %H:%M:%S",
                background=theme_data["colors"]["background"],
                foreground=theme_data["colors"]["foreground"],
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
        ],
        size=int(round(dpi_height / 2.54 * SYS_VARIABLES["bar-scaling"])),
        margin=[
            int(round(dpi_height / 2.54) * 0.5),
            int(round(dpi_width / 2.54) * 0.5),
            int(round(dpi_height / 2.54) * 0.5),
            int(round(dpi_width / 2.54) * 0.5),
        ],
        background=theme_data["colors"]["transparent"],
    )
    # b.window.window.set_property('QTILE_BAR', 1, 'CARDINAL', 32)
    status_bar = bar.Bar(
        [
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widgets.logitech.Logitech(
                fmt='{}',
                foreground=theme_data["colors"]["foreground"],
                background=theme_data["colors"]["background"],
                indicator_foreground=theme_data["colors"]["background-02"],
                indicator_highlight=theme_data["colors"]["highlight"],
                indicator_background=theme_data["colors"]["background-00"],
                update_interval=5,
            ),
            widgets.bluetooth.Bluetooth(
                fmt='{}',
                foreground=theme_data["colors"]["foreground"],
                background=theme_data["colors"]["background"],
                indicator_foreground=theme_data["colors"]["background-02"],
                indicator_highlight=theme_data["colors"]["highlight"],
                indicator_background=theme_data["colors"]["background-00"],
            ),
            parse_battery.BatteryState(
                fmt='<span color="'
                + theme_data["colors"]["background-02"]
                + '">󱐋</span> <span color="'
                + theme_data["colors"]["foreground"]
                + '">{}</span>'
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Spacer(background=theme_data["colors"]["transparent"]),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            parse_sensors.Sensors(
                *SYS_VARIABLES["system_temperature"],
                fmt='<span color="'
                + theme_data["colors"]["background-02"]
                + '"></span> <span rise="-2pt">{}° C</span>',
                update_inverval=10,
                foreground=theme_data["colors"]["foreground"],
            ),
            parse_xset.InputState(
                fmt='<span color="'
                + theme_data["colors"]["background-02"]
                + '">{}</span>',
                update_inverval=0.5,
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Spacer(background=theme_data["colors"]["transparent"]),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widgets.audio.Audio(
                fmt='<span color="' + theme_data["colors"]["foreground"] + '">{}</span>',
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            widget.Spacer(background=theme_data["colors"]["transparent"]),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_left.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
            parse_sun.SunState(
                fmt='<span color="' + theme_data["colors"]["foreground"] + '">{}</span>'
            ),
            widget.Image(
                padding=0,
                margin=0,
                filename=os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "auto_instance",
                    "end_cap_right.svg",
                ),
                background=theme_data["colors"]["transparent"],
            ),
        ],
        size=int(round(dpi_height / 2.54 * SYS_VARIABLES["bar-scaling"])),
        margin=[
            0,
            int(round(dpi_width / 2.54) * 0.5),
            int(round(dpi_height / 2.54) * 0.5),
            int(round(dpi_width / 2.54) * 0.5),
        ],
        background=theme_data["colors"]["transparent"],
    )
    debugger.log(f"monitor = {str(i)}")
    debugger.log(f"monitor-width = {str(monitor.width)}")
    debugger.log(f"monitor-height = {str(monitor.height)}")
    debugger.log(f"monitor-width-mm = {str(monitor.width_mm)}")
    debugger.log(f"monitor-height-mm = {str(monitor.height_mm)}")
    debugger.log(f"dpi-width = {str(dpi_width)}")
    debugger.log(f"dpi-height = {str(dpi_height)}")
    debugger.log(f"dpi-diagonal = {str(dpi_diagonal)}")
    debugger.log(
        f'font-size = {str(int(round(dpi_height / 2.54 * SYS_VARIABLES["font-scaling"])))}'
    )
    debugger.log(
        f'bar-size = {str(int(round(dpi_height / 2.54 * SYS_VARIABLES["bar-scaling"])))}'
    )
    screens.append(Screen(top=b, bottom=status_bar))

debugger.log(json.dumps(theme_data, indent=4))

xresources_config = {}
xresources_path = os.path.expanduser(os.path.join("~", ".Xresources"))
with io.open(xresources_path, "r", encoding="utf-8") as input_handle:
    for line in input_handle:
        k, v = line.rstrip().split()
        xresources_config[k] = v


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


xresources_config["Xft.dpi:"] = str(int(round(theme_data["dpi_diagonal"])))
xresources_config["Xcursor.size:"] = str(int(round(theme_data["dpi_diagonal"] / 6)))
with io.open(xresources_path, "w", encoding="utf-8") as output_handle:
    for key in xresources_config.keys():
        output_handle.write(" ".join([key, xresources_config[key]]) + "\n")

debugger.log(f'xft-dpi = {str(xresources_config["Xft.dpi:"])}')
debugger.log(f'xcursor-size = {str(xresources_config["Xcursor.size:"])}')


groups = []
chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
for i, chunk in enumerate(chunks):
    for name in chunk:
        groups.append(Group(name=name, layouts=layouts[i]))


@hook.subscribe.startup
def _():
    subprocess.Popen(args=["picom"])
    if theme_data["wallpaper"] == "stretched" or theme_data["wallpaper"] == "centered":
        wallpaper_mode = "--bg-fill"
    elif theme_data["wallpaper"] == "tiled":
        wallpaper_mode = "--bg-tile"
    else:
        raise ValueError

    subprocess.Popen(
        args=[
            "feh",
            wallpaper_mode,
            os.path.expanduser(
                os.path.join(
                    "~",
                    ".config",
                    "qtile",
                    "assets",
                    "themes",
                    THEME_NAME,
                    THEME,
                    "wallpaper.png",
                )
            ),
        ]
    )
    patch._patch_kitty(theme_data)
    patch._patch_dunst(theme_data)
    patch._patch_starship(theme_data)
    patch._patch_gtk(theme_data)
    patch._patch_rofi(theme_data)


@hook.subscribe.startup_complete
def send_to_second_screen():
    chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
    for i, chunk in enumerate(chunks):
        # qtile.groups_map[chunk[0]].cmd_toscreen(i, toggle=False)
        qtile.groups_map[chunk[0]].toscreen(i)
        # logger.warning(f'{chunk[0]}, {i}')


mod = "mod4"

terminal = guess_terminal()


@lazy.function
def backlight(qtile, direction, steps=20):
    with open(
        "/sys/class/backlight/intel_backlight/max_brightness", "r"
    ) as input_handle:
        max_brightness = int(input_handle.read().strip())

    with open("/sys/class/backlight/intel_backlight/brightness", "r") as input_handle:
        current_brightness = int(input_handle.read().strip())

    if direction == "inc":
        current_brightness = min(
            max_brightness, current_brightness + max_brightness / steps
        )
    elif direction == "dec":
        current_brightness = max(0, current_brightness - max_brightness / steps)
    else:
        raise ValueError(f"direction: {direction}")

    new_brightness = str(int(round(current_brightness)))
    with open("/sys/class/backlight/intel_backlight/brightness", "w") as output_handle:
        output_handle.write(new_brightness)


keys = [
    Key([], "XF86MonBrightnessUp", backlight("inc")),
    Key([], "XF86MonBrightnessDown", backlight("dec")),

    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute/Unmute Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Raise Volume by 5%"), 
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle window floating"),
    Key(
        [mod, "control"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle window fullscreen",
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod, "shift"],
        "Tab",
        lazy.hide_show_bar("bottom"),
        desc="Toggle bottom bar visibility",
    ),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Spawn a command using rofi."),
    Key(
        [mod, "shift"],
        "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget",
    ),
]

for i in groups:
    for screen in groups_by_screen:
        if i.name in groups_by_screen[screen]:
            break
    lazy.group[i.name].toscreen(screen)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(screen),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_normal=theme_data["colors"]["background"],
    border_focus=theme_data["colors"]["highlight-00"],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
