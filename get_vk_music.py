import requests
import re
from pprint import pprint
# import pandas as pd
from http.cookiejar import Cookie
from collections import namedtuple

import json
import random
import re
import time

import requests

import json
import logging
import random
import re
import threading
import time

import requests
import six

import jconfig


RE_LOGIN_HASH = re.compile(r'name="lg_h" value="([a-z0-9]+)"')
RE_CAPTCHAID = re.compile(r"onLoginCaptcha\('(\d+)'")
RE_NUMBER_HASH = re.compile(r"al_page: '3', hash: '([a-z0-9]+)'")
RE_AUTH_HASH = re.compile(
    r"\{.*?act: 'a_authcheck_code'.+?hash: '([a-z_0-9]+)'.*?\}"
)
RE_TOKEN_URL = re.compile(r'location\.href = "(.*?)"\+addr;')

RE_PHONE_PREFIX = re.compile(r'label ta_r">\+(.*?)<')
RE_PHONE_POSTFIX = re.compile(r'phone_postfix">.*?(\d+).*?<')




def search_re(reg, string):
    """ Поиск по регулярке """
    s = reg.search(string)

    if s:
        groups = s.groups()
        return groups[0]


def cookie_from_dict(d):
    return Cookie(**d)


def set_cookies_from_list(cookie_jar, l):
    for cookie in l:
        cookie_jar.set_cookie(cookie_from_dict(cookie))

HTTP_COOKIE_ARGS = [
    'version', 'name', 'value',
    'port', 'port_specified',
    'domain', 'domain_specified',
    'domain_initial_dot',
    'path', 'path_specified',
    'secure', 'expires', 'discard', 'comment', 'comment_url', 'rest', 'rfc2109'
]


def cookie_to_dict(cookie):
    cookie_dict = {
        k: v for k, v in six.iteritems(cookie.__dict__) if k in HTTP_COOKIE_ARGS
    }

    cookie_dict['rest'] = cookie._rest
    cookie_dict['expires'] = None

    return cookie_dict

def cookies_to_list(cookies):
    return [cookie_to_dict(cookie) for cookie in cookies]

def clear_string(s):
    if s:
        return s.strip().replace('&nbsp;', '')

def code_from_number(prefix, postfix, number):
    prefix_len = len(prefix)
    postfix_len = len(postfix)

    if number[0] == '+':
        number = number[1:]

    if (prefix_len + postfix_len) >= len(number):
        return

    # Сравниваем начало номера
    if number[:prefix_len] != prefix:
        return

    # Сравниваем конец номера
    if number[-postfix_len:] != postfix:
        return

    return number[prefix_len:-postfix_len]


class VkApi(object):
    """
    :param login: Логин ВКонтакте (лучше использовать номер телефона для
        автоматического обхода проверки безопасности)
    :type login: str

    :param password: Пароль ВКонтакте (если пароль не передан, то будет
        попытка использовать сохраненные данные)
    :type password: str

    :param token: access_token
    :type token: str

    :param auth_handler: Функция для обработки двухфакторной аутентификации,
        должна возвращать строку с кодом и
        булево значение, означающее, стоит ли запомнить
        это устройство, для прохождения аутентификации.
    :param captcha_handler: Функция для обработки капчи, см. :func:`captcha_handler`
    :param config: Класс для сохранения настроек
    :type config: :class:`jconfig.base.BaseConfig`
    :param config_filename: Расположение config файла для :class:`jconfig.config.Config`

    :param api_version: Версия API
    :type api_version: str

    :param app_id: app_id Standalone-приложения
    :type app_id: int

    :param scope: Запрашиваемые права, можно передать строкой или числом.
        См. :class:`VkUserPermissions`
    :type scope: int or str

    :param client_secret: Защищенный ключ приложения для Client Credentials Flow
        авторизации приложения (https://vk.com/dev/client_cred_flow).
        Внимание: Этот способ авторизации устарел, рекомендуется использовать
        сервисный ключ из настроек приложения.


    `login` и `password` необходимы для автоматического получения токена при помощи
    Implicit Flow авторизации пользователя и возможности работы с веб-версией сайта
    (включая :class:`vk_api.audio.VkAudio`)

    :param session: Кастомная сессия со своими параметрами(из библиотеки requests)
    :type session: :class:`requests.Session`
    """

    RPS_DELAY = 0.34  # ~3 requests per second

    def __init__(self, login=None, password=None,
                 config=jconfig.Config, config_filename='vk_config.v2.json', session=None):

        self.login = login
        self.password = password
        self.storage = config(self.login, filename=config_filename)

        self.http = session or requests.Session()
        if not session:
            self.http.headers.update({
                'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                              'Gecko/20100101 Firefox/52.0'
            })

        self.logger = logging.getLogger('vk_api')
        self.logger.setLevel(logging.INFO)

    @property
    def _sid(self):
        return (
            self.http.cookies.get('remixsid') or
            self.http.cookies.get('remixsid6')
        )

    def auth(self):
        set_cookies_from_list(
            self.http.cookies,
            self.storage.setdefault('cookies', [])
        )

        self._vk_login()


    def _vk_login(self, captcha_sid=None, captcha_key=None):

        self.http.cookies.clear()

        # Get cookies
        response = self.http.get('https://vk.com/')

        values = {
            'act': 'login',
            'role': 'al_frame',
            '_origin': 'https://vk.com',
            'utf8': '1',
            'email': self.login,
            'pass': self.password,
            'lg_h': search_re(RE_LOGIN_HASH, response.text)
        }

        if captcha_sid and captcha_key:
            self.logger.info(
                'Using captcha code: {}: {}'.format(
                    captcha_sid,
                    captcha_key
                )
            )

            values.update({
                'captcha_sid': captcha_sid,
                'captcha_key': captcha_key
            })

        response = self.http.post('https://login.vk.com/', values)

        if 'onLoginCaptcha(' in response.text:
            self.logger.warning('Captcha code is required')
            return

        if 'onLoginReCaptcha(' in response.text:
            self.logger.warning('Captcha code is required (recaptcha)')
            return

        if 'onLoginFailed(4' in response.text:
            raise ValueError('Bad password')

        if 'act=authcheck' in response.text:
            self.logger.error('Two factor is required')
            return

        if self._sid:
            self.logger.info('Got remixsid')

            self.storage.cookies = cookies_to_list(self.http.cookies)
            self.storage.save()
        else:
            raise ValueError(
                'Unknown error. Please send bugreport to vk_api@python273.pw'
            )

        response = self._pass_security_check(response)

        if 'act=blocked' in response.url:
            raise ValueError('Account is blocked')


    def _pass_security_check(self, response=None):
        """ Функция для обхода проверки безопасности (запрос номера телефона)

        :param response: ответ предыдущего запроса, если есть
        """

        self.logger.info('Checking security check request')

        if response is None:
            response = self.http.get('https://vk.com/settings')

        if 'security_check' not in response.url:
            self.logger.info('Security check is not required')
            return response

        phone_prefix = clear_string(search_re(RE_PHONE_PREFIX, response.text))
        phone_postfix = clear_string(
            search_re(RE_PHONE_POSTFIX, response.text))

        code = None
        if self.login and phone_prefix and phone_postfix:
            code = code_from_number(phone_prefix, phone_postfix, self.login)

        if code:
            number_hash = search_re(RE_NUMBER_HASH, response.text)

            values = {
                'act': 'security_check',
                'al': '1',
                'al_page': '3',
                'code': code,
                'hash': number_hash,
                'to': ''
            }

            response = self.http.post('https://vk.com/login.php', values)

            if response.text.split('<!>')[4] == '4':
                return response

        if phone_prefix and phone_postfix:
            raise ValueError(phone_prefix, phone_postfix)

        raise ValueError()

    def check_sid(self):
        """ Проверка Cookies remixsid на валидность """

        self.logger.info('Checking remixsid...')

        if not self._sid:
            self.logger.info('No remixsid')
            return

        response = self.http.get('https://vk.com/feed2.php').json()

        if response['user']['id'] != -1:
            self.logger.info('remixsid is valid')
            return response

        self.logger.info('remixsid is not valid')



vk_session = VkApi('TELEPHONE', 'PASSWORD')
vk_session.auth()
print(vk_session.http.cookies.get('remixsid'))

COOKIE_STRING = f'remixsid={vk_session.http.cookies.get("remixsid")}'

def get_cookie():
    res = requests.post('https://login.vk.com/?act=login', data=str('act=login&role=al_frame&expire=&recaptcha=&captcha_sid=&captcha_key=&_origin=https%3A%2F%2Fvk.com&ip_h=cfef87c0ea2509e8cd&lg_h=e411a66e4de0b8a269&ul=&email=%2B79214161314&pass=uaz469193318416'))
    print(res)


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
            print('Got {} songs.'.format(len(songs)))


            return songs, playlist['nextOffset'], playlist['totalCount']

    cnt = 1
    songs = []
    offset = 0
    while len(songs) < cnt:
        songs_, next_offset, cnt = get_songs(offset)
        offset = next_offset
        songs = songs + songs_

    print('Totally Got {} songs. I.E.:'.format(len(songs)))
    pprint(songs[:10])
    return songs

get_users_songs(17278900)




