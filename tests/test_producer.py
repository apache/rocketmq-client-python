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
import sys

from rocketmq.client import Message, SendStatus, TransactionMQProducer, TransactionStatus

PY_VERSION = sys.version_info[0]


def test_producer_send_sync(producer):
    msg = Message('test')
    msg.set_keys('send_sync')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_sync(msg)
    assert ret.status == SendStatus.OK


def test_producer_send_oneway(producer):
    msg = Message('test')
    msg.set_keys('send_oneway')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    producer.send_oneway(msg)


def test_producer_send_orderly_with_sharding_key(orderly_producer):
    msg = Message('test')
    msg.set_keys('sharding_message')
    msg.set_tags('sharding')
    msg.set_body('sharding message')
    msg.set_property('property', 'test')
    ret = orderly_producer.send_orderly_with_sharding_key(msg, 'order1')
    assert ret.status == SendStatus.OK


def test_transaction_producer():
    stop_event = threading.Event()
    msg_body = 'XXXX'

    def on_local_execute(msg, user_args):
        return TransactionStatus.UNKNOWN

    def on_check(msg):
        stop_event.set()
        assert msg.body.decode('utf-8') == msg_body
        return TransactionStatus.COMMIT

    producer = TransactionMQProducer('transactionTestGroup' + str(PY_VERSION), on_check)
    producer.set_name_server_address('127.0.0.1:9876')
    producer.start()
    msg = Message('test')
    msg.set_keys('transaction')
    msg.set_tags('XXX')
    msg.set_body(msg_body)
    producer.send_message_in_transaction(msg, on_local_execute)
    while not stop_event.is_set():
        time.sleep(2)
    producer.shutdown()

