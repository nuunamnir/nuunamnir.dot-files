import io
import os
import json
import subprocess


class Kitty:
    def __init__(self, input_path, wm_theme):
        self.kitty_configuration = dict()
        with io.open(os.path.expanduser(os.path.join(input_path, 'kitty.conf')), 'r', encoding='utf-8') as input_handle:
            for line in input_handle:
                if line.startswith('#'):
                    continue
                line_pieces = line.rstrip().split()
                if len(line_pieces) > 1:
                    if line_pieces[0] == 'include':
                        continue
                    self.kitty_configuration[line_pieces[0]] = ' '.join(line_pieces[1:])
        
        self.kitty_configuration['font_family'] = wm_theme['fonts']['console']
        self.kitty_configuration['font_features'] = wm_theme['fonts']['features']
        self.kitty_configuration['font_size'] = wm_theme['fonts']['console_size']

        self.kitty_theme = {
            'background': wm_theme['colors']['black'], 
            'foreground': wm_theme['colors']['white'],
            'cursor': wm_theme['colors']['white'],
            'selection_background': wm_theme['colors']['grey1'],
            'selection_foreground': wm_theme['colors']['bright-black'],
            'color8': wm_theme['colors']['bright-black'],
            'color9': wm_theme['colors']['bright-red'],
            'color10': wm_theme['colors']['bright-green'],
            'color11': wm_theme['colors']['bright-yellow'],
            'color12': wm_theme['colors']['bright-blue'],
            'color13': wm_theme['colors']['bright-purple'],
            'color14': wm_theme['colors']['bright-cyan'],
            'color15': wm_theme['colors']['bright-white'],
            'color0': wm_theme['colors']['black'],
            'color1': wm_theme['colors']['red'],
            'color2': wm_theme['colors']['green'],
            'color3': wm_theme['colors']['yellow'],
            'color4': wm_theme['colors']['blue'],
            'color5': wm_theme['colors']['purple'],
            'color6': wm_theme['colors']['cyan'],
            'color7': wm_theme['colors']['white'],
        }

    def save(self, output_path):
        with io.open(os.path.expanduser(os.path.join(output_path, 'kitty.conf')), 'w', encoding='utf-8') as output_handle:
            for key in self.kitty_configuration:
                output_handle.write(' '.join([key, self.kitty_configuration[key]]) + '\n')

        with io.open(os.path.expanduser(os.path.join(output_path, 'themes', 'nuunamnir.conf')), 'w', encoding='utf-8') as output_handle:
            for key in self.kitty_theme:
                output_handle.write(' '.join([key, self.kitty_theme[key]]) + '\n')

    def update(self):
        subprocess.Popen(args=['kitty', '+kitten', 'themes', '--reload-in=all', 'nuunamnir'])


if __name__ == '__main__':
    theme_path=os.path.expanduser(os.path.join('~', 'Pictures', 'light_default', 'theme.json'))
    with io.open(theme_path, 'r', encoding='utf-8') as input_handle:
        theme_data = json.load(input_handle)
    kitty = Kitty(input_path=os.path.join('~', '.config', 'kitty'), wm_theme=theme_data)

'''
background            #dfdbc3   # most frequent color
foreground            #3b2322
selection_background  #a4a390
selection_foreground #dfdbc3
cursor                #73635a
color0                #000000   # black
color8                #7f7f7f   # bright black
color1                #cc0000   # red
color9                #cc0000   # bright red
color2                #009600   # green
color10               #009600   # bright green
color3                #d06b00   # yellow
color11               #d06b00   # bright yellow
color4                #0000cc   # blue
color12               #0000cc   # bright blue
color5                #cc00cc   # purple
color13               #cc00cc   # bright purple
color6                #0087cc   # cyan
color14               #0086cb   # bright cyan
color7                #cccccc   # white
color15               #ffffff   # bright white
'''