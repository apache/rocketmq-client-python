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

from rocketmq.client import Message, SendStatus


def test_producer_send_sync(producer):
    msg = Message('test')
    msg.set_keys('send_sync')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_sync(msg)
    assert ret.status == SendStatus.OK


def test_producer_send_async(producer):
    stop_event = threading.Event()
    errors = []

    def on_success(result):
        stop_event.set()
        if not result.msg_id:
            errors.append(AssertionError('Producer send_async failed'))

    def on_exception(exc):
        stop_event.set()
        errors.append(exc)

    msg = Message('test')
    msg.set_keys('send_async')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    producer.send_async(msg, on_success, on_exception)

    max_wait = 10
    wait_count = 0
    while not stop_event.is_set():
        if wait_count >= max_wait:
            stop_event.set()
            raise Exception('test timed-out')
        time.sleep(1)
        wait_count += 1
    if errors:
        raise errors[0]


def test_producer_send_oneway(producer):
    msg = Message('test')
    msg.set_keys('send_oneway')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    producer.send_oneway(msg)


def test_producer_send_oneway_orderly(producer):
    msg = Message('test')
    msg.set_keys('send_oneway_orderly')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    producer.send_oneway_orderly(msg, 1)


def test_producer_send_orderly(producer):
    msg = Message('test')
    msg.set_keys('send_orderly')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_orderly(msg, 1)
    assert ret.status == SendStatus.OK


def test_producer_send_batch(producer):
    batch_msg = []
    msg = Message('test')
    msg.set_keys('send_batch_1')
    msg.set_tags('XXX1')
    msg.set_body('XXXX1')
    batch_msg.append(msg)

    msg = Message('test')
    msg.set_keys('send_batch_2')
    msg.set_tags('XXX2')
    msg.set_body('XXXX2')
    batch_msg.append(msg)

    ret = producer.send_batch(batch_msg)
    assert ret.status == SendStatus.OK
