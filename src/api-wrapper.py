from api import InstagramApi 


class InstagramApiWrapper:
    def __init__(self):
        self.api = InstagramApi()
        self.api.login()


    def get_user_posts_by_username(self, username):
        user_id = self.api.get_user_id(username)
        return self.api.get_user_posts_by_id(user_id)
