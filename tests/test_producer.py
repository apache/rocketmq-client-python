# -*- coding: utf-8 -*-
from rocketmq.client import Message, SendStatus


def test_producer(producer):
    msg = Message('test')
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_sync(msg)
    assert ret.status == SendStatus.OK
