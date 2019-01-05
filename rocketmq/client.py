# -*- coding: utf-8 -*-
import ctypes
from enum import IntEnum
from collections import namedtuple

from .ffi import (
    dll, _CSendResult, MSG_CALLBACK_FUNC, _CMessageQueue, _CPullStatus,
    _CConsumeStatus, MessageModel,
)
from .exceptions import ffi_check, PushConsumerStartFailed


SendResult = namedtuple('SendResult', ['status', 'msg_id', 'offset'])


class SendStatus(IntEnum):
    OK = 0
    FLUSH_DISK_TIMEOUT = 1
    FLUSH_SLAVE_TIMEOUT = 2
    SLAVE_NOT_AVAILABLE = 3


class Message(object):
    def __init__(self, topic):
        self._handle = dll.CreateMessage(topic.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyMessage(self._handle))

    def set_keys(self, keys):
        ffi_check(dll.SetMessageKeys(self._handle, keys.encode('utf-8')))

    def set_tags(self, tags):
        ffi_check(dll.SetMessageTags(self._handle, tags.encode('utf-8')))

    def set_body(self, body):
        ffi_check(dll.SetMessageBody(self._handle, body.encode('utf-8')))

    def set_property(self, key, value):
        ffi_check(dll.SetMessageProperty(self._handle, key.encode('utf-8'), value.encode('utf-8')))

    def set_delay_time_level(self, delay_time_level):
        ffi_check(dll.SetDelayTimeLevel(self._handle, delay_time_level))

    @property
    def _as_parameter_(self):
        return self._handle


def maybe_decode(val):
    if val:
        return val.decode('utf-8')


class RecvMessage(object):
    def __init__(self, handle):
        self.topic = maybe_decode(dll.GetMessageTopic(handle))
        self.tags = dll.GetMessageTags(handle)
        self.keys = dll.GetMessageKeys(handle)
        self.body = dll.GetMessageBody(handle)
        self.id = maybe_decode(dll.GetMessageId(handle))
        self.delay_time_level = dll.GetMessageDelayTimeLevel(handle)
        self.queue_id = dll.GetMessageQueueId(handle)
        self.reconsume_times = dll.GetMessageReconsumeTimes(handle)
        self.store_size = dll.GetMessageStoreSize(handle)
        self.born_timestamp = dll.GetMessageBornTimestamp(handle)
        self.store_timestamp = dll.GetMessageStoreTimestamp(handle)
        self.queue_offset = dll.GetMessageQueueOffset(handle)
        self.commit_log_offset = dll.GetMessageCommitLogOffset(handle)
        self.prepared_transaction_offset = dll.GetMessagePreparedTransactionOffset(handle)

    def __str__(self):
        return self.body.decode('utf-8')

    def __bytes__(self):
        return self.body

    def __repr__(self):
        return '<RecvMessage topic={} id={} body={}>'.format(
            repr(self.topic),
            repr(self.id),
            repr(self.body),
        )


class Producer(object):
    def __init__(self, group_id, timeout=None, compress_level=None, max_message_size=None):
        self._handle = dll.CreateProducer(group_id.encode('utf-8'))
        if timeout is not None:
            self.set_timeout(timeout)
        if compress_level is not None:
            self.set_compress_level(compress_level)
        if max_message_size is not None:
            self.set_max_message_size(max_message_size)

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyProducer(self._handle))

    def send_sync(self, msg):
        cres = _CSendResult()
        ffi_check(dll.SendMessageSync(self._handle, msg, ctypes.pointer(cres)))
        return SendResult(
            SendStatus(cres.sendStatus),
            cres.msgId.decode('utf-8'),
            cres.offset
        )

    def send_oneway(self, msg):
        ffi_check(dll.SendMessageOneway(self._handle, msg))

    def set_group(self, group_name):
        ffi_check(dll.SetProducerGroupName(group_name.encode('utf-8')))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetProducerNameServerAddress(self._handle, addr.encode('utf-8')))

    def set_namesrv_domain(self, domain):
        ffi_check(dll.SetProducerNameServerDomain(self._handle, domain.encode('utf-8')))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetProducerSessionCredentials(
            self._handle,
            access_key.encode('utf-8'),
            access_secret.encode('utf-8'),
            channel.encode('utf-8')
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


class PushConsumer(object):
    def __init__(self, group_id, orderly=False, message_model=MessageModel.CLUSTERING):
        self._handle = dll.CreatePushConsumer(group_id.encode('utf-8'))
        self._orderly = orderly
        self.set_message_model(message_model)
        self._callback_refs = []

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyPushConsumer(self._handle))

    def set_message_model(self, model):
        ffi_check(dll.SetPushConsumerMessageModel(self._handle, model))

    def start(self):
        if self._callback_refs:
            # rocketmq-client-cpp segfault if we don't have any callback registered
            ffi_check(dll.StartPushConsumer(self._handle))
        else:
            raise PushConsumerStartFailed('PushConsumer start failed: no topic subscribed')

    def shutdown(self):
        ffi_check(dll.ShutdownPushConsumer(self._handle))

    def set_group(self, group_id):
        ffi_check(dll.SetPushConsumerGroupID(group_id.encode('utf-8')))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetPushConsumerNameServerAddress(self._handle, addr.encode('utf-8')))

    def set_namesrv_domain(self, domain):
        ffi_check(dll.SetPushConsumerNameServerDomain(self._handle, domain.encode('utf-8')))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetPushConsumerSessionCredentials(
            self._handle,
            access_key.encode('utf-8'),
            access_secret.encode('utf-8'),
            channel.encode('utf-8')
        ))

    def subscribe(self, topic, callback, expression='*'):
        def _on_message(consumer, msg):
            exc = None
            try:
                callback(RecvMessage(msg))
            except Exception as e:
                exc = e
                return _CConsumeStatus.RECONSUME_LATER.value
            finally:
                if exc:
                    raise exc

            return _CConsumeStatus.CONSUME_SUCCESS.value

        ffi_check(dll.Subscribe(self._handle, topic.encode('utf-8'), expression.encode('utf-8')))
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
        ffi_check(dll.SetPushConsumerInstanceName(self._handle, name.encode('utf-8')))


class PullConsumer(object):
    def __init__(self, group_id):
        self._handle = dll.CreatePullConsumer(group_id.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyPullConsumer(self._handle))

    def start(self):
        ffi_check(dll.StartPullConsumer(self._handle))

    def shutdown(self):
        ffi_check(dll.ShutdownPullConsumer(self._handle))

    def set_group(self, group_id):
        ffi_check(dll.SetPullConsumerGroupID(group_id.encode('utf-8')))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetPullConsumerNameServerAddress(self._handle, addr.encode('utf-8')))

    def set_namesrv_domain(self, domain):
        ffi_check(dll.SetPullConsumerNameServerDomain(self._handle, domain.encode('utf-8')))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetPullConsumerSessionCredentials(
            self._handle,
            access_key.encode('utf-8'),
            access_secret.encode('utf-8'),
            channel.encode('utf-8')
        ))

    def pull(self, topic, expression='*', max_num=32):
        message_queue = ctypes.POINTER(_CMessageQueue)()
        queue_size = ctypes.c_int()
        ffi_check(dll.FetchSubscriptionMessageQueues(
            self._handle,
            topic.encode('utf-8'),
            ctypes.pointer(message_queue),
            ctypes.pointer(queue_size)
        ))
        for i in range(int(queue_size.value)):
            tmp_offset = ctypes.c_longlong()
            while True:
                pull_res = dll.Pull(
                    self._handle,
                    ctypes.pointer(message_queue[i]),
                    expression.encode('utf-8'),
                    tmp_offset,
                    max_num,
                )
                if pull_res.pullStatus != _CPullStatus.BROKER_TIMEOUT:
                    tmp_offset = pull_res.nextBeginOffset
                if pull_res.pullStatus == _CPullStatus.FOUND:
                    for i in range(int(pull_res.size)):
                        yield RecvMessage(pull_res.msgFoundList[i])
                elif pull_res.pullStatus == _CPullStatus.NO_MATCHED_MSG:
                    break
                dll.ReleasePullResult(pull_res)  # NOTE: No need to check ffi return code
        ffi_check(dll.ReleaseSubscriptionMessageQueue(message_queue))
