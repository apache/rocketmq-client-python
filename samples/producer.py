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
from rocketmq.client import Producer, Message, TransactionMQProducer, TransactionStatus

import time
import threading

topic = 'TopicTest'
gid = 'test'
name_srv = '127.0.0.1:9876'
MUTEX = threading.Lock()

def create_message():
    msg = Message(topic)
    msg.set_keys('XXX')
    msg.set_tags('XXX')
    msg.set_property('property', 'test')
    msg.set_body('message body')
    return msg


def send_message_sync(count):
    producer = Producer(gid)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_sync(msg)
        print ('send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
    print ('send sync message done')
    producer.shutdown()


def send_message_multi_threaded(retry_time):
    producer = Producer(gid)
    producer.set_name_server_address(name_srv)
    msg = create_message()

    global MUTEX
    MUTEX.acquire()
    try:
        producer.start()
    except Exception as e:
        print('ProducerStartFailed:', e)
        MUTEX.release()
        return

    try:
        for i in range(retry_time):
            ret = producer.send_sync(msg)
            if ret.status == 0:
                print('send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
                break
            else:
                print('send message to MQ failed.')
            if i == (retry_time - 1):
                print('send message to MQ failed after retries.')
    except Exception as e:
        print('ProducerSendSyncFailed:', e)
    finally:
        producer.shutdown()
        MUTEX.release()
        return


def send_orderly_with_sharding_key(count):
    producer = Producer(gid, True)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_orderly_with_sharding_key(msg, 'orderId')
        print ('send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
    print ('send sync order message done')
    producer.shutdown()


def check_callback(msg):
    print ('check: ' + msg.body.decode('utf-8'))
    return TransactionStatus.COMMIT


def local_execute(msg, user_args):
    print ('local:   ' + msg.body.decode('utf-8'))
    return TransactionStatus.UNKNOWN


def send_transaction_message(count):
    producer = TransactionMQProducer(gid, check_callback)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_message_in_transaction(msg, local_execute, None)
        print ('send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
    print ('send transaction message done')

    while True:
        time.sleep(3600)


if __name__ == '__main__':
    send_message_sync(10)

