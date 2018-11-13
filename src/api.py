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

    def get_user_id(self, username):
        user_data = self.session.get('{}{}/?__a=1'.format(INSTAGRAM_URL, username)).content
        return json.loads(user_data)['graphql']['user']['id']

    def update_ig_gis_header(self, params):
        self.session.headers.update({
            'x-instagram-gis': self.get_ig_gis(
                self.rhx_gis,
                params
            )
        })

    def get_ig_gis(self, rhx_gis, params):
        return hashlib.md5(rhx_gis + ":" + params).hexdigest()

    def get_user_posts_by_username(self, username):
        user_id = self.get_user_id(username)
        self.get_user_posts_by_id(user_id)

    def get_user_posts_by_id(self, user_id, from_post = '', count = 12):
        ''' Basic API calling, which defaultly called,
            user_id = the requested profile user_id
            from_post = api fetching posts always releated from a post id

            the QUERY_MEDIA_VARS "first" param is setted to 12, because api defaultly request 12 posts, max 50
        '''
        params = QUERY_MEDIA_VARS.format(user_id, count, from_post)
        self.update_ig_gis_header(params)
        return self.session.get(QUERY_MEDIA_URL.format(params)).content

    def get_user_some_posts_by_id(self, user_id, count):
        posts = []
        has_next_page = True

        if count <= 50:
            data = self.get_user_posts_by_id(user_id, '', count)
        else:
            while count != 0 and has_next_page is True:
                data = self.get_user_posts_by_id(user_id, 50)
                #has_next_page = data[....] To be continued

        return data 

    def get_user_all_posts_by_id(self, user_id):
        after = ''
        has_next_page = True
        data = []

        while (has_next_page == True):
            #self.get_user_posts_by_id(


            has_next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            after = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            data.append(['data']['user']['edge_owner_to_timeline_media']['edges'])

            time.sleep(1)

        return data
