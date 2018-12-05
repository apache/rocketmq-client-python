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
import sys

topic = 'test'
name_srv = '127.0.0.1:9876'
tag = 'rmq-tag'
consumer_group = 'test-consumer-group'
totalMsg = 0


def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    sys.exit(0)


def consumer_message(msg):
    global totalMsg
    totalMsg += 1
    print 'total count %d' % totalMsg
    print 'topic=%s' % GetMessageTopic(msg)
    print 'tag=%s' % GetMessageTags(msg)
    print 'body=%s' % GetMessageBody(msg)
    print 'msg id=%s' % GetMessageId(msg)

    print 'map.keys %s' % GetMessageKeys(msg)

    print 'map.name %s' % GetMessageProperty(msg, 'name')
    print 'map.id %s' % GetMessageProperty(msg, 'id')
    return 0


def init_producer(_group, _topic, _tag):
    consumer = CreatePushConsumer(_group)
    SetPushConsumerNameServerAddress(consumer, name_srv)
    SetPushConsumerThreadCount(consumer, 1)
    Subscribe(consumer, _topic, _tag)
    RegisterMessageCallback(consumer, consumerMessage)
    StartPushConsumer(consumer)
    print 'consumer is ready...'
    return consumer


def start_one_consumer(_group, _topic, _tag):
    consumer = init_producer(_group, _topic, _tag)
    i = 1
    while i <= 10:
        print 'clock: ' + str(i)
        i += 1
        time.sleep(10)

    ShutdownPushConsumer(consumer)
    DestroyPushConsumer(consumer)
    print("Consumer Down....")


if __name__ == '__main__':
    start_one_consumer(consumer_group, topic, '*')
