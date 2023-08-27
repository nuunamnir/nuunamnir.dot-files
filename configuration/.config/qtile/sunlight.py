import sys
import os
import subprocess
import signal
import io
import zoneinfo
import time
import datetime
import pickle
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

import requests


def update():
    logger.warning('updating ...')

    try:
        token_path = sys.argv[1]
    except IndexError:
        token_path = os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo'))
    with io.open(token_path, 'r', encoding='utf-8') as input_handle:
        for line in input_handle:
            token = line.strip()

    ip = requests.get('https://ident.me').content.decode('utf-8')
    url = f'https://ipinfo.io/{ip}?token={token}'

    data = requests.get(url, timeout=None)

    try:
        QTILE_THEME_MODE, QTILE_THEME_MODE_LOCK, sunrise, now, sunset, tzinfo = pickle.load(open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'rb'))
        logger.info('sunlight data loaded ...')
    except:
        tzinfo = zoneinfo.ZoneInfo('UTC')
        QTILE_THEME_MODE = 'dark'
        QTILE_THEME_MODE_LOCK = False
        now = datetime.datetime.now(tz=tzinfo)
        sunrise = datetime.datetime.now(tz=tzinfo).replace(hour=6, minute=0)
        sunset = datetime.datetime.now(tz=tzinfo).replace(hour=18, minute=0)

    success = False
    try:
        data_json = data.json()
        loc = data_json['loc']
        tzinfo = zoneinfo.ZoneInfo(data_json['timezone'])
        if loc is not None:
            lat, lng = loc.split(',')
            sun_data = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0').json()['results']
            sunset = datetime.datetime.fromisoformat(sun_data['sunset'])
            sunrise = datetime.datetime.fromisoformat(sun_data['sunrise'])

            now = datetime.datetime.now(tz=tzinfo)

            current_state = QTILE_THEME_MODE
            trigger_reload = False
            if now > sunrise and now < sunset:
                QTILE_THEME_MODE = 'light'
                if current_state != 'light':
                    trigger_reload = True
            else:
                QTILE_THEME_MODE = 'dark'
                if current_state != 'dark':
                    trigger_reload = True

            if trigger_reload and not QTILE_THEME_MODE_LOCK:
                subprocess.run(['pkill', '-SIGUSR1', 'qtile'])
            success = True
    except KeyError:
        pass

    if success:
        success = False
        pickle.dump((QTILE_THEME_MODE, QTILE_THEME_MODE_LOCK, sunrise, now, sunset, tzinfo), open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sunlight.pickle')), 'wb'))
        logger.info('sunlight data saved ...')


def handler(signum, frame):
    if signum == 10:
        update()
signal.signal(signal.SIGUSR1, handler)


if __name__ == '__main__':
    try:
        logger.info('sunlight service started ...')        
        while True:
            update()
            time.sleep(10 * 60)
    except KeyboardInterrupt:
        logger.info('sunlight service stopping ...')