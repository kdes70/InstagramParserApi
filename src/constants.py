INSTAGRAM_URL = 'https://instagram.com/'
INSTAGRAM_API_URL = 'https://www.instagram.com/graphql/query/'
PROFILE_REQUEST_HASH = '7c16654f22c819fb63d1183034a5162f'
MEDIA_REQUEST_HASH = 'f412a8bfd8332a76950fefc1da5785ef'
REQUEST_HASH = '0f318e8cfff9cc9ef09f88479ff571fb'
REQUEST_LOGIN_HASH = '60b755363b5c230111347a7a4e242001'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36'

QUERY_MEDIA_VARS = '{{"id":"{0}","first":"{1}","after":"{2}"}}'
QUERY_MEDIA_URL  = INSTAGRAM_URL + 'graphql/query/?query_hash=66eb9403e44cc12e5b5ecda48b667d41&variables={0}'

POST_MEDIA_VARS = '{{"shortcode":"{0}","child_comment_count":0,"fetch_comment_count":0,"parent_comment_count":0,"has_threaded_comments":false}}'
POST_MEDIA_URL = INSTAGRAM_URL + 'graphql/query/?query_hash=49699cdb479dd5664863d4b647ada1f7&variables={0}'
