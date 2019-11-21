# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import time
import threading

import pytest

from rocketmq.client import Message, SendStatus, ConsumeStatus, PushConsumer
from rocketmq.exceptions import PushConsumerStartFailed


def _send_test_msg(producer):
    msg = Message('test')
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    msg.set_property('property', 'test')
    ret = producer.send_sync(msg)
    assert ret.status == SendStatus.OK


def test_push_consumer_no_subscription_start_fail():
    consumer = PushConsumer('testGroup')
    consumer.set_name_server_address("127.0.0.1:9876")
    with pytest.raises(PushConsumerStartFailed):
        consumer.start()


def test_push_consumer(producer, push_consumer):
    stop_event = threading.Event()
    _send_test_msg(producer)
    errors = []

    def on_message(msg):
        stop_event.set()
        try:
            assert msg.body.decode('utf-8') == 'XXXX'
            assert msg.keys.decode('utf-8') == 'XXX'
            assert msg.get_property('property').decode('utf-8') == 'test'
            return ConsumeStatus.CONSUME_SUCCESS
        except Exception as exc:
            errors.append(exc)
            return ConsumeStatus.RECONSUME_LATER

    push_consumer.subscribe('test', on_message)
    push_consumer.start()
    while not stop_event.is_set():
        time.sleep(2)
    if errors:
        raise errors[0]


def test_push_consumer_reconsume_later(producer, push_consumer):
    stop_event = threading.Event()
    _send_test_msg(producer)
    raised_exc = threading.Event()
    errors = []

    def on_message(msg):
        if not raised_exc.is_set():
            raised_exc.set()
            return ConsumeStatus.RECONSUME_LATER

        stop_event.set()
        try:
            assert msg.body.decode('utf-8') == 'XXXX'
            assert msg.keys.decode('utf-8') == 'XXX'
        except Exception as exc:
            errors.append(exc)
            return ConsumeStatus.CONSUME_SUCCESS

    push_consumer.subscribe('test', on_message)
    push_consumer.start()
    while not stop_event.is_set():
        time.sleep(2)
    if errors:
        raise errors[0]
