import sys
import os
import io
import time
import datetime
import zoneinfo
import pickle

import psutil
import requests


if __name__ == '__main__':
    # token_path = os.path.expanduser(os.path.join('~', '.credentials', 'ipinfo'))
    token_path = sys.argv[1]
    with io.open(token_path, 'r', encoding='utf-8') as input_handle:
        for line in input_handle:
            token = line.strip()
    try:
        print('sun light service starting ...')
        running = True
        while running:
            for p in psutil.process_iter():
                if p.name() == 'python':
                    d = p.as_dict(attrs=['pid', 'cmdline'])
                    if d['pid'] <= os.getpid():
                        continue
                    for c in d['cmdline']:
                        if c.endswith('parse_sun_service.py'):
                            print('sun light service already running ...')
                            running = False
            if running:
                ip = requests.get('https://ident.me').content.decode('utf-8')
                url = f'https://ipinfo.io/{ip}?token={token}'
                r = requests.get(url, timeout=None)
                try:
                    loc = r.json()['loc']
                    tzinfo = zoneinfo.ZoneInfo(r.json()['timezone'])
                except KeyError:
                    pass
                if loc is not None:
                    lat, lng = loc.split(',')
                    sun_data = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0').json()['results']
                    sunset = datetime.datetime.fromisoformat(sun_data['sunset'])
                    sunrise = datetime.datetime.fromisoformat(sun_data['sunrise'])
                    pickle.dump((tzinfo, sunset, sunrise), open(os.path.expanduser(os.path.join('~', '.config', 'qtile', 'sun.pickle')), 'wb'))
                time.sleep(60 * 60)
    except KeyboardInterrupt:
        print('sun light service stopping ...')