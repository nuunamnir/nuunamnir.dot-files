import subprocess
import json
import typing
import re
import os
import io
import requests
import datetime
import zoneinfo
import pickle

from libqtile import qtile
import libqtile.widget.base
from libqtile.utils import logger


class SunState(libqtile.widget.base.ThreadPoolText):
    """A text widgets that handles light and dark theme and ajusts it automatically based on state of the sun at a given location."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 10, 'time between updates in seconds'), 
    ]

    def __init__(self, token_path=os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo')), **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(SunState.defaults)
     
        self.tzinfo = None
        self.sunset = None
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        self.state = os.environ.get('QTILE_THEME_MODE', 'dark')
        subprocess.Popen(args=['python', os.path.expanduser(os.path.join('~', '.config', 'qtile', 'parse_sun_service.py')), token_path])

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
        try:
            self.tzinfo, self.sunset, self.sunrise = pickle.load(open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sun.pickle')), 'rb'))
        except FileNotFoundError:
            self.tzinfo = zoneinfo.ZoneInfo('UTC')
            self.sunset = datetime.datetime.now(tz=self.tzinfo)
            self.sunrise = datetime.datetime.now(tz=self.tzinfo)
            logger.debug(f'correct sunset/sunrise not found, using current time: {self.sunset}')

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
