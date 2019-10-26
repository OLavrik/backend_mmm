from .req_parsers import sync_parser
from flask import Response
from flask_restplus import Namespace, Resource, fields
import requests
from mmm_back.get_vk_music import get_users_songs
from collections import namedtuple

ns = Namespace('plsync', description='Service api for VK syncing')

req_post_sync = ns.model('Sync playlist', {
    'vk_user_id': fields.Integer(help='VK user id'),
    'mts_kind': fields.Integer(help='Playlist kind smth like 1012'),
    'mts_token': fields.String(help='token from mts cookies'),
    'mts_login': fields.String(help='Mts login like "uid-fke5ra"'),
    'mts_yandexuid': fields.String(help='"yandexuid" from cookies'),
    'mts_sign': fields.String(help='"mts_sign" from auth data')
})


MtsTrack = namedtuple('MtsTrack','id albumId')
def search_mts(search_field):
    query_params = {
        'text': search_field,
        'type': 'tracks'
    }
    res = requests.get('https://music.mts.ru/handlers/search.jsx', params=query_params)
    items = res.json()['tracks']['items']
    if len(items) == 0:
        return None
    t = items[0]
    return MtsTrack(t['id'], t['albums'][0]['id'])

def get_playlist_info(mts_login, mts_kind, mts_token):
    query_params = {
        'owner': mts_login,
        'kinds': mts_kind
    }
    cookies = dict(token=mts_token)

    res = requests.get('https://music.mts.ru/handlers/playlist.jsx',
                       params=query_params, cookies=cookies)
    pl = res.json()
    return pl['playlist']['revision']



def add_to_playlist(mts_tracks_list,mts_token, mts_yandexuid, mts_kind, mts_sign, cur_revision):
    form_url_encoded = {
        'diff': str([{"op": "insert", "at": 0, "tracks": [
            {"id": t.id, "albumId": t.albumId} for t in mts_tracks_list
        ]}]),
        'sign': mts_sign,
        'kind': mts_kind,
        'from': 'mtsweb-search-track-track-main',
        'revision': cur_revision
    }
    # headers = {
        # 'X-Current-UID':'972977063',
        # 'Host': 'music.mts.ru'
    # }
    cookies = dict(token=mts_token, yandexuid=mts_yandexuid)
    res = requests.post('https://music.mts.ru/handlers/playlist-patch.jsx',
                       data=form_url_encoded, cookies=cookies)#, headers=headers)

    return res.json()


@ns.route('/')
class Post(Resource):
    @ns.response(200, 'Success')
    @ns.expect(req_post_sync)
    def post(self):
        args = sync_parser.parse_args()

        songs_vk = get_users_songs(args['vk_user_id'])

        revision = get_playlist_info(args['mts_login'], args['mts_kind'], args['mts_token'])
        print(revision)
        mts_tracks_list = []
        for i, song in enumerate(songs_vk):
            mts_track = search_mts(song.name + ' ' + song.author)
            print(mts_track)
            if mts_track is not None:
                mts_tracks_list.append(mts_track)
            if i == 20:
                break

        patch_res = add_to_playlist(mts_tracks_list, args['mts_token'], args['mts_yandexuid'], args['mts_kind'], args['mts_sign'], revision)

        return patch_res, 200


