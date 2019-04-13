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
import RocketMQConfig
import time
import utils.log_util as log_util


rocketMQConfig= RocketMQConfig.Config()
name_srv = rocketMQConfig.get_name_server()
consume_config = rocketMQConfig.get_consumer_config()
topic_tag_list = consume_config.get("topic_tag_list")
group_id = consume_config.get("group_id")
thread_count = consume_config.get("thread_count")
max_batch_size = consume_config.get("max_batch_size")


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


logger = log_util.setup_logging(default_path="logs/logging.json")

consumeClient = RocketMQConsumeClient.ConsumeClient(name_srv, group_id, topic_tag_list)
consumeClient.startup_consumer(consumer_message, thread_count, max_batch_size, None)
i = 1
while i <= 600:
    logger.info(i)
    i += 1
    time.sleep(10)

consumeClient.ShutdownPushConsumer(consumeClient.consumer)
consumeClient.DestroyPushConsumer(consumeClient.consumer)
logger.info("Consumer Down....")




