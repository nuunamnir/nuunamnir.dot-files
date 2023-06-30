import subprocess
import json
import typing
import re
import os
import io
import requests
import datetime
import zoneinfo
from libqtile.utils import send_notification
from libqtile.command.client import CommandClient
from libqtile import qtile

import libqtile.widget.base


class SunState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that handles light and dark theme and ajusts it automatically based on state of the sun at a given location."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 10, 'time between updates in seconds'), 
    ]

    def __init__(self, token_path=os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo')), **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(SunState.defaults)

        self.c = CommandClient()

        with io.open(token_path, 'r', encoding='utf-8') as input_handle:
            for line in input_handle:
                self.token = line.strip()
        
        self.loc = None
        self.tzinfo = None
        self.sunset = None
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        self.counter = 0
        self.state = os.environ.get('QTILE_THEME_MODE', 'dark')
        self._update_location()


    def _configure(self, qtile, bar):
        libqtile.widget.base.ThreadPoolText._configure(self, qtile, bar)
        self.add_callbacks({"Button1": self.force_update, "Button2": self.toggle_lock, "Button3": self.toggle_mode})

    def force_update(self):
        self._update_location()
        self.update(self.poll())

    def toggle_lock(self):
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True
        self.lock = not self.lock
        os.environ['QTILE_THEME_MODE_LOCK'] = str(self.lock)
        self.update(self.poll())


    def toggle_mode(self):
        send_notification('test', 'test')
        if os.environ.get('QTILE_THEME_MODE', 'light') == 'light':
            os.environ['QTILE_THEME_MODE'] = 'dark'
            self.state = 'light'
        else:
            os.environ['QTILE_THEME_MODE'] = 'light'
            self.state = 'dark'
        os.environ['QTILE_THEME_MODE_LOCK'] = str(True)
        self.lock = True
        qtile.cmd_reload_config()

    
    def _update_location(self):
        self.ip = requests.get('https://ident.me').content.decode('utf-8')
        self.url = f'https://ipinfo.io/{self.ip}?token={self.token}'
        r = requests.get(self.url, timeout=None)
        try:
            self.loc = r.json()['loc']
            self.tzinfo = zoneinfo.ZoneInfo(r.json()['timezone'])
        except KeyError:
            pass
        if self.loc is not None:
            lat, lng = self.loc.split(',')
            sun_data = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0').json()['results']
            self.sunset = datetime.datetime.fromisoformat(sun_data['sunset'])
            self.sunrise = datetime.datetime.fromisoformat(sun_data['sunrise'])
        self.counter += 1


    def poll(self):
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        if not self.lock:
            now = datetime.datetime.now(tz=self.tzinfo)
            try:
                if now > self.sunrise and now < self.sunset:
                    os.environ['QTILE_THEME_MODE'] = 'light'
                    if self.state == 'dark':
                        self.state = 'light'
                        qtile.cmd_reload_config()

                else:
                    os.environ['QTILE_THEME_MODE'] = 'dark'
                    if self.state == 'light':
                        self.state = 'dark'
                        qtile.cmd_reload_config()
            except AttributeError:
                self.state = 'unknown'

        if self.lock and self.state == 'unknown':
            self._update_location()

        if not self.lock:
            lock_str = '<sub> </sub>'
        else:
            lock_str = '<sub> 󰌾</sub>'

        if self.state == 'light':
            return f'󰖨' + lock_str
        elif self.state == 'dark':
            return f'' + lock_str
        else:
            return f'󱎖' + lock_str


if __name__ == '__main__':
    pass
