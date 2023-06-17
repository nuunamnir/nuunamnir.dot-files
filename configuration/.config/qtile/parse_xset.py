import subprocess
import json
import typing
import re

import libqtile.widget.base


class InputState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that displays sensor values taken from the lm-sensors library."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 0.5, 'time between updates in seconds'), 
    ]

    def __init__(self, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(InputState.defaults)


    def input_data(self):
        output_data = {}
        command = ['xset', 'q']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        states = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", result.stdout)

        output_data = {}
        for k, s in states:
            if k == 'Num':
                output_data['numlock'] = '' if s.lower() == 'off' else ''
            elif k == 'Caps':
                output_data['capslock'] = '' if s.lower() == 'off' else ''

        return output_data


    def poll(self):
        output_data = self.input_data()
        return ' '.join([output_data['numlock'], output_data['capslock']])


if __name__ == '__main__':
    print(InputState().input_data())
