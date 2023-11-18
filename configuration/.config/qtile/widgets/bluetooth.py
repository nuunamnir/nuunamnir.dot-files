import os
import io
import json
import signal

import libqtile.widget.base
from gi.repository import Gio


class Bluetooth(libqtile.widget.base.ThreadPoolText):
    defaults = [
        (
            "update_interval",
            0.5,
            "time between polling for connected bluetooth devices in seconds",
        )
    ]

    def __init__(
        self,
        input_file_path=os.path.expanduser(
            os.path.join("~", ".config", "qtile", "widgets", "bluetooth.json")
        ),
        foreground="#ffffff",
        indicator_highlight="#ffffff",
        background="#000000",
        indicator_foreground="#ffffff",
        indicator_background="#000000",
        **config,
    ):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Bluetooth.defaults)

        with io.open(input_file_path, "r", encoding="utf-8") as input_handle:
            self._devices = json.load(input_handle)

        self.foreground = foreground
        self.indicator_highlight = indicator_highlight
        self.background = background
        self.indicator_background = indicator_background
        self.indicator_foreground = indicator_foreground

        self._mngr_proxy = self.timeout(
            Gio.DBusProxy().new_for_bus_sync,
            kwargs={
                "bus_type": Gio.BusType.SYSTEM,
                "flags": Gio.DBusProxyFlags.NONE,
                "info": None,
                "name": "org.bluez",
                "object_path": "/",
                "interface_name": "org.freedesktop.DBus.ObjectManager",
                "cancellable": None,
            },
        )

    def timeout(self, func, args=(), kwargs={}, timeout_duration=1, default=None):
        class TimeoutError(Exception):
            pass

        def handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout_duration)
        try:
            result = func(*args, **kwargs)
        except TimeoutError:
            result = default
        finally:
            signal.alarm(0)

        return result

    def poll(self):
        label = "nuunamnir.widgets.bluetooth.Bluetooth"

        if self._mngr_proxy is None:
            return ""

        connected_devices = []
        mngd_objs = self._mngr_proxy.GetManagedObjects()
        for obj_path, obj_data in mngd_objs.items():
            status = obj_data.get("org.bluez.Device1", {}).get("Connected")
            if status:
                address = obj_data.get("org.bluez.Device1", {}).get("Address")
                try:
                    battery = obj_data.get("org.bluez.Battery1", {}).get("Percentage")
                except AttributeError:
                    battery = None
                if address in self._devices:
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
        return (
            f'<span background="{self.background}">'
            + " ".join(connected_devices)
            + "</span>"
        )


if __name__ == "__main__":
    widget = Bluetooth()
    print(widget.poll())
