#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''
@author:wanglei1
'''


import json
import os


class JsonConf:

    '''
    json configs
    '''

    @staticmethod
    def store(data, file_name):
        with open(file_name, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    @staticmethod
    def load(file_name):
        if not os.path.exists(file_name):
            with open(file_name, 'w') as json_file:
                pass
        with open(file_name) as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            return data

    @staticmethod
    def set(data_dict):
        json_obj = JsonConf.load()
        for key in data_dict:
            json_obj[key] = data_dict[key]
        JsonConf.store(json_obj)
        print(json.dumps(json_obj, indent=4))


if __name__ == "__main__":
    data = {"a": " 1", "f": "100", "b": "3000"}
    file_name = 'configs.json'
    JsonConf.set(data, file_name)