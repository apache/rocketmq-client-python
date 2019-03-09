#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


import RocketMQConsumeClient
import time


topic = 'test-topic-normal'
name_srv = '127.0.0.1:9876'
group = 'test-consumer-group'



'''
init instance and start consume
'''

totalMsg = 0
def consumer_message(message, args):
    global totalMsg
    totalMsg += 1
    print 'total count %d' % totalMsg
    print 'topic=%s' % RocketMQConsumeClient.ConsumeClient.get_message_topic(message)
    print 'tag=%s' % RocketMQConsumeClient.ConsumeClient.get_message_tags(message)
    print 'body=%s' % RocketMQConsumeClient.ConsumeClient.get_message_body(message)
    print 'msg id=%s' % RocketMQConsumeClient.ConsumeClient.get_message_id(message)
    print 'map.keys %s' % RocketMQConsumeClient.ConsumeClient.get_message_keys(message)
    print 'map.name %s' % RocketMQConsumeClient.ConsumeClient.get_message_property(message, 'name')
    print 'map.id %s' % RocketMQConsumeClient.ConsumeClient.get_message_property(message, 'id')
    return 0


consumeClient = RocketMQConsumeClient.ConsumeClient(name_srv, group, topic)
consumeClient.startup_consumer("*", consumer_message, 1, None)
i = 1
while i <= 600:
    print(i)
    i += 1
    time.sleep(10)

consumeClient.ShutdownPushConsumer(consumeClient.consumer)
consumeClient.DestroyPushConsumer(consumeClient.consumer)
print("Consumer Down....")




