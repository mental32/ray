import asyncio
import json
from urllib.parse import quote

import aiohttp

from .constants import (
    _TOKEN_URL,
    _EXCHANGE_URL,
    _ACCOUNT_URL,
    _PLAYER_URL,
    _STATUS_URL,
    _FRIENDS_URL,
    _BR_URL,
)

_CLIENT_LAUNCHER_TOKEN = 'MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y='
_FORTNITE_CLIENT_TOKEN = 'ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ='


class HTTPClient:
    __slots__ = ('_loop', '_session', '_username', '_password', '_auth_locked', '_access_token', '_refresh_token', '_access_expires_in', '_refresh_expires_in', '_account_id')

    launcher_token = _CLIENT_LAUNCHER_TOKEN
    fortnite_token = _FORTNITE_CLIENT_TOKEN

    def __init__(self, email_account, password, loop=None):
        self._loop = loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=loop)

        self._username = email_account
        self._password = password

        # Lock to prevent recursive call inside HTTPClient._authenticate
        self._auth_locked = False

        self._access_token = None
        self._refresh_token = None
        self._access_expires_in = None
        self._refresh_expires_in = None
        self._account_id = None

    def __del__(self):
        self.__close()

    def __close(self):
        session = self._session
        if not session.closed:
            if session._connector_owner:
                session._connector.close()
        session._connector = None

    @property
    def session(self):
        return self._session

    @property
    def account_id(self):
        return self._account_id

    @property
    def headers(self):
        return {'Authorization': 'bearer %s' % self._access_token}

    async def _authenticate(self):
        # prevent recursive call.
        self._auth_locked = True

        # Initialize header and data fields.
        headers = {
            'Authorization': 'basic %s' % self.launcher_token
        }

        data = {
            'grant_type': 'password',
            'username': self._username,
            'password': self._password,
            'includePerms': True
        }

        # Get bearer token using username and password
        resp = await self.request('POST', _TOKEN_URL, headers=headers, data=data)

        # Exchange bearer token for an "exchange code".
        headers['Authorization'] = 'bearer %s' % resp['access_token']
        resp = await self.request('GET', _EXCHANGE_URL, headers=headers)

        # Use fortnite client token and exchange code to request
        # an access token and a refresh token.
        headers['Authorization'] = 'basic %s' % self.fortnite_token

        data.pop('username')
        data.pop('password')

        data['grant_type'] = 'exchange_code'
        data['token_type'] = 'egl'
        data['exchange_code'] = resp['code']

        resp = await self.request('POST', _TOKEN_URL, headers=headers, data=data)

        # populate our access_token, refresh_token and expiry data
        self._access_token = resp['access_token']
        self._refresh_token = resp['refresh_token']

        self._access_expires_in = resp['expires_in']
        self._refresh_expires_in = resp['refresh_expires']

        self._account_id = resp['account_id']

        # release lock
        self._auth_locked = False

    async def request(self, method, url, **kwargs):
        '''Performs a HTTP request, returns the response data'''

        if self._access_token is None and not self._auth_locked:
            await self._authenticate()

        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers

        async with self._session.request(method, url, **kwargs) as resp:
            return await resp.json()

    # Authless methods

    def get_server_status(self):
        async def _inner():
            return await (await self._session.request('GET', _STATUS_URL)).json()
        return _inner()

    # Contextual methods

    def get_me(self):
        return self.get_user_from_id(self._account_id)

    def get_friends(self):
        return self.get_player_friends(self._account_id)

    # General methods

    def get_player(self, username):
        return self.request('GET', _PLAYER_URL.format(username=quote(username)))

    def get_player_friends(self, account_id):
        return self.request('GET', _FRIENDS_URL.format(account_id=account_id))

    def get_battle_royale_stats(self, account_id=None, timeframe='alltime'):
        account_id = account_id or self.account_id
        return self.request('GET', _BR_URL.format(account_id=account_id, timeframe=timeframe))

    def get_users_from_ids(self, *account_ids):
        async def _inner():
            data = self.request('GET', _ACCOUNT_URL.format(account_id='&accountId='.join(account_ids)))

            if not isinstance(data, list):
                data = list(data)

            return data

        return _inner()

    def get_user_from_id(self, account_id):
        async def _inner():
            data = await self.request('GET', _ACCOUNT_URL.format(account_id=account_id))

            if isinstance(data, list):
                return data[0]
            return data

        return _inner()
