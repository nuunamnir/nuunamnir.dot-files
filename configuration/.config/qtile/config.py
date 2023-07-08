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

# calculate screen specific vertical unit (vunit) according to which all widgets are scaled
import math
import os
import io
import collections
import subprocess
import logging
import json
import uuid

from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, logger

import screeninfo
import numpy

import parse_sensors
import parse_xset
import parse_sun

logger.setLevel(logging.WARNING)

SYS_ID = uuid.getnode()
SYS_VARIABLES = {
    'font_scaling': 0.75,
    'font_scaling_kitty': 0.75, 
    'bar_scaling': 1.25,
    'system_temperature': ['asusec-isa-', 'T_Sensor']
}
if SYS_ID == 9190538989478: # stationary computer
    pass
elif SYS_ID == 74780420245850: # mobile computer
    SYS_VARIABLES['font_scaling'] = 0.35
    SYS_VARIABLES['font_scaling_kitty'] = 0.25
    SYS_VARIABLES['bar_scaling'] = 0.8
    SYS_VARIABLES['system_temperature'] = ['acpitz-acpi-', 'temp1']
else:
    pass


THEME_MODE = os.environ.get('QTILE_THEME_MODE', 'light')
os.environ['QTILE_THEME_MODE'] = THEME_MODE

THEME = f'{THEME_MODE}_standard'
logger.warn(THEME)

theme_path = os.path.expanduser(os.path.join('~', 'Pictures', THEME, 'theme.json'))
auto_assets_path = os.path.expanduser(os.path.join('~', '.config', 'qtile', 'assets', THEME))
try:
    os.makedirs(auto_assets_path)
except FileExistsError:
    pass

themes = {
        'default': {
            'colors': {
                'background': '#402C25FF',
                'this-current-screen-border': '#FFD8A0FF',
                'other-current-screen-border': '#FF0000FF',
                'active': '#1A161AFF',
                'inactive': '#806C50FF',
                'border-focus-stack': '#FF0000FF',
                'transparent': '#FFFFFF00',
                'foreground': '#FFFFFFFF',
            },
            'fonts': {
                'standard': 'Cantarell',
                'console': 'Fira Code Regular',
                'font-features': 'FiraCode-Regular +cv16 +ss02',
            }
        },
    }

auto_template_assets_path = os.path.expanduser(os.path.join('~', '.config', 'qtile', 'assets', 'auto_template'))
logger.warn('searching for theme file ...')
if os.path.isfile(theme_path):
    logger.warn('theme file found')
    with io.open(theme_path, 'r', encoding='utf-8') as input_handle:
        theme_data = json.load(input_handle)
        themes[THEME] = {
            'colors': {
                'background': theme_data['colors']['background-accent'],
                'this-current-screen-border': theme_data['colors']['foreground-accent-alt1'],
                'other-current-screen-border': '#FF0000FF',
                'active':  theme_data['colors']['foreground-accent-complementary'],
                'info': theme_data['colors']['foreground-accent-alt2'],
                'inactive': theme_data['colors']['foreground-accent'],
                'urgent-background': theme_data['colors']['foreground-accent-complementary'],
                'border-focus-stack': '#FF0000FF',
                'transparent': '#FFFFFF00',
                'foreground': theme_data['colors']['foreground'],
            },
            'fonts': {
                'standard': 'FiraCode Nerd Font',
                'console': 'Fira Code Regular',
                'font-features': 'FiraCode-Regular +cv16 +ss02',
            },
            'wallpaper': theme_data['wallpaper']
        }
        for asset in os.listdir(auto_template_assets_path):
            with io.open(os.path.join(auto_template_assets_path, asset), 'r', encoding='utf-8') as input_handle:
                data = input_handle.read()
            data = data.replace('#100001', theme_data['colors']['background-accent'])
            with io.open(os.path.join(auto_assets_path, asset), 'w', encoding='utf-8') as output_handle:
                output_handle.write(data)
else:
    THEME = 'default'

kitty_config = {}
kitty_path = os.path.expanduser(os.path.join('~', '.config', 'kitty', 'kitty.conf'))
with io.open(kitty_path, 'r', encoding='utf-8') as input_handle:
    for line in input_handle:
        line_pieces = line.rstrip().split(' ')
        kitty_config[line_pieces[0]] = ' '.join(line_pieces[1:])

kitty_theme = {}
kitty_theme['background'] = themes[THEME]['colors']['background']
kitty_theme['foreground'] = themes[THEME]['colors']['inactive']
kitty_theme['cursor'] = themes[THEME]['colors']['inactive']
kitty_theme['selection_background'] = themes[THEME]['colors']['this-current-screen-border']
kitty_theme['selection_foreground'] = themes[THEME]['colors']['urgent-background']
kitty_theme['color3'] = themes[THEME]['colors']['info']
monitors = screeninfo.get_monitors()[::-1]

layouts = {} 

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

group_names = '12345678'
chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
groups_by_screen = collections.defaultdict(list)
for i, chunk in enumerate(chunks):
    for name in chunk:
        groups_by_screen[i].append(name)

screens = []
dpi_diagonal_collector = []


for i, monitor in enumerate(monitors):
    diagonal_mm = (monitor.width_mm ** 2 + monitor.height_mm ** 2) ** 0.5
    diagonal = (monitor.width ** 2 + monitor.height ** 2) ** 0.5
    diagonal_in = diagonal_mm / 25.4
    dpi_diagonal = diagonal / diagonal_in
    dpi_diagonal_collector.append(dpi_diagonal)

    width_in = monitor.width_mm / 25.4
    height_in = monitor.height_mm / 25.4
    dpi_width = monitor.width / width_in
    dpi_height = monitor.height / height_in

    layouts[i] = [
        layout.Columns(
            border_normal=themes[THEME]['colors']['background'],
            border_focus=themes[THEME]['colors']['this-current-screen-border'],
            border_focus_stack=themes[THEME]['colors']['border-focus-stack'],
            border_width=1,
            margin=[0, int(round(dpi_width / 2.54) * 0.5), int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5)],
            margin_on_single=[0, int(round(dpi_width / 2.54) * 0.5), int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5)],
        ),
        layout.Max(
            margin=[0, int(round(dpi_width / 2.54) * 0.5), int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5)],
        ),
    ]

    widget_defaults = dict(
        font=themes[THEME]['fonts']['standard'],
        fontsize=int(round(dpi_height / 2.54 * SYS_VARIABLES['font_scaling'])),
        # padding=int(round(dpi_diagonal / 2.54 * 0.125)),
        background=themes[THEME]['colors']['background'],
    )
    extension_defaults = widget_defaults.copy()
    kitty_config['font_family'] = themes[THEME]['fonts']['console']
    kitty_config['font_size'] = str(int(round(dpi_height / 2.54 * SYS_VARIABLES['font_scaling'] * SYS_VARIABLES['font_scaling_kitty'])))
    kitty_config['font_features'] = themes[THEME]['fonts']['font-features']

    b = bar.Bar(
        [
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_left.svg'), background=themes[THEME]['colors']['transparent']),
            widget.GroupBox(
                active=themes[THEME]['colors']['this-current-screen-border'],
                block_highlight_text_color=themes[THEME]['colors']['active'],
                this_current_screen_border=themes[THEME]['colors']['this-current-screen-border'],
                highlight_method='block',
                rounded=True,
                hide_unused=False,
                visible_groups=groups_by_screen[i],
                this_screen_border=themes[THEME]['colors']['background'],
                other_current_screen_border=themes[THEME]['colors']['other-current-screen-border'],
                other_screen_border=themes[THEME]['colors']['other-current-screen-border'],
                background=themes[THEME]['colors']['background'],
                inactive=themes[THEME]['colors']['inactive'],
                urgent_border=themes[THEME]['colors']['urgent-background'],
                urgent_text=themes[THEME]['colors']['this-current-screen-border'],
            ),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_right.svg'), background=themes[THEME]['colors']['transparent']),
            widget.Spacer(background=themes[THEME]['colors']['transparent']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_left.svg'), background=themes[THEME]['colors']['transparent']),
            widget.Prompt(background=themes[THEME]['colors']['background'], cursor_color=themes[THEME]['colors']['foreground'], prompt=' ', fmt='<span color="' + themes[THEME]['colors']['info'] + '"></span> {}', cursor=False, rounded=True),
            widget.WindowName(fmt='<span rise="8pt">{}</span>', background=themes[THEME]['colors']['background'], foreground=themes[THEME]['colors']['inactive']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_right.svg'), background=themes[THEME]['colors']['transparent']),
            widget.Spacer(background=themes[THEME]['colors']['transparent']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_left.svg'), background=themes[THEME]['colors']['transparent']),
            widget.Clock(fmt='<span rise="8pt">{}</span>', format='%Y-%m-%d %a %H:%M:%S', background=themes[THEME]['colors']['background'], foreground=themes[THEME]['colors']['inactive']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_right.svg'), background=themes[THEME]['colors']['transparent']),
        ],
        size=int(round(dpi_height / 2.54 * SYS_VARIABLES['bar_scaling'])),
        margin=[int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5), int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5)],
        background=themes[THEME]['colors']['transparent'],
    )
    # b.window.window.set_property('QTILE_BAR', 1, 'CARDINAL', 32)
    status_bar = bar.Bar(
        [
            widget.Spacer(background=themes[THEME]['colors']['transparent']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_left.svg'), background=themes[THEME]['colors']['transparent']),
            parse_sensors.Sensors(*SYS_VARIABLES['system_temperature'], fmt='<span color="' + themes[THEME]['colors']['info'] + '"></span> <span rise="-2pt">{}° C</span>', update_inverval=10, foreground=themes[THEME]['colors']['inactive']),
            parse_xset.InputState(fmt='<span color="' + themes[THEME]['colors']['info'] + '">{}</span>', update_inverval=0.5),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_right.svg'), background=themes[THEME]['colors']['transparent']),
            widget.Spacer(background=themes[THEME]['colors']['transparent']),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_left.svg'), background=themes[THEME]['colors']['transparent']),
            parse_sun.SunState(fmt='<span color="' + themes[THEME]['colors']['info'] + '">{}</span>'),
            widget.Image(padding=0, margin=0, filename=os.path.join('~', '.config', 'qtile', 'assets', THEME, 'end_cap_right.svg'), background=themes[THEME]['colors']['transparent']),
        ],
        size=int(round(dpi_height / 2.54 * SYS_VARIABLES['bar_scaling'])),
        margin=[0, int(round(dpi_width / 2.54) * 0.5), int(round(dpi_height / 2.54) * 0.5), int(round(dpi_width / 2.54) * 0.5)],
        background=themes[THEME]['colors']['transparent'],
    )
    screens.append(Screen(top=b, bottom=status_bar))

with io.open(kitty_path, 'w', encoding='utf-8') as output_handle:
    for key in kitty_config.keys():
        output_handle.write(' '.join([key, kitty_config[key]]) + '\n')
kitty_theme_path = os.path.expanduser(os.path.join('~', '.config', 'kitty', 'themes', 'nuunamnir.conf'))
with io.open(kitty_theme_path, 'w', encoding='utf-8') as output_handle:
    for key in kitty_theme.keys():
        output_handle.write(' '.join([key, kitty_theme[key]]) + '\n')

xresources_config = {}
xresources_path = os.path.expanduser(os.path.join('~', '.Xresources'))
with io.open(xresources_path, 'r', encoding='utf-8') as input_handle:
    for line in input_handle:
        k, v = line.rstrip().split()
        xresources_config[k] = v

xresources_config['Xft.dpi:'] = str(int(round(numpy.mean(dpi_diagonal_collector))))
xresources_config['Xcursor.size:'] = str(int(round(numpy.mean(dpi_diagonal_collector) / 12)))
with io.open(xresources_path, 'w', encoding='utf-8') as output_handle:
    for key in xresources_config.keys():
        output_handle.write(' '.join([key, xresources_config[key]]) + '\n')



groups = []
chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
for i, chunk in enumerate(chunks):
    for name in chunk:
        groups.append(Group(name=name, layouts=layouts[i]))

@hook.subscribe.startup
def _():
    subprocess.Popen(args=['picom'])
    if themes[THEME]['wallpaper'] == 'stretched' or themes[THEME]['wallpaper'] == 'centered':
        wallpaper_mode = '--bg-fill'
    elif themes[THEME]['wallpaper'] == 'tiled':
        wallpaper_mode = '--bg-tile'
    else:
        raise ValueError

    subprocess.Popen(args=['feh', wallpaper_mode, os.path.expanduser(os.path.join('~', 'Pictures', THEME, 'wallpaper.png'))])
    subprocess.Popen(args=['kitty', '+kitten', 'themes', '--reload-in=all', 'nuunamnir'])


@hook.subscribe.startup_complete
def send_to_second_screen():
    chunks = divide_chunks(group_names, math.ceil(len(group_names) / len(monitors)))
    for i, chunk in enumerate(chunks):
        #qtile.groups_map[chunk[0]].cmd_toscreen(i, toggle=False)
        qtile.groups_map[chunk[0]].cmd_toscreen(i)
        logger.warning(f'{chunk[0]}, {i}')
 
mod = "mod4"

terminal = guess_terminal()

@lazy.function
def spawn_prompt_on_active_screen(qtile):
    qtile.current_screen.cmd_spawn()

keys = [
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
    Key([mod, 'shift'], "Tab", lazy.hide_show_bar('bottom'), desc="Toggle bottom bar visibility"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, 'shift'], "r", spawn_prompt_on_active_screen(), desc="Spawn a command using a prompt widget"),
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
    border_normal=themes[THEME]['colors']['background'],
    border_focus=themes[THEME]['colors']['this-current-screen-border'],
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
