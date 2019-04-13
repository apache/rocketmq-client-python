#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /*
# * Licensed to the Apache Software Foundation (ASF) under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The ASF licenses this file to You under the Apache License, Version 2.0
# * (the "License"); you may not use this file except in compliance with
# * the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */

import __init__
from librocketmqclientpython import *
import time
import sys
import RocketMQBaseClient


'''
ConsumeClient
'''


class ConsumeClient(object):

    def __init__(self, name_server, group, topic_tag_list):
        baseClient = RocketMQBaseClient.BaseClient(name_server, group)
        self.consumer = baseClient.get_consumer_instance()
        self.topic_tag_list = topic_tag_list

    def startup_consumer(self, callback_method, thread_count, max_batch_size, arg):
        self.set_consumer_thread_count(thread_count)
        for topic_tag in self.topic_tag_list:
            topic = str(topic_tag.get("topic"))
            tags = str(topic_tag.get("tags"))
            self.add_subscribe(topic, tags)
        self.set_consumer_message_batch_size(max_batch_size)
        self.register_message_callback(callback_method, arg)
        self.start_consumer_pure()

    def add_subscribe(self, topic, tags):
        Subscribe(self.consumer, topic, tags)

    def start_consumer_pure(self):
        StartPushConsumer(self.consumer)

    def register_message_callback(self, callback_method, arg):
        RegisterMessageCallback(self.consumer, callback_method, arg)

    def set_consumer_thread_count(self, thread_count):
        SetPushConsumerThreadCount(self.consumer, thread_count)

    def set_consumer_message_batch_size(self, max_batch_size):
        SetPushConsumerMessageBatchMaxSize(self.consumer, max_batch_size)

    def set_consumer_instance_name(self, instance_name):
        SetPushConsumerInstanceName(self.consumer, instance_name)

    def shutdown_push_consumer(self):
        ShutdownPushConsumer(self.consumer)

    def destroy_push_consumer(self):
        DestroyPushConsumer(self.consumer)

    @staticmethod
    def get_message_topic(message):
        return GetMessageTopic(message)

    @staticmethod
    def get_message_tags(message):
        return GetMessageTags(message)

    @staticmethod
    def get_message_body(message):
        return GetMessageBody(message)

    @staticmethod
    def get_message_id(message):
        return GetMessageId(message)

    @staticmethod
    def get_message_keys(message):
        return GetMessageKeys(message)

    @staticmethod
    def get_message_property(message, key):
        return GetMessageProperty(message, key)