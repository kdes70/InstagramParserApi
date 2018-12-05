from api import InstagramApi 
import time
import post_data_helper 
import json


class InstagramApiWrapper:
    '''Preferably used, as self.api give interface to basic api'''
    def __init__(self, username, password, login = True):
        self.api = InstagramApi(username, password, login)

    def get_user_posts_with_location(self, username, count):
        data = dict()

        user_id = self.api.get_user_id(username)
        posts = json.loads(self.api.get_user_posts_by_id(user_id))["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for post in posts:
            data["post"] = self.get_post_data_by_keys(post["node"]["shortcode"], ['location'])


        print data

    def get_post_data_by_keys(self, shortcode, array_keys):
        ''' Wrapped api calling for getting post's data by desirable keys
            Current implementation is hacky #TODO fix it.
            Currently supported keys: 
                            * location
                            * url
                            * author_username
                            * author_full_name
                            * text
            return: dictionary with selected keys, and found values
        '''
        found_data = dict()

        post_data = self.api.get_post_data_by_shortcode(shortcode)
        post_data = json.loads(post_data)
        for key in array_keys:
            method_to_call = getattr(post_data_helper, 'get_post_{}'.format(key))
            found_data[key] = method_to_call(post_data)

        return found_data

    def get_user_posts_by_username(self, username):
        user_id = self.api.get_user_id(username)
        return self.api.get_user_posts_by_id(user_id)

    def get_user_some_posts_by_id(self, user_id, count):
        posts = []
        has_next_page = True

        if count <= 50:
            data = self.get_user_posts_by_id(user_id, '', count)
        else:
            while count != 0 and has_next_page is True:
                data = self.get_user_posts_by_id(user_id, 50)
                #TODO: implement it
                #has_next_page = data[....] To be continued

        return data 

    def get_user_all_posts_by_id(self, user_id, time_out = 2, just_edges = True):
        ''' Same behaviour as you scrolling down the user page
            With edges flag you could define if you just want the ['edges'] 
            to be scraped, to not contain the whole response data to be more useful
        '''

        after = ''
        has_next_page = True
        data = []

        while (has_next_page == True):
            json_data = json.loads(self.api.get_user_posts_by_id(user_id, after, 50))
            has_next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            after = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            if just_edges = True:
                data.append(json_data['data']['user']['edge_owner_to_timeline_media']['edges'])
            else:
                data.append(json_data)

            time.sleep(time_out)

        return data
