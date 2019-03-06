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

import unittest
import json
import time
from librocketmqclientpython import \
    CreateProducer, SetProducerNameServerAddress, StartProducer, \
    CreateMessage, SetMessageBody, SetMessageTags, SendMessageSync, SetMessageProperty, SetMessageKeys, DestroyMessage, \
    CreatePushConsumer, SetPushConsumerNameServerAddress, SetPushConsumerThreadCount, \
    Subscribe, RegisterMessageCallback, StartPushConsumer, ShutdownPushConsumer, DestroyPushConsumer, \
    GetMessageTopic, GetMessageTags, GetMessageBody, GetMessageId, GetMessageKeys, GetMessageProperty, SendMessageOrderly, \
    DestroyProducer
from config import name_srv, topic, topic_orderly, tag, key, consumer_group, consumer_group_orderly
from utils import output, randstr


class Test2ConsumeMessages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = CreateProducer('TestProducer')
        SetProducerNameServerAddress(cls.producer, name_srv)
        StartProducer(cls.producer)

    @classmethod
    def tearDownClass(cls):
        DestroyProducer(cls.producer)

    def send_message(self, data, orderly=False):
        msg = CreateMessage(data['topic'])
        SetMessageBody(msg, data['body'])
        SetMessageTags(msg, data['tag'])
        SetMessageKeys(msg, data['key'])
        SetMessageProperty(msg, 'id', data['map_id'])
        SetMessageProperty(msg, 'name', data['map_name'])

        if orderly:
            SendMessageOrderly(self.producer, msg, 1, None, lambda size, msg, arg: 0)
        else:
            SendMessageSync(self.producer, msg)
        DestroyMessage(msg)

        output('sent: ' + json.dumps(data))

    def init_consumer(self, group, topic, tag, callback):
        consumer = CreatePushConsumer(group)
        SetPushConsumerNameServerAddress(consumer, name_srv)
        SetPushConsumerThreadCount(consumer, 1)
        Subscribe(consumer, topic, tag)
        RegisterMessageCallback(consumer, callback, None)
        StartPushConsumer(consumer)
        return consumer

    def shutdown_consumer(self, consumer):
        ShutdownPushConsumer(consumer)
        DestroyPushConsumer(consumer)

    def check_message(self, msg, send):
        data = {
            'msg_id': GetMessageId(msg),
            'topic': GetMessageTopic(msg),
            'body': GetMessageBody(msg),
            'tag': GetMessageTags(msg),
            'key': GetMessageKeys(msg),
            'map_id': GetMessageProperty(msg, 'id'),
            'map_name': GetMessageProperty(msg, 'name'),
        }
        output('message: ' + ','.join(key + '=' + value for [key, value] in data.items()))

        self.assertIsInstance(data['body'], str)
        return 0

    def test_one_consumer(self):
        send = dict(
            topic=topic,
            body=randstr(6),
            tag=tag,
            key=key,
            map_id=randstr(6),
            map_name=randstr(6),
        )
        self.send_message(send)

        got_msg = dict(value=False)

        def callback(msg, args):
            if not got_msg['value']:
                got_msg['value'] = True
                self.check_message(msg, send)
            return 0
        consumer = self.init_consumer(consumer_group, send['topic'], send['tag'], callback)

        i = 1
        while i <= 20:
            output('clock: ' + str(i))
            i += 1
            if got_msg['value']:
                break
            time.sleep(1)

        self.shutdown_consumer(consumer)
        output("Consumer Down....")

        self.assertEqual(got_msg['value'], True)

    def test_orderly_consumer(self):
        send = dict(
            topic=topic_orderly,
            body=randstr(6),
            tag='*',
            key=key,
            map_id=randstr(6),
            map_name=randstr(6),
        )
        self.send_message(send, orderly=True)

        got_msg = dict(value=False)

        def callback(msg, args):
            if not got_msg['value']:
                got_msg['value'] = True
                self.check_message(msg, send)
            return 0
        consumer = self.init_consumer(consumer_group_orderly, send['topic'], send['tag'], callback)

        i = 1
        while i <= 20:
            output('clock: ' + str(i))
            i += 1
            if got_msg['value']:
                break
            time.sleep(1)

        self.shutdown_consumer(consumer)
        output("Consumer Down....")

        self.assertEqual(got_msg['value'], True)
