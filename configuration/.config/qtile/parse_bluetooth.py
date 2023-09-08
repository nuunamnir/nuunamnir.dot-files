import subprocess
import json
import typing
import re

import libqtile.widget.base
from libqtile.utils import logger
import pydbus


class BluetoothState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that displays connected bluetooth devices."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 0.5, 'time between updates in seconds'), 
    ]

    def __init__(self, devices={}, **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(BluetoothState.defaults)
        self.devices = devices
        bus = pydbus.SystemBus()

        self.adapter = bus.get('org.bluez', '/org/bluez/hci0')
        self.mngr = bus.get('org.bluez', '/')


    def get_connected_devices(self):
        connected_devices_icons = []
        mngd_objs = self.mngr.GetManagedObjects()
        for path in mngd_objs:
            con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', False)
            if con_state:
                addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
                
                if addr in self.devices:
                    print(addr, mngd_objs[path].get('org.bluez.Battery1', {}))
                    connected_devices_icons.append(self.devices[addr])
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
