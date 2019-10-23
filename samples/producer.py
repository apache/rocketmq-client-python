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
from rocketmq.client import Producer, Message, TransactionMQProducer
from rocketmq.consts import MessageProperty

import time

topic = 'TopicTest'
gid = 'test'
name_srv = '47.107.167.190:9876'


def init_producer():
    producer = Producer(gid)
    producer.set_namesrv_addr(name_srv)
    producer.start()
    return producer


producer = init_producer()


def create_message():
    msg = Message(topic)
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_body('message body')
    return msg


def send_message_sync(count):
    for n in range(count):
        msg = create_message()
        ret = producer.send_sync(msg)
        print 'send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id + ' offset: ' + str(ret.offset)
    print 'send sync message done'
    producer.shutdown()


def send_orderly_with_sharding_key(count):
    for n in range(count):
        msg = create_message()
        ret = producer.send_orderly_with_sharding_key(msg, 'orderId')
        print 'send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id + ' offset: ' + str(ret.offset)
    print 'send sync message done'
    producer.shutdown()


def check_callback(msg):
    print 'check'
    # print msg.body.decode('utf-8')


def local_execute(msg, user_args):
    print 'local'
    print msg[MessageProperty.TAGS]
    # print msg.body.decode('utf-8')


def send_transaction_message(count):
    transactionMQProducer = TransactionMQProducer(gid, check_callback);
    for n in range(count):
        msg = create_message()
        ret = transactionMQProducer.send_message_in_transaction(msg, local_execute, 1)
        print 'send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id + ' offset: ' + str(ret.offset)
    print 'send sync message done'

    while True:
        time.sleep(3600)
    producer.shutdown()


if __name__ == '__main__':
    send_message_sync(10)
