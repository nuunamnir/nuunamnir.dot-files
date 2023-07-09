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
            'background': wm_theme['colors']['background-accent'], 
            'foreground': wm_theme['colors']['foreground-accent'],
            'cursor': wm_theme['colors']['foreground-accent'],
            'selection_background': wm_theme['colors']['foreground-accent-alt1'],
            'selection_foreground': wm_theme['colors']['foreground-accent-complementary'],
            'color0': wm_theme['colors']['color1'],
            'color1': wm_theme['colors']['color2'],
            'color2': wm_theme['colors']['color3'],
            'color3': wm_theme['colors']['color4'],
            'color4': wm_theme['colors']['color5'],
            'color5': wm_theme['colors']['color6'],
            'color6': wm_theme['colors']['color7'],
            'color7': wm_theme['colors']['color8'],
            'color8': wm_theme['colors']['color9'],
            'color9': wm_theme['colors']['color10'],
            'color10': wm_theme['colors']['color11'],
            'color11': wm_theme['colors']['color12'],
            'color12': wm_theme['colors']['color13'],
            'color13': wm_theme['colors']['color14'],
            'color14': wm_theme['colors']['color15'],
            'color15': wm_theme['colors']['color16'],
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