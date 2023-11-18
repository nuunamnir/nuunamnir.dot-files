import subprocess
import typing
import os
import datetime
import zoneinfo
import pickle

import libqtile.widget.base



class SunState(libqtile.widget.base.ThreadPoolText): # libqtile.widget.base.InLoopPollText
    """A text widgets that handles light and dark theme and ajusts it automatically based on state of the sun at a given location."""

    defaults: list[tuple[str, typing.Any, str]] = [
        ('update_interval', 10, 'time between updates in seconds'), 
    ]

    def __init__(self, token_path=os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo')), **config):
        libqtile.widget.base.ThreadPoolText.__init__(self, '', **config)
        self.add_defaults(SunState.defaults)

        try:
            self.QTILE_THEME_MODE, self.QTILE_THEME_MODE_LOCK, self.sunrise, self.now, self.sunset, self.tzinfo = pickle.load(open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'rb'))
        except:
            self.tzinfo = zoneinfo.ZoneInfo('UTC')
            self.QTILE_THEME_MODE = 'dark'
            self.QTILE_THEME_MODE_LOCK = False
            self.now = datetime.datetime.now(tz=self.tzinfo)
            self.sunrise = datetime.datetime.now(tz=self.tzinfo).replace(hour=6, minute=0)
            self.sunset = datetime.datetime.now(tz=self.tzinfo).replace(hour=18, minute=0)


    def _configure(self, qtile, bar):
        libqtile.widget.base.ThreadPoolText._configure(self, qtile, bar)
        self.add_callbacks({'Button1': self.show, 'Button2': self.toggle_lock, 'Button3': self.toggle_mode})


    def show(self):
        subprocess.run(['notify-send', 'Sunset/Sunrise', f'Sunrise: {self.sunrise.astimezone(self.tzinfo).isoformat()}\nNow:\t {self.now.astimezone(self.tzinfo).isoformat()}\nSunset:\t {self.sunset.astimezone(self.tzinfo).isoformat()}'])


    def toggle_lock(self):
        if self.QTILE_THEME_MODE_LOCK:
            self.QTILE_THEME_MODE_LOCK = False
        else:
            self.QTILE_THEME_MODE_LOCK = True
        pickle.dump((self.QTILE_THEME_MODE, self.QTILE_THEME_MODE_LOCK, self.sunrise, self.now, self.sunset, self.tzinfo), open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'wb'))
        subprocess.run(['pkill', '-SIGUSR1', '-f', 'sunlight.py'])
        self.update(self.poll())


    def toggle_mode(self):
        if self.QTILE_THEME_MODE == 'light':
            self.QTILE_THEME_MODE = 'dark'
        else:
            self.QTILE_THEME_MODE = 'light'
        self.QTILE_THEME_MODE_LOCK = True
        pickle.dump((self.QTILE_THEME_MODE, self.QTILE_THEME_MODE_LOCK, self.sunrise, self.now, self.sunset, self.tzinfo), open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'wb'))
        subprocess.run(['pkill', '-SIGUSR1', 'qtile'])
    

    def poll(self):
        try:
            self.QTILE_THEME_MODE, self.QTILE_THEME_MODE_LOCK, self.sunrise, self.now, self.sunset, self.tzinfo = pickle.load(open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'rb'))
        except:
            self.tzinfo = zoneinfo.ZoneInfo('UTC')
            self.QTILE_THEME_MODE = 'dark'
            self.QTILE_THEME_MODE_LOCK = False
            self.now = datetime.datetime.now(tz=self.tzinfo)
            self.sunrise = datetime.datetime.now(tz=self.tzinfo).replace(hour=6, minute=0)
            self.sunset = datetime.datetime.now(tz=self.tzinfo).replace(hour=18, minute=0)

        if not self.QTILE_THEME_MODE_LOCK:
            lock_str = '<sub></sub>'
        else:
            lock_str = '<sub> 󰌾</sub>'

        if self.QTILE_THEME_MODE == 'light':
            return f'󰖨{lock_str}'
        elif self.QTILE_THEME_MODE == 'dark':
            return f'{lock_str}'
        else:
            return f'󱎖{lock_str}'


if __name__ == '__main__':
    pass
