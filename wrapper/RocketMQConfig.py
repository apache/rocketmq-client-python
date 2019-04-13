#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils.config_util as config_util

'''
RocketMQConfg
'''


class Config(object):

  def __init__(self):
    config_dict = config_util.JsonConf.load('configs/config.json')
    self.name_server = config_dict.get("name_server")
    self.consumer_config_dict = config_dict.get("consumer")
    self.producer_config_dict = config_dict.get("producer")

  def get_consumer_config(self):
    return self.consumer_config_dict

  def get_producer_config(self):
    return self.producer_config_dict

  def get_name_server(self):
    return self.name_server


