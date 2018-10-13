import asyncio
import json

import aiohttp

_CLIENT_LAUNCHER_TOKEN = 'MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y='
_FORTNITE_CLIENT_TOKEN = 'ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ='

_PROD_03 = 'https://account-public-service-prod03.ol.epicgames.com'
_PROD_06_PERSONA = 'https://persona-public-service-prod06.ol.epicgames.com'
_PROD_06_FRIENDS = 'https://friends-public-service-prod06.ol.epicgames.com'
_PROD_06_LIGHTSWITCH = 'https://lightswitch-public-service-prod06.ol.epicgames.com'
_PROD_07 = 'https://fortnitecontent-website-prod07.ol.epicgames.com'
_PROD_11 = 'https://fortnite-public-service-prod11.ol.epicgames.com'
_EPIC_GAMES = 'https://www.epicgames.com'

_TOKEN_URL    = _PROD_03 + '/account/api/oauth/token'
_EXCHANGE_URL = _PROD_03 + '/account/api/oauth/exchange'
_ACCOUNT_URL  = _PROD_03 + '/account/api/public/account?accountId={account_id}'

_PLAYER_URL   = _PROD_06_PERSONA + '/persona/api/public/account/lookup?q={}'
_STATUS_URL   = _PROD_06_LIGHTSWITCH + 'lightswitch/api/service/bulk/status?serviceId=Fortnite'
_FRIENDS_URL  = _PROD_06_FRIENDS + '/friends/api/public/friends/{}'

_NEWS_URL     = _PROD_07 + '/content/api/pages/fortnite-game'

_BR_URL       = _PROD_11 + '/fortnite/api/stats/accountId/{account_id}/bulk/window/alltime'
_STORE_URL    = _PROD_11 + '/fortnite/api/storefront/v2/catalog?rvn={}'
_LDRBRD_URL   = _PROD_11 + '/fortnite/api/leaderboards/type/global/stat/br_placetop1_{}_m0{}/window/weekly'

_PN_URL       = _EPIC_GAMES + '/fortnite/api/blog/getPosts'
_BLOG_URL     = _EPIC_GAMES + '/fortnite/{}/news/{}'


class HTTPClient:
    def __init__(self, email_account, password, loop=None):
        self._loop = loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=loop)

        self._username = email_account
        self._password = password

        self.launcher_token = _CLIENT_LAUNCHER_TOKEN
        self.fortnite_token = _FORTNITE_CLIENT_TOKEN

        self._access_token = None
        self._refresh_token = None

        self._access_expires_in = None
        self._refresh_expires_in = None

    @property
    def session(self):
        return self._session

    async def _authenticate(self):

        # Initialize headers and data fields.

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

        self._access_token = resp['access_token']
        self._refresh_token = resp['refresh_token']

        self._access_expires_in = resp['expires_in']
        self._refresh_expires_in = resp['refresh_expires']

    async def request(self, method, url, **kwargs):
        '''Performs a HTTP request, returns the response data'''

        if self._access_token is None:
            await self._authenticate()

        async with self._session.request(method, url, **kwargs) as resp:
            return await resp.json()
