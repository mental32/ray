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

_PLAYER_URL   = _PROD_06_PERSONA + '/persona/api/public/account/lookup?q={username}'
_STATUS_URL   = _PROD_06_LIGHTSWITCH + '/lightswitch/api/service/bulk/status?serviceId=Fortnite'
_FRIENDS_URL  = _PROD_06_FRIENDS + '/friends/api/public/friends/{account_id}'

_NEWS_URL     = _PROD_07 + '/content/api/pages/fortnite-game'

_BR_URL       = _PROD_11 + '/fortnite/api/stats/accountId/{account_id}/bulk/window/{timeframe}'
_STORE_URL    = _PROD_11 + '/fortnite/api/storefront/v2/catalog?rvn={}'
_LDRBRD_URL   = _PROD_11 + '/fortnite/api/leaderboards/type/global/stat/br_placetop1_{}_m0{}/window/weekly'

_PN_URL       = _EPIC_GAMES + '/fortnite/api/blog/getPosts'
_BLOG_URL     = _EPIC_GAMES + '/fortnite/{}/news/{}'
