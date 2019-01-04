# -*- coding: utf-8 -*-
import time
import threading

from rocketmq.client import Message, SendStatus


def _send_test_msg(producer):
    msg = Message('test')
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_sync(msg)
    assert ret.status == SendStatus.OK


def test_pull_consumer(producer, pull_consumer):
    try:
        msg = next(pull_consumer.pull('test'))
    except StopIteration:
        _send_test_msg(producer)
        msg = next(pull_consumer.pull('test'))
        time.sleep(5)
    assert msg.body.decode('utf-8') == 'XXXX'


def test_push_consumer(producer, push_consumer):
    stop_event = threading.Event()
    _send_test_msg(producer)

    def on_message(msg):
        stop_event.set()
        assert msg.body.decode('utf-8') == 'XXXX'

    push_consumer.subscribe('test', on_message)
    push_consumer.start()
    while not stop_event.is_set():
        time.sleep(10)
