import requests
import re
from pprint import pprint
import pandas as pd

from collections import namedtuple

COOKIE_STRING = 'remixsid	a4ffcb52dfc1da55634824ce338f6a675a15c9fd76ef7f0bc117bd5e853a3	.vk.com	/	01.11.2020, 4:59:13	69 Б	✓	✓	'
def get_users_songs(user_id):

    cookies_vals = dict(re.findall(r'\s*(.+?)=(.+?);', COOKIE_STRING + ';'))
    cookie_jar = requests.cookies.cookiejar_from_dict(cookies_vals)

    session = requests.Session()
    session.cookies = cookie_jar

    form_data = {
        'access_hash': '',
        'act': 'load_section',
        'al': 1,
        'claim': 0,
        'offset': 0,
        'owner_id': user_id,
        'playlist_id': -1,
        'track_type': 'default',
        'type': 'playlist',
    }
    headers = {
        'Dnt': '1',
        'X-requested-with': 'XMLHttpRequest'
    }

    Song = namedtuple('Song', 'name author')

    def get_songs(offset):
        form_data['offset'] = offset
        form_data['claim'] += 1
        with session as s:
            res = s.post('https://vk.com/al_audio.php', cookies=cookie_jar, data=form_data, headers=headers)

            print('Request done. Parsing...')
            data = res.json()
            playlist = data['payload'][1][0]
            song_list = playlist['list']
            songs = [Song(song[3].strip(), song[4].strip()) for song in song_list]
            print('Got {len(songs)} songs.')


            return songs, playlist['nextOffset'], playlist['totalCount']

    cnt = 1
    songs = []
    offset = 0
    while len(songs) < cnt:
        songs_, next_offset, cnt = get_songs(offset)
        offset = next_offset
        songs = songs + songs_

    print('Totally Got {len(songs)} songs. I.E.:')
    pprint(songs[:10])
    return songs

get_users_songs(17278900)

