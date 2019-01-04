# -*- coding: utf-8 -*-
from rocketmq.client import Producer, Message, SendStatus


def test_producer():
    producer = Producer('testGroup')
    producer.set_namesrv_addr('127.0.0.1:9876')
    producer.start()

    msg = Message('test')
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_body('XXXX')
    ret = producer.send_sync(msg)
    producer.shutdown()
    assert ret.status == SendStatus.OK
