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
from utils import timestr, output
from librocketmqclientpython import CreateProducer, SetProducerNameServerAddress, StartProducer, \
    CreateMessage, SetMessageBody, SendMessageSync, DestroyMessage, SendResult, CSendStatus, \
    SetMessageProperty, SetMessageTags, SetMessageKeys, SendMessageOneway, SetDelayTimeLevel, SendMessageOrderly, \
    DestroyProducer
from config import name_srv, topic, topic_orderly, tag, key


class Test1SendMessages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = CreateProducer('TestProducer')
        cls.set_ns_result = SetProducerNameServerAddress(cls.producer, name_srv)
        cls.start_result = StartProducer(cls.producer)

    @classmethod
    def tearDownClass(cls):
        DestroyProducer(cls.producer)

    def send_message_sync(self, sending_info='', set_message=None):
        for i in range(5):
            output('sending sync ' + sending_info + '... ', end='')

            msg = CreateMessage(topic)
            SetMessageBody(msg, 'hi rmq, now is ' + timestr())
            if set_message:
                set_message(msg)

            result = SendMessageSync(self.producer, msg)
            msg_id = result.GetMsgId()
            DestroyMessage(msg)

            output('done, msg_id=' + msg_id)

            self.assertIsInstance(result, SendResult)
            # self.assertEqual(result.sendStatus, CSendStatus.E_SEND_OK)
            self.assertIsInstance(msg_id, str, 'message id should be a string')

    def send_message_delay(self, sending_info='', set_message=None):
        for i in range(5):
            output('sending delay ' + sending_info + '... ', end='')

            msg = CreateMessage(topic)
            SetMessageBody(msg, 'hi rmq, now is ' + timestr())
            if set_message:
                set_message(msg)

            SetDelayTimeLevel(msg, 5)

            result = SendMessageSync(self.producer, msg)
            msg_id = result.GetMsgId()
            DestroyMessage(msg)

            output('done, msg_id=' + msg_id)

            self.assertIsInstance(result, SendResult)
            # self.assertEqual(result.sendStatus, CSendStatus.E_SEND_OK)
            self.assertIsInstance(msg_id, str, 'message id should be a string')

    def send_message_oneway(self, sending_info='', set_message=None):
        for i in range(5):
            output('sending oneway ' + sending_info + '... ', end='')

            msg = CreateMessage(topic)
            SetMessageBody(msg, 'hi rmq, now is ' + timestr())
            if set_message:
                set_message(msg)

            result = SendMessageOneway(self.producer, msg)
            DestroyMessage(msg)

            self.assertIsInstance(result, int)
            output('done, result=' + str(result))

    def send_message_orderly(self, sending_info='', set_message=None):
        for i in range(5):
            output('sending orderly ' + sending_info + '... ', end='')

            msg = CreateMessage(topic_orderly)
            SetMessageBody(msg, 'hi rmq orderly-message, now is ' + timestr())
            if set_message:
                set_message(msg)

            result = SendMessageOrderly(self.producer, msg, 1, None, self.calc_which_queue_to_send)
            msg_id = result.GetMsgId()

            output('done, msg_id=' + msg_id)

            self.assertIsInstance(result, SendResult)
            # self.assertEqual(result.sendStatus, CSendStatus.E_SEND_OK)
            self.assertIsInstance(msg_id, str, 'message id should be a string')

    def calc_which_queue_to_send(self, size, msg, arg):
        # it is index start with 0....
        return 0

    def test_setUp(self):
        self.assertEqual(self.set_ns_result, 0)
        self.assertEqual(self.start_result, 0)

    def test_send_message(self):
        def set_map(msg):
            SetMessageProperty(msg, 'name', 'test')
            SetMessageProperty(msg, 'id', timestr())

        def set_tag(msg):
            SetMessageTags(msg, tag)

        def set_key(msg):
            SetMessageKeys(msg, key)

        setters = {'map': set_map, 'tag': set_tag, 'key': set_key}
        tests = [
            ['map'],
            ['tag'],
            ['key'],
            ['map', 'tag'],
            ['map', 'key'],
            ['tag', 'key'],
            ['map', 'tag', 'key'],
        ]

        test_methods = [
            self.send_message_sync,
            self.send_message_delay,
            self.send_message_oneway,
            self.send_message_orderly,
        ]

        # -------------------------------------

        for method in test_methods:
            method()
            for test in tests:
                info = 'with ' + ' and '.join(test)

                def set_message(msg):
                    for setter_name in test:
                        setters[setter_name](msg)

                method(info, set_message)
