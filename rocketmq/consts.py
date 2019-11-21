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
from enum import Enum


class MessageProperty(Enum):
    TRACE_SWITCH = "TRACE_ON"
    MSG_REGION = "MSG_REGION"
    KEYS = "KEYS"
    TAGS = "TAGS"
    WAIT_STORE_MSG_OK = "WAIT"
    DELAY_TIME_LEVEL = "DELAY"
    RETRY_TOPIC = "RETRY_TOPIC"
    REAL_TOPIC = "REAL_TOPIC"
    REAL_QUEUE_ID = "REAL_QID"
    TRANSACTION_PREPARED = "TRAN_MSG"
    PRODUCER_GROUP = "PGROUP"
    MIN_OFFSET = "MIN_OFFSET"
    MAX_OFFSET = "MAX_OFFSET"
    BUYER_ID = "BUYER_ID"
    ORIGIN_MESSAGE_ID = "ORIGIN_MESSAGE_ID"
    TRANSFER_FLAG = "TRANSFER_FLAG"
    CORRECTION_FLAG = "CORRECTION_FLAG"
    MQ2_FLAG = "MQ2_FLAG"
    RECONSUME_TIME = "RECONSUME_TIME"
    UNIQ_CLIENT_MESSAGE_ID_KEYIDX = "UNIQ_KEY"
    MAX_RECONSUME_TIMES = "MAX_RECONSUME_TIMES"
    CONSUME_START_TIMESTAMP = "CONSUME_START_TIME"
