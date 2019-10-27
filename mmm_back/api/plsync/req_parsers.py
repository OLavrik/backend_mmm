from flask_restplus import reqparse

sync_parser = reqparse.RequestParser()
sync_parser.add_argument('vk_user_id', type=int, help='VK user id')
sync_parser.add_argument('mts_kind', type=int, help='Playlist kind smth like 1012')
sync_parser.add_argument('mts_token',  help='token from mts cookies')
# sync_parser.add_argument('mts_sign', type=int, help='Rate to charge for this resource')
sync_parser.add_argument('mts_login',  help='Mts login like "uid-fke5ra"')
sync_parser.add_argument('mts_yandexuid',  help='"yandexuid" from cookies')
sync_parser.add_argument('mts_sign',  help='"mts_sign" from auth data')





