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



class SunState(libqtile.widget.base.ThreadPoolText): # libqtile.widget.base.InLoopPollText
    """A text widgets that handles light and dark theme and ajusts it automatically based on state of the sun at a given location."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 10, 'time between updates in seconds'), 
    ]

    def __init__(self, token_path=os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo')), **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, "", **config)
        # libqtile.widget.base.InLoopPollText.__init__(self, "", **config)
        self.add_defaults(SunState.defaults)
     
        # self.tzinfo = zoneinfo.ZoneInfo('UTC')
        # self.sunrise = datetime.datetime.now(tz=self.tzinfo)
        # self.sunset = datetime.datetime.now(tz=self.tzinfo)
        self._update_location()
        
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        self.state = os.environ.get('QTILE_THEME_MODE', 'unknown')
        self.token_path = token_path
        self.service_started = False

        # self.progress_bar = ['\uEE06', '\uEE07', '\uEE08', '\uEE09', '\uEE0A', '\uEE0B']
        # self.progress_bar = ['\u25CE', '\u25D4', '\u25D1', '\u25D5', '\u25C9']
        self.progress_bar = ['\u25F4', '\u25F5', '\u25F6', '\u25F7']
        self.progress = 0
        self.trigger_reload = False


    def _configure(self, qtile, bar):
        libqtile.widget.base.ThreadPoolText._configure(self, qtile, bar)
        self.add_callbacks({"Button1": self.force_update, "Button2": self.toggle_lock, "Button3": self.toggle_mode})


    def force_update(self):
        self._update_location()
        #self.update(self.poll())


    def toggle_lock(self):
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True
        self.lock = not self.lock
        os.environ['QTILE_THEME_MODE_LOCK'] = str(self.lock)
        self.progress = 5
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
            now = datetime.datetime.now(tz=self.tzinfo)
            subprocess.run(['notify-send', 'Sunset/Sunrise', f'\nSunrise: {self.sunrise.strftime("%H:%M")}\nNow: {now.strftime("%H:%M")}\nSunset: {self.sunset.strftime("%H:%M")}'])
        except FileNotFoundError:
            self.tzinfo = zoneinfo.ZoneInfo('UTC')
            self.sunset = datetime.datetime.now(tz=self.tzinfo)
            self.sunrise = datetime.datetime.now(tz=self.tzinfo)
            logger.debug(f'correct sunset/sunrise not found, using current time: {self.sunset}')
            subprocess.run(['notify-send', '--urgency=critical', 'Sunset/Sunrise', f'Sunset: {self.sunset.strftime("%H:%M")}\nSunrise: {self.sunrise.strftime("%H:%M")}'])


    def update(self, text):
        if self.text == text:
            return
        if text is None:
            text = ""

        try:
            old_width = self.layout.width
            self.text = text

            # If our width hasn't changed, we just draw ourselves. Otherwise,
            # we draw the whole bar.
            if self.layout.width == old_width:
                self.draw()
            else:
                self.bar.draw()
        except TypeError:
            return


    def poll(self):
        if not self.service_started:
            subprocess.Popen(args=['python', os.path.expanduser(os.path.join('~', '.config', 'qtile', 'parse_sun_service.py')), self.token_path])
            self.service_started = True            
        
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        if not self.lock:
            now = datetime.datetime.now(tz=self.tzinfo)
            try:
                if now > self.sunrise and now < self.sunset:
                    if self.state != 'light':
                        self.state = 'light'
                        os.environ['QTILE_THEME_MODE'] = 'light'
                        self.trigger_reload = True
                else:
                    if self.state != 'dark':
                        self.state = 'dark'
                        os.environ['QTILE_THEME_MODE'] = 'dark'
                        self.trigger_reload = True
            except AttributeError as e:
                self.state = 'unknown'

            if self.trigger_reload:
                if self.progress % len(self.progress_bar) == len(self.progress_bar) - 1:
                    self.trigger_reload = False
                    qtile.cmd_reload_config()

        if self.lock and self.state == 'unknown':
            self._update_location()

        if not self.lock:
            lock_str = '<sub> </sub>'
        else:
            lock_str = '<sub> 󰌾</sub>'

        self.progress += 1
        if self.state == 'light':
            if self.progress < len(self.progress_bar):
                return f'󰖨' + lock_str + ' ' + self.progress_bar[self.progress % len(self.progress_bar)]
            else:
                return f'󰖨' + lock_str
        elif self.state == 'dark':
            if self.progress < len(self.progress_bar):
                return f'' + lock_str + ' ' + self.progress_bar[self.progress % len(self.progress_bar)]
            else:
                return f'' + lock_str
        else:
            return f'󱎖' + lock_str + ' ' + self.progress_bar[self.progress % len(self.progress_bar)]


if __name__ == '__main__':
    pass
