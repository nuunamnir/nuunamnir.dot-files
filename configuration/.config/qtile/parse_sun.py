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
        self.add_defaults(SunState.defaults)
     
        self._update_location()
        
        if os.environ.get('QTILE_THEME_MODE_LOCK', 'False') == 'False':
            self.lock = False
        else:
            self.lock = True

        self.state = os.environ.get('QTILE_THEME_MODE', 'unknown')
        self.token_path = token_path
        self.service_started = False
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
        subprocess.run(['pkill', '-SIGUSR1', 'qtile'])

    
    def _update_location(self):
        try:
            self.tzinfo, self.sunset, self.sunrise = pickle.load(open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sun.pickle')), 'rb'))
            now = datetime.datetime.now(tz=self.tzinfo)
            # subprocess.run(['notify-send', 'Sunset/Sunrise', f'Sunrise: {self.sunrise.astimezone(self.tzinfo).isoformat()}\nNow: {now.astimezone(self.tzinfo).isoformat()}\nSunset: {self.sunset.astimezone(self.tzinfo).isoformat()}'])
        except FileNotFoundError:
            self.tzinfo = zoneinfo.ZoneInfo('UTC')
            self.sunset = datetime.datetime.now(tz=self.tzinfo).replace(hour=18, minute=0)
            self.sunrise = datetime.datetime.now(tz=self.tzinfo).replace(hour=6, minute=0)
            logger.debug(f'correct sunset/sunrise not found, using current time: {self.sunset}')
            subprocess.run(['notify-send', '--urgency=critical', 'Sunset/Sunrise', f'Sunrise: {self.sunrise.astimezone(self.tzinfo).isoformat()}\nNow: {now.astimezone(self.tzinfo).isoformat()}\nSunset: {self.sunset.astimezone(self.tzinfo).isoformat()}'])


    def update(self, text):
        if self.text == text:
            return
        if text is None or text == '':
            text = f'󱎖<sub> </sub>'

        try:
            old_width = self.layout.width
            self.text = text

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
            lock_str = '<sub> </sub>'
        else:
            lock_str = '<sub> 󰌾</sub>'

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
                self.trigger_reload = False
                # qtile.cmd_reload_config()
                subprocess.run(['pkill', '-SIGUSR1', 'qtile'])
                return f'󱎖{lock_str}'

        if self.lock and self.state == 'unknown':
            self._update_location()



        if self.state == 'light':
            return f'󰖨{lock_str}'
        elif self.state == 'dark':
            return f'{lock_str}'
        else:
            return f'󱎖{lock_str}'


if __name__ == '__main__':
    pass
