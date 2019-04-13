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
ProduceClient
'''


class ProduceClient(object):

    def __init__(self, name_server, group, topic):
        baseClient = RocketMQBaseClient.BaseClient(name_server, group)
        self.producer = baseClient.get_producer_instance()
        self.topic = topic

    def start_producer(self):
        StartProducer(self.producer)

    def shutdown_producer(self):
        ShutdownProducer(self.producer)

    def destroy_producer(self):
        DestroyProducer(self.producer)

    def create_message(self, body, key, tag):
        message = self.create_message_pure()
        self.set_message_body(message, str(body))
        self.set_message_keys(message, str(key))
        self.set_message_tags(message, str(tag))
        return message

    def create_message_pure(self):
        return CreateMessage(self.topic)

    def send_message_sync(self, message):
        result = SendMessageSync(self.producer, message)
        return result

    def send_message_oneway(self, message):
        result = SendMessageOneway(self.producer, message)
        return result

    def send_message_orderly(self, message, auto_retry_times, arg, callback_method):
        result = SendMessageOrderly(self.producer, message, auto_retry_times, arg, callback_method)
        return result

    def set_producer_session_credentials(self, access_key, secret_key, channel):
        SetProducerSessionCredentials(self.producer, access_key, secret_key, channel)

    def set_producer_nameserver_address(self, namesrv_address):
        SetProducerNameServerAddress(self.producer, namesrv_address)

    def set_producer_instance_name(self, instance_name):
        SetProducerInstanceName(self.producer, instance_name)

    def set_message_body(self, message, body):
        return SetMessageBody(message, body)

    def set_message_keys(self, message, keys):
        return SetMessageKeys(message, keys)

    def set_message_tags(self, message, tags):
        return SetMessageTags(message, tags)

    def set_message_property(self, message, key, value):
        return SetMessageProperty(message, key, value)

    def resolve_result(self, result):
        if not result:
            return None, None, None
        return result.GetMsgId(), result.offset, result.sendStatus

    def destory_message(self, message):
        DestroyMessage(message)