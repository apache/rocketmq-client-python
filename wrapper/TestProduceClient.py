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


import RocketMQProduceClient
import RocketMQConfig
import time
import utils.log_util as log_util


topic_orderly = 'test-topic-normal-orderly'

rocketMQConfig= RocketMQConfig.Config()
produce_config = rocketMQConfig.get_producer_config()
topic = produce_config.get("topic")
tag = produce_config.get("tag")
group = produce_config.get("group_id")
name_srv = rocketMQConfig.get_name_server()


logger = log_util.setup_logging(default_path="logging.json")


'''
init instance
'''
produceClient = RocketMQProduceClient.ProduceClient(name_srv, group, topic)
produceClient.start_producer()

'''
1.test oneway
'''
key = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
message = produceClient.create_message('this is a cat at '+key, key, tag)
result = produceClient.send_message_oneway(message)
produceClient.destory_message(message)
logger.info('test send_message_oneway:%s'%(result))

'''
2.test async
'''
count = 3
while count > 0:
    time.sleep(5)
    count -= 1
    key = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    message = produceClient.create_message('this is a apple at '+key, key, 'friut')
    result = produceClient.send_message_sync(message)
    produceClient.destory_message(message)
    logger.info('%d test send_message_sync:%s'%(count, produceClient.resolve_result(result)))


'''
3. test send_message_orderly
'''


def calc_which_queue_to_send(size, msg, arg):
    logger.info("i am a callback ", size, msg, arg)
    return 0


count = 4
while count > 0:
    time.sleep(5)
    count -= 1
    key = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    message = produceClient.create_message('this is a plan at '+key, key, 'tools')
    result = produceClient.send_message_orderly(message, 1, message, calc_which_queue_to_send)
    produceClient.destory_message(message)
    logger.info('%d test send_message_sync:%s'%(count, produceClient.resolve_result(result)))


