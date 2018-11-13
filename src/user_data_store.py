

class UserDataStore:
    def set_rhx_gis(self, gis):
        self.gis = gis

    def get_rhx_gis(self):
        return self.gis

    def set_csrf_token(self, csrf):
        self.csrf_token = csrf

    def get_csrf_token(self):
        return self.csrf_token
