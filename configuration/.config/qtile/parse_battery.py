import subprocess
import json
import typing
import re

import libqtile.widget.base
from libqtile.utils import logger


class BatteryState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that displays the state of the battery."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 0.5, 'time between updates in seconds'), 
    ]

    def __init__(self, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(BatteryState.defaults)


    def read_battery(self):
        try:
            with open('/sys/class/power_supply/BAT0/charge_full', 'r') as input_handle:
                charge_full = int(input_handle.read().strip())
            with open('/sys/class/power_supply/BAT0/charge_now', 'r') as input_handle:
                charge_now = int(input_handle.read().strip())
            
            with open('/sys/class/power_supply/BAT0/status', 'r') as input_handle:
                status = input_handle.read().strip()

            status_icon = None
            if status == 'Discharging':
                status_icon = ' ▼'
            elif status == 'Charging':
                status_icon = ' ▲'
            else:
                status_icon = ''
            
            if status != 'Full':
                return f'{charge_now / charge_full * 100:.2f} %{status_icon}' 
            else:
                return f' '
        except Exception as e:
            logger.debug(f'no battery found')
        return f'󱐥'


    def poll(self):
        output_data = self.read_battery()
        return output_data


if __name__ == '__main__':
    print(BatteryState().read_battery())
