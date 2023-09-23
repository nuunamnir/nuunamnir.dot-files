import subprocess
import json
import typing
import re

import libqtile.widget.base
from libqtile.utils import logger
from gi.repository import Gio, GLib


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

    return result


class BluetoothState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that displays connected bluetooth devices."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 0.5, 'time between updates in seconds'), 
    ]

    def __init__(self, devices={}, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(BluetoothState.defaults)
        self.devices = devices

        self.mngr_proxy = timeout(Gio.DBusProxy().new_for_bus_sync, kwargs={
            'bus_type':Gio.BusType.SYSTEM,
            'flags':Gio.DBusProxyFlags.NONE,
            'info':None,
            'name':'org.bluez',
            'object_path':'/',
            'interface_name':'org.freedesktop.DBus.ObjectManager',
            'cancellable':None})

    def get_connected_devices(self):
        if self.mngr_proxy is None:
            return ''

        connected_devices_icons = []

        mngd_objs = self.mngr_proxy.GetManagedObjects()
        for obj_path, obj_data in mngd_objs.items():
            status = obj_data.get('org.bluez.Device1', {}).get('Connected')    
            if status:
                address = obj_data.get('org.bluez.Device1', {}).get('Address')                
                if address in self.devices:
                    connected_devices_icons.append(self.devices[address])
        return ' '.join(connected_devices_icons)


    def poll(self):
        output_data = self.get_connected_devices()
        return output_data


if __name__ == '__main__':
    devices = {
        'DD:F8:A4:C5:FE:55': '󰍽',
        'F8:4E:17:4C:D8:D2': '󰋎',
    }
    print(BluetoothState(devices=devices).get_connected_devices())