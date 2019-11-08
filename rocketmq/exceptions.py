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
import re

from .ffi import dll, _CStatus


_EXCEPTION_MAP = {}


def _register(status_code):
    def register(cls):
        _EXCEPTION_MAP[status_code] = cls
        return cls
    return register


def ffi_check(status_code):
    if status_code == _CStatus.OK:
        return
    exc_cls = _EXCEPTION_MAP.get(status_code, RocketMQException)
    msg = dll.GetLatestErrorMessage()
    if msg is not None:
        msg = msg.decode('utf-8')
        msg = re.sub('<.*?(rocketmq-client-cpp/)(.*)>', '\\1\\2', msg)
        if msg.startswith('msg: '):
            msg = msg[5:]
    raise exc_cls(msg)


class RocketMQException(Exception):
    '''RocketMQ exception base class'''
    pass


@_register(_CStatus.NULL_POINTER)
class NullPointerException(RocketMQException):
    pass


@_register(_CStatus.MALLOC_FAILED)
class MallocFailed(RocketMQException):
    pass


class ProducerException(RocketMQException):
    pass


@_register(_CStatus.PRODUCER_START_FAILED)
class ProducerStartFailed(ProducerException):
    pass


@_register(_CStatus.PRODUCER_SEND_SYNC_FAILED)
class ProducerSendSyncFailed(ProducerException):
    pass


@_register(_CStatus.PRODUCER_SEND_ONEWAY_FAILED)
class ProducerSendOnewayFailed(ProducerException):
    pass


@_register(_CStatus.PRODUCER_SEND_ORDERLY_FAILED)
class ProducerSendOrderlyFailed(ProducerException):
    pass


class ProducerSendAsyncFailed(ProducerException):
    def __init__(self, msg, error, file, line, type):
        super(ProducerSendAsyncFailed, self).__init__(msg)
        self.error = error
        self.file = file
        self.line = line
        self.type = type


class ConsumerException(RocketMQException):
    pass


@_register(_CStatus.PUSH_CONSUMER_START_FAILED)
class PushConsumerStartFailed(ConsumerException):
    pass

