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

topic = 'test-topic-normal'
topic_orderly = 'test-topic-normal-orderly'
name_srv = '127.0.0.1:9876'


def init_producer():
    producer = CreateProducer('TestProducer')
    SetProducerLogLevel(producer, CLogLevel.E_LOG_LEVEL_INFO)
    SetProducerNameServerAddress(producer, name_srv)
    StartProducer(producer)
    return producer

def transaction_local_checker(msg):
    print 'begin check for msg: ' + GetMessageId(msg)
    return TransactionStatus.E_COMMIT_TRANSACTION

def init_transaction_producer():
    producer = CreateTransactionProducer('TransactionTestProducer', transaction_local_checker)
    SetProducerLogLevel(producer, CLogLevel.E_LOG_LEVEL_INFO)
    SetProducerNameServerAddress(producer, name_srv)
    StartProducer(producer)
    return producer

producer = init_transaction_producer()
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

def send_message_orderly(count):
    key = 'rmq-key'
    print 'start sending order-ly message'
    tag = 'test'
    for n in range(count):
        body = 'hi rmq orderly-message, now is' + str(n)
        msg = CreateMessage(topic_orderly)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageTags(msg, tag)

        result = SendMessageOrderly(producer, msg, 1, None, calc_which_queue_to_send)
        DestroyMessage(msg)
        print 'msg id =' + result.GetMsgId()

def send_message_orderly_with_shardingkey(count):
    key = 'rmq-key'
    print 'start sending sharding key order-ly message'
    tag = 'test'
    for n in range(count):
        body = 'hi rmq sharding orderly-message, now is' + str(n)
        msg = CreateMessage(topic_orderly)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageTags(msg, tag)

        result = SendMessageOrderlyByShardingKey(producer, msg, 'orderId')
        DestroyMessage(msg)
        print 'msg id =' + result.GetMsgId()

def calc_which_queue_to_send(size, msg, arg): ## it is index start with 0....
    return 0

def send_message_async(count):
    key = 'rmq-key'
    print 'start sending message'
    tag = 'test'
    for n in range(count):
        body = 'hi rmq message, now is' + str(n)
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageTags(msg, tag)

        SendMessageAsync(producer, msg, send_message_async_success, send_message_async_fail)
        DestroyMessage(msg)
    print 'send async message done'
    time.sleep(10000)

def send_message_async_success(result, msg):
    print 'send success'
    print 'msg id =' + result.GetMsgId()

def send_message_async_fail(msg, exception):
    print 'send message failed'
    print 'error msg: ' + exception.GetMsg()

def send_transaction_message(count):
    key = 'rmq-key'
    print 'start send transaction message'
    tag = 'test'
    for n in range(count):
        body = 'hi rmq message, now is' + str(n)
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        SetMessageKeys(msg, key)
        SetMessageTags(msg, tag)

        SendMessageInTransaction(producer, msg, transaction_local_execute, None)
    print 'send transaction message done'
    time.sleep(10000)

def transaction_local_execute(msg, args):
    print 'begin execute local transaction'
    return TransactionStatus.E_UNKNOWN_TRANSACTION

if __name__ == '__main__':
    send_transaction_message(10)
