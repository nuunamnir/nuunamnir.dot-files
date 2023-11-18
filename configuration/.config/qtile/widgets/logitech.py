import os
import io
import json

import libqtile.widget.base
from logitech_receiver import Device, Receiver
from logitech_receiver.base import receivers_and_devices


class Logitech(libqtile.widget.base.ThreadPoolText):
    defaults = [
        (
            "update_interval",
            0.5,
            "time between polling for connected logitech devices in seconds",
        )
    ]

    def __init__(
        self,
        input_file_path=os.path.expanduser(
            os.path.join("~", ".config", "qtile", "widgets", "logitech.json")
        ),
        foreground="#ffffff",
        indicator_highlight="#ffffff",
        background="#000000",
        indicator_foreground="#ffffff",
        indicator_background="#000000",
        **config,
    ):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Logitech.defaults)

        with io.open(input_file_path, "r", encoding="utf-8") as input_handle:
            self._devices = json.load(input_handle)

        self.foreground = foreground
        self.indicator_highlight = indicator_highlight
        self.background = background
        self.indicator_background = indicator_background
        self.indicator_foreground = indicator_foreground

    def _get_devices(self):
        for dev_info in receivers_and_devices():
            try:
                d = (
                    Device.open(dev_info)
                    if dev_info.isDevice
                    else Receiver.open(dev_info)
                )
                if d is not None:
                    yield d
            except Exception as e:
                pass

    def poll(self):
        label = "nuunamnir.widgets.logitech.Logitech"

        connected_devices = []
        try:
            for receiver in self._get_devices():
                for device in list(receiver):
                    address = device.unitId
                    if address in self._devices:
                        battery = device.battery()[0]
                        if battery is None:
                            battery_str = ""
                        elif battery <= 10:
                            battery_str = f' <span foreground="{self.indicator_highlight}" background="{self.indicator_background}">🭻</span>'
                        elif battery <= 20:
                            battery_str = f' <span foreground="{self.indicator_foreground}" background="{self.indicator_background}">🭺</span>'
                        elif battery <= 40:
                            battery_str = f' <span foreground="{self.indicator_foreground}" background="{self.indicator_background}">🭹</span>'
                        elif battery <= 60:
                            battery_str = f' <span foreground="{self.indicator_foreground}" background="{self.indicator_background}">🭸</span>'
                        elif battery <= 90:
                            battery_str = f' <span foreground="{self.indicator_foreground}" background="{self.indicator_background}">🭷</span>'
                        else:
                            battery_str = f' <span foreground="{self.indicator_foreground}" background="{self.indicator_background}">🭶</span>'
                        connected_devices.append(self._devices[address] + battery_str)
        except ImportError:
            pass
        return (
            f'<span background="{self.background}">'
            + " ".join(connected_devices)
            + "</span>"
        )


if __name__ == "__main__":
    widget = Logitech()
    print(widget.poll())
