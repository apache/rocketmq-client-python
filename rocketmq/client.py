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
import sys
import ctypes
from enum import IntEnum
from collections import namedtuple

from .ffi import (
    dll, _CSendResult, MSG_CALLBACK_FUNC, MessageModel, TRANSACTION_CHECK_CALLBACK,
    LOCAL_TRANSACTION_EXECUTE_CALLBACK
)
from .exceptions import (
    ffi_check, NullPointerException,
)
from .consts import MessageProperty

__all__ = ['SendStatus', 'Message', 'ReceivedMessage', 'Producer', 'PushConsumer', 'TransactionMQProducer',
           'TransactionStatus', 'ConsumeStatus']

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

SendResult = namedtuple('SendResult', ['status', 'msg_id', 'offset'])


class SendStatus(IntEnum):
    OK = 0
    FLUSH_DISK_TIMEOUT = 1
    FLUSH_SLAVE_TIMEOUT = 2
    SLAVE_NOT_AVAILABLE = 3


class TransactionStatus(IntEnum):
    COMMIT = 0
    ROLLBACK = 1
    UNKNOWN = 2


class ConsumeStatus(IntEnum):
    CONSUME_SUCCESS = 0
    RECONSUME_LATER = 1


def _to_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


class Message(object):
    def __init__(self, topic):
        self._handle = dll.CreateMessage(_to_bytes(topic))

    def set_keys(self, keys):
        ffi_check(dll.SetMessageKeys(self._handle, _to_bytes(keys)))

    def set_tags(self, tags):
        ffi_check(dll.SetMessageTags(self._handle, _to_bytes(tags)))

    def set_body(self, body):
        ffi_check(dll.SetMessageBody(self._handle, _to_bytes(body)))

    def set_property(self, key, value):
        ffi_check(dll.SetMessageProperty(self._handle, _to_bytes(key), _to_bytes(value)))

    def set_delay_time_level(self, delay_time_level):
        ffi_check(dll.SetDelayTimeLevel(self._handle, delay_time_level))

    @property
    def _as_parameter_(self):
        return self._handle


def maybe_decode(val):
    if isinstance(val, binary_type):
        return val.decode('utf-8')
    elif isinstance(val, text_type):
        return val
    raise TypeError('Expects string types, but got %s', type(val))


class ReceivedMessage(object):
    def __init__(self, handle):
        self._handle = handle

    @property
    def topic(self):
        return maybe_decode(dll.GetMessageTopic(self._handle))

    @property
    def tags(self):
        return dll.GetMessageTags(self._handle)

    @property
    def keys(self):
        return dll.GetMessageKeys(self._handle)

    @property
    def body(self):
        return dll.GetMessageBody(self._handle)

    @property
    def id(self):
        return maybe_decode(dll.GetMessageId(self._handle))

    @property
    def delay_time_level(self):
        return dll.GetMessageDelayTimeLevel(self._handle)

    @property
    def queue_id(self):
        return dll.GetMessageQueueId(self._handle)

    @property
    def reconsume_times(self):
        return dll.GetMessageReconsumeTimes(self._handle)

    @property
    def store_size(self):
        return dll.GetMessageStoreSize(self._handle)

    @property
    def born_timestamp(self):
        return dll.GetMessageBornTimestamp(self._handle)

    @property
    def store_timestamp(self):
        return dll.GetMessageStoreTimestamp(self._handle)

    @property
    def queue_offset(self):
        return dll.GetMessageQueueOffset(self._handle)

    @property
    def commit_log_offset(self):
        return dll.GetMessageCommitLogOffset(self._handle)

    @property
    def prepared_transaction_offset(self):
        return dll.GetMessagePreparedTransactionOffset(self._handle)

    def get_property(self, prop):
        if isinstance(prop, MessageProperty):
            prop = prop.value
        val = dll.GetMessageProperty(self._handle, _to_bytes(prop))
        return val

    def __getitem__(self, key):
        return self.get_property(key)

    def __str__(self):
        return self.body.decode('utf-8')

    def __bytes__(self):
        return self.body

    def __repr__(self):
        return '<ReceivedMessage topic={} id={} body={}>'.format(
            repr(self.topic),
            repr(self.id),
            repr(self.body),
        )


class Producer(object):
    def __init__(self, group_id, orderly=False, timeout=None, compress_level=None, max_message_size=None):
        if orderly:
            self._handle = dll.CreateOrderlyProducer(_to_bytes(group_id))
        else:
            self._handle = dll.CreateProducer(_to_bytes(group_id))
        if self._handle is None:
            raise NullPointerException('Returned null pointer when create Producer')
        if timeout is not None:
            self.set_timeout(timeout)
        if compress_level is not None:
            self.set_compress_level(compress_level)
        if max_message_size is not None:
            self.set_max_message_size(max_message_size)
        self._callback_refs = []

    def __enter__(self):
        self.start()

    def __exit__(self, exec_type, value, traceback):
        self.shutdown()

    def send_sync(self, msg):
        c_result = _CSendResult()
        ffi_check(dll.SendMessageSync(self._handle, msg, ctypes.pointer(c_result)))
        return SendResult(
            SendStatus(c_result.sendStatus),
            c_result.msgId.decode('utf-8'),
            c_result.offset
        )

    def send_oneway(self, msg):
        ffi_check(dll.SendMessageOneway(self._handle, msg))

    def send_orderly_with_sharding_key(self, msg, sharding_key):
        c_result = _CSendResult()
        ffi_check(
            dll.SendMessageOrderlyByShardingKey(self._handle, msg, _to_bytes(sharding_key), ctypes.pointer(c_result)))
        return SendResult(
            SendStatus(c_result.sendStatus),
            c_result.msgId.decode('utf-8'),
            c_result.offset
        )

    def set_group(self, group_name):
        ffi_check(dll.SetProducerGroupName(self._handle, _to_bytes(group_name)))

    def set_name_server_address(self, addr):
        ffi_check(dll.SetProducerNameServerAddress(self._handle, _to_bytes(addr)))

    def set_name_server_domain(self, domain):
        ffi_check(dll.SetProducerNameServerDomain(self._handle, _to_bytes(domain)))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetProducerSessionCredentials(
            self._handle,
            _to_bytes(access_key),
            _to_bytes(access_secret),
            _to_bytes(channel)
        ))

    def set_timeout(self, timeout):
        ffi_check(dll.SetProducerSendMsgTimeout(self._handle, timeout))

    def set_compress_level(self, level):
        ffi_check(dll.SetProducerCompressLevel(self._handle, level))

    def set_max_message_size(self, max_size):
        ffi_check(dll.SetProducerMaxMessageSize(self._handle, max_size))

    def start(self):
        ffi_check(dll.StartProducer(self._handle))

    def shutdown(self):
        ffi_check(dll.ShutdownProducer(self._handle))


class TransactionMQProducer(Producer):
    def __init__(self, group_id, checker_callback, user_args=None, timeout=None, compress_level=None,
                 max_message_size=None):
        super(TransactionMQProducer, self).__init__(group_id, timeout, compress_level, max_message_size)
        self._callback_refs = []

        def _on_check(producer, c_message, user_data):
            exc = None
            try:
                py_message = ReceivedMessage(c_message)
                check_result = checker_callback(py_message)
                if check_result != TransactionStatus.UNKNOWN and check_result != TransactionStatus.COMMIT \
                        and check_result != TransactionStatus.ROLLBACK:
                    raise ValueError(
                        'Check transaction status error, please use enum \'TransactionStatus\' as response')
                return check_result
            except BaseException as e:
                exc = e
                return TransactionStatus.UNKNOWN
            finally:
                if exc:
                    raise exc

        transaction_checker_callback = TRANSACTION_CHECK_CALLBACK(_on_check)
        self._callback_refs.append(transaction_checker_callback)

        self._handle = dll.CreateTransactionProducer(_to_bytes(group_id), transaction_checker_callback, user_args)
        if self._handle is None:
            raise NullPointerException('Returned null pointer when create transaction producer')
        if timeout is not None:
            self.set_timeout(timeout)
        if compress_level is not None:
            self.set_compress_level(compress_level)
        if max_message_size is not None:
            self.set_max_message_size(max_message_size)

    def __enter__(self):
        self.start()

    def __exit__(self, exec_type, value, traceback):
        self.shutdown()

    def set_name_server_address(self, addr):
        ffi_check(dll.SetProducerNameServerAddress(self._handle, _to_bytes(addr)))

    def start(self):
        ffi_check(dll.StartProducer(self._handle))

    def send_message_in_transaction(self, message, local_execute, user_args=None):

        def _on_local_execute(producer, c_message, usr_args):
            exc = None
            try:
                py_message = ReceivedMessage(c_message)
                local_result = local_execute(py_message, usr_args)
                if local_result != TransactionStatus.UNKNOWN and local_result != TransactionStatus.COMMIT \
                        and local_result != TransactionStatus.ROLLBACK:
                    raise ValueError(
                        'Local transaction status error, please use enum \'TransactionStatus\' as response')
                return local_result
            except BaseException as e:
                exc = e
                return TransactionStatus.UNKNOWN
            finally:
                if exc:
                    raise exc

        local_execute_callback = LOCAL_TRANSACTION_EXECUTE_CALLBACK(_on_local_execute)
        self._callback_refs.append(local_execute_callback)

        result = _CSendResult()
        try:
            ffi_check(
                dll.SendMessageTransaction(self._handle,
                                           message,
                                           local_execute_callback,
                                           user_args,
                                           ctypes.pointer(result)))
        finally:
            self._callback_refs.remove(local_execute_callback)

        return SendResult(
            SendStatus(result.sendStatus),
            result.msgId.decode('utf-8'),
            result.offset
        )


class PushConsumer(object):
    def __init__(self, group_id, orderly=False, message_model=MessageModel.CLUSTERING):
        self._handle = dll.CreatePushConsumer(_to_bytes(group_id))
        if self._handle is None:
            raise NullPointerException('Returned null pointer when create PushConsumer')
        self._orderly = orderly
        self.set_message_model(message_model)
        self._callback_refs = []

    def __enter__(self):
        self.start()

    def __exit__(self, exec_type, value, traceback):
        self.shutdown()

    def set_message_model(self, model):
        ffi_check(dll.SetPushConsumerMessageModel(self._handle, model))

    def start(self):
        ffi_check(dll.StartPushConsumer(self._handle))

    def shutdown(self):
        ffi_check(dll.ShutdownPushConsumer(self._handle))

    def set_group(self, group_id):
        ffi_check(dll.SetPushConsumerGroupID(self._handle, _to_bytes(group_id)))

    def set_name_server_address(self, addr):
        ffi_check(dll.SetPushConsumerNameServerAddress(self._handle, _to_bytes(addr)))

    def set_name_server_domain(self, domain):
        ffi_check(dll.SetPushConsumerNameServerDomain(self._handle, _to_bytes(domain)))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetPushConsumerSessionCredentials(
            self._handle,
            _to_bytes(access_key),
            _to_bytes(access_secret),
            _to_bytes(channel)
        ))

    def subscribe(self, topic, callback, expression='*'):
        def _on_message(consumer, msg):
            exc = None
            try:
                consume_result = callback(ReceivedMessage(msg))
                if consume_result != ConsumeStatus.CONSUME_SUCCESS and consume_result != ConsumeStatus.RECONSUME_LATER:
                    raise ValueError('Consume status error, please use enum \'ConsumeStatus\' as response')
                return consume_result
            except BaseException as e:
                exc = e
                return ConsumeStatus.RECONSUME_LATER
            finally:
                if exc:
                    raise exc

        ffi_check(dll.Subscribe(self._handle, _to_bytes(topic), _to_bytes(expression)))
        self._register_callback(_on_message)

    def _register_callback(self, callback):
        if self._orderly:
            register_func = dll.RegisterMessageCallbackOrderly
        else:
            register_func = dll.RegisterMessageCallback

        func = MSG_CALLBACK_FUNC(callback)
        self._callback_refs.append(func)
        ffi_check(register_func(self._handle, func))

    def _unregister_callback(self):
        if self._orderly:
            ffi_check(dll.UnregisterMessageCallbackOrderly(self._handle))
        ffi_check(dll.UnregisterMessageCallback(self._handle))
        self._callback_refs = []

    def set_thread_count(self, thread_count):
        ffi_check(dll.SetPushConsumerThreadCount(self._handle, thread_count))

    def set_message_batch_max_size(self, max_size):
        ffi_check(dll.SetPushConsumerMessageBatchMaxSize(self._handle, max_size))

    def set_instance_name(self, name):
        ffi_check(dll.SetPushConsumerInstanceName(self._handle, _to_bytes(name)))
