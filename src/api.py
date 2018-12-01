from utils import *
from constants import *
import time
import requests
import json

# -*- coding: utf-8 -*-


class InstagramApi:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.login(username, password)

    def set_headers(self):
        content = self.session.get(INSTAGRAM_URL).content

        header =  {'x-csrftoken'        : return_raw_content_data(content)["csrf_token"],
                'x-requested-with'   : 'XMLHttpRequest',
                'cookie'             : 'ig_cb=1',
                'X-Instagram-AJAX'   : '1',
                'Accept'             : '*/*',
                'User-Agent'         : USER_AGENT,
                'Accept-Language'    : 'en-US',
                'Accept-Encoding'    : 'gzip, deflate',
                'Connection'         : 'close',
                'Referer'            : 'https://www.instagram.com',
                'Authority'          : 'www.instagram.com',
                'Origin'             : 'https://www.instagram.com',
                'Content-Type'       : 'application/x-www-form-urlencoded'
                }

        self.rhx_gis = return_raw_content_data(content)["rhx_gis"]
        self.session.headers.update(header)

    def login(self, username, password):
        self.set_headers()

        data = {'username'    : username,
                'password'    : password}

        login_response = self.session.post(
                '{}accounts/login/ajax/'.format(INSTAGRAM_URL),
                data    = data,
                allow_redirects = True)

        if (login_response.status_code != 200):
            raise Exception("Login error with {}".format(username))

        self.session.headers.update({'x-csrftoken' : login_response.cookies['csrftoken']})
        self.cookies = login_response.cookies

    def update_ig_gis_header(self, params):
        self.session.headers.update({
            'x-instagram-gis': self.get_ig_gis(
                self.rhx_gis,
                params
            )
        })

    def get_ig_gis(self, rhx_gis, params):
        return hashlib.md5(rhx_gis + ":" + params).hexdigest()

    def get_user_id(self, username):
        ''' Basic API calling
            username = username of target instagram user
            return data will be the ID of the target user
        '''
        user_data = self.session.get('{}{}/?__a=1'.format(INSTAGRAM_URL, username)).content
        return json.loads(user_data)['graphql']['user']['id']

    def get_user_posts_by_id(self, user_id, from_post = '', count = 12):
        ''' Basic API calling, which defaultly called,
            user_id = the requested profile user_id
            from_post = api fetching posts always releated from a post id

            the QUERY_MEDIA_VARS "first" param is setted to 12, because api defaultly request 12 posts, max 50
        '''
        params = QUERY_MEDIA_VARS.format(user_id, count, from_post)
        self.update_ig_gis_header(params)
        return self.session.get(QUERY_MEDIA_URL.format(params)).content

    def get_post_data_by_shortcode(self, shortcode):
        ''' Basic API calling
            shortcode = shortcode of the targeted post
            return data will be all available information from the post
        '''
        params = POST_MEDIA_VARS.format(shortcode)
        self.update_ig_gis_header(params)
        return self.session.get(POST_MEDIA_URL.format(params)).content
