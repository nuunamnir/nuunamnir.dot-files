import subprocess
import json
import typing

import libqtile.widget.base


class Sensors(libqtile.widget.base.ThreadPoolText):
    """A text widgets that displays sensor values taken from the lm-sensors library."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ("sensor", 'system-temperature', "the systems average temperature"),
    ]

    def __init__(self, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Sensors.defaults)


    def sensors_data(self):
        output_data = {}
        command = ['sensors', '-j']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        data = json.loads(result.stdout)
        for k in data:
            if k.startswith('asusec-isa-'):
                output_data = {
                    'system-temperature': float(data[k]['T_Sensor'][list(data[k]['T_Sensor'])[0]]),
                }
        return output_data


    def poll(self):
        output_data = self.sensors_data()
        return f'{output_data["system-temperature"]:.0f}'


if __name__ == '__main__':
    print(sensors_data())

    