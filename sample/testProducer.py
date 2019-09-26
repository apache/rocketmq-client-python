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

from base import *
import time


def initProducer(name):
    print("---------Create Producer---------------")
    producer = CreateProducer(name)
    SetProducerNameServerAddress(producer, "172.17.0.2:9876")
    StartProducer(producer)
    return producer


def testSendMssage(producer, topic, key, body):
    print("Starting Sending.....")
    msg = CreateMessage(topic)
    SetMessageBody(msg, body)
    SetMessageKeys(msg, key)
    SetMessageTags(msg, "ThisMessageTag.")
    result = SendMessageSync(producer, msg)
    print(result)
    print("Msgid:")
    print(result.GetMsgId())
    print("Offset:")
    print(result.offset)
    print("sendStatus:")
    print(result.sendStatus)
    DestroyMessage(msg)
    print("Done...............")


def testSendMessageOneway(producer, topic, key, body):
    print("Starting Sending(Oneway).....")
    msg = CreateMessage(topic)
    SetMessageBody(msg, body)
    SetMessageKeys(msg, key)
    SetMessageTags(msg, "Send Message Oneway Test.")
    SendMessageOneway(producer, msg)
    DestroyMessage(msg)
    print("Done...............")


def testSendMssageOrderly(producer, topic, key, body):
    print("Starting Sending.....")
    msg = CreateMessage(topic)
    SetMessageBody(msg, body)
    SetMessageKeys(msg, key)
    SetMessageTags(msg, "ThisMessageTag.")
    result = SendMessageOrderlyByShardingKey(producer, msg, "orderId")
    print(result)
    print("Msgid:")
    print(result.GetMsgId())
    print("Offset:")
    print(result.offset)
    print("sendStatus:")
    print(result.sendStatus)
    DestroyMessage(msg)
    print("Done...............")


def releaseProducer(producer):
    ShutdownProducer(producer)
    DestroyProducer(producer)
    print("--------Release producer-----------")


showClientVersion()
producer = initProducer("TestPythonProducer")
topic = "T_TestTopic"
key = "TestKeys"
body = "ThisIsTestBody"
i = 0
while i < 100:
    i += 1
    testSendMssageOrderly(producer, topic, key, body)

    print("Now Send Message:", i)

while i < 10:
    i += 1
    testSendMessageOneway(producer, topic, key, body)
    print("Now Send Message One way:", i)

releaseProducer(producer)
