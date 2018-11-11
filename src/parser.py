from utils import *
import time
from constants import *
import requests
import json


class Parser:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.set_headers()
        self.login(username, password)

    def set_headers(self):
        content = self.session.get(INSTAGRAM_URL).content

        headers = {'x-csrftoken'        : get_csrf_token(content),
                   'x-requested-with'   : 'XMLHttpRequest',
                   'cookie'             : 'ig_cb=1',
                   'X-Instagram-AJAX'   : '1'}

        self.session.headers.update(headers)

    def login(self, username, password):
        data = {'username'    : username,
                'password'    : password,
                'queryParams' : "{}"}

        login_response = self.session.post(
                '{}accounts/login/ajax/'.format(INSTAGRAM_URL),
                data    = data)

        self.session.headers.update({'x-csrftoken' : login_response.cookies['csrftoken']})

    def get_user_id(self, username):
        user_data = self.session.get('{}{}/?__a=1'.format(INSTAGRAM_URL, username)).content
        json_data = json.loads(user_data)
        return json_data['graphql']['user']['id']

    def get_user_posts_by_username(self, username):
        user_id = self.get_user_id(username)
        self.get_user_posts_by_id(user_id)


    def get_user_profile_page_by_id(self, user_id):
        variable_filter= {"user_id"                   : user_id,
                          "include_chaining"          :'true',
                          "include_reel"              :'true',
                          "include_suggested_users"   :'false',
                          "include_logged_out_extras" :'false',
                          "include_highlight_reels"   :'true'}

        data = {'query_hash' : PROFILE_REQUEST_HASH,
                'variables'  : json.dumps(variable_filter)}

        response = self.session.get(INSTAGRAM_API_URL, params = data).content
        return json.loads(response)

    def get_user_posts_by_id(self, user_id):
        self.get_user_profile_page_by_id(user_id)

        after = ''
        has_next_page = True
        data = []

        while (has_next_page == True):
            variable_filter= {"id"    : user_id,
                              "first" :'10',
                              "after" : after}

            data = {'query_hash' : MEDIA_REQUEST_HASH,
                    'variables'  : json.dumps(variable_filter)}

            response = self.session.get(INSTAGRAM_API_URL, params = data)
            json_data = json.loads(response.content)

            has_next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            after = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            data.append(['data']['user']['edge_owner_to_timeline_media']['edges'])

            time.sleep(1)

        return data
