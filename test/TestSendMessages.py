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

topic = 'test'
name_srv = '127.0.0.1:9876'


def init_producer():
    producer = CreateProducer('TestProducer')
    SetProducerNameServerAddress(producer, name_srv)
    StartProducer(producer)
    return producer


producer = init_producer()
tag = 'rmq-tag'
key = 'rmq-key'


def send_messages_sync(count):
    for a in range(count):
        print 'start sending...'
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print '[RMQ-PRODUCER]start sending...done, msg id = ' + \
            result.GetMsgId()


def send_messages_sync_with_map(count):
    print 'sending message with properties...id, name'
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)

        SetMessageProperty(msg, 'name', 'test')
        SetMessageProperty(msg, 'id', str(time.time()))

        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print '[RMQ-PRODUCER]start sending...done, msg id = ' + \
            result.GetMsgId()


def send_messages_with_tag_sync(count):
    print 'sending message with tag...' + tag
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageTags(msg, tag)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_with_tag_and_map_sync(count):
    print 'sending message with tag...' + tag + ' and properties id, name'
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)

        SetMessageProperty(msg, 'name', 'test')
        SetMessageProperty(msg, 'id', str(time.time()))

        SetMessageTags(msg, tag)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_with_key_sync(count):
    print 'sending message with keys...' + key
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_with_key_and_map_sync(count):
    print 'sending message with keys...' + key + ' and properties id, name'
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)

        SetMessageProperty(msg, 'name', 'test')
        SetMessageProperty(msg, 'id', str(time.time()))

        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_with_key_and_tag_sync(count):
    key = 'rmq-key'
    print 'sending message with keys and tag...' + key + ', ' + tag
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageTags(msg, tag)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_with_key_and_tag_and_map_sync(count):
    key = 'rmq-key'
    print 'sending message with keys and tag...' + \
        key + ', ' + tag + ' and properties id, name'
    for a in range(count):
        body = 'hi rmq, now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)

        SetMessageProperty(msg, 'name', 'test')
        SetMessageProperty(msg, 'id', str(time.time()))

        SetMessageTags(msg, tag)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id = ' + result.GetMsgId()


def send_messages_oneway(count):
    for a in range(count):
        print 'start sending...'
        body = 'hi rmq, this is oneway message. now is ' + \
            time.strftime('%Y.%m.%d', time.localtime(time.time()))
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)

        SetMessageKeys(msg, key)
        SetMessageProperty(msg, 'name', 'test')
        SetMessageProperty(msg, 'id', str(time.time()))

        SendMessageOneway(producer, msg)
        DestroyMessage(msg)
        print 'send oneway is over'


def send_delay_messages(producer, topic, count):
    key = 'rmq-key'
    print 'start sending message'
    tag = 'test'
    for n in range(count):
        body = 'hi rmq, now is' + str(time.time())
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageProperty(msg, 'name', 'hello world')
        SetMessageProperty(msg, 'id', str(time.time()))
        SetMessageTags(msg, tag)
        # messageDelayLevel=1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h

        SetDelayTimeLevel(msg, 5)

        print str(msg)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'msg id =' + result.GetMsgId()


if __name__ == '__main__':
    # print GetVersion()
    while True:
        send_messages_oneway(1)
        time.sleep(1)
