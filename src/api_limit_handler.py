import os
import json

class ApiLimitHandler:
    ''' Handles the situation when fetching posts, saves the cursor, and
        target user scraped again, it will skip parsed post
        Method of way of working: JSON data store, with user, first scraped ID, last scraped ID

        {'users' : {'id' : user_id,
                    'first_scraped' : first_scraped(string),
                    'last_scraped'  : last_scraped(string),
                    'is_last'       : is_last(bool)}

        Method:
            -> read file
            -> append new data to current data
            -> write data
    '''
    DATA_FILE = '{}/data'.format(os.getcwd()) 

    @staticmethod
    def save_current_pointer(json_object):
        self.__load_data()

    @staticmethod
    def __load_data():
        if !os.path.exists(DATA_FILE):
            os.mkdir(os.path.dirname(os.path.abspath(DATA_FILE)))
            with open(DATA_FILE, 'w+'): pass
        with open(DATA_FILE, 'r') as data:
            return data.read()

    @staticmethod
    def __append_new_to_current(current_data, new_data):
        data = json.loads(current_data)
        data['users'].extend(new_data)
        return data

    @staticmethod
    def __save_data(data):
        with open(DATA_FILE, 'w') as data_file:
            data_file.write(data_file)
