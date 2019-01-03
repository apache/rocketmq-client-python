# -*- coding: utf-8 -*-
import ctypes
from collections import namedtuple

from .ffi import (
    dll, _CSendResult, MSG_CALLBACK_FUNC, _CMessageQueue, _CPullStatus,
    _CConsumeStatus, MessageModel,
)


SendResult = namedtuple('SendResult', ['status', 'msg_id', 'offset'])


class Message(object):
    def __init__(self, topic):
        self._handle = dll.CreateMessage(topic.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            dll.DestroyMessage(self._handle)

    def set_keys(self, keys):
        return dll.SetMessageKeys(self._handle, keys.encode('utf-8'))

    def set_tags(self, tags):
        return dll.SetMessageTags(self._handle, tags.encode('utf-8'))

    def set_body(self, body):
        return dll.SetMessageBody(self._handle, body.encode('utf-8'))

    def set_property(self, key, value):
        return dll.SetMessageProperty(self._handle, key.encode('utf-8'), value.encode('utf-8'))

    def set_delay_time_level(self, delay_time_level):
        return dll.SetDelayTimeLevel(self._handle, delay_time_level)

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


class Producer(object):
    def __init__(self, group_id):
        self._handle = dll.CreateProducer(group_id.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            dll.DestroyProducer(self._handle)

    def send_sync(self, msg):
        cres = _CSendResult()
        dll.SendMessageSync(self._handle, msg, ctypes.pointer(cres))
        return SendResult(cres.sendStatus, cres.msgId.decode('utf-8'), cres.offset)

    def send_oneway(self, msg):
        return dll.SendMessageOneway(self._handle, msg)

    def set_group(self, group_name):
        return dll.SetProducerGroupName(group_name.encode('utf-8'))

    def set_namesrv_addr(self, addr):
        return dll.SetProducerNameServerAddress(self._handle, addr.encode('utf-8'))

    def set_namesrv_domain(self, domain):
        return dll.SetProducerNameServerDomain(self._handle, domain.encode('utf-8'))

    def set_session_credentials(self, access_key, access_secret, channel):
        return dll.SetProducerSessionCredentials(self._handle, access_key.encode('utf-8'), access_secret.encode('utf-8'), channel.encode('utf-8'))

    def start(self):
        return dll.StartProducer(self._handle)

    def shutdown(self):
        return dll.ShutdownProducer(self._handle)


class PushConsumer(object):
    def __init__(self, group_id, orderly=False, message_model=MessageModel.CLUSTERING):
        self._handle = dll.CreatePushConsumer(group_id.encode('utf-8'))
        self._orderly = orderly
        self.set_message_model(message_model)
        self._refs = []

    def __del__(self):
        if self._handle is not None:
            dll.DestroyPushConsumer(self._handle)

    def set_message_model(self, model):
        dll.SetPushConsumerMessageModel(self._handle, model)

    def start(self):
        return dll.StartPushConsumer(self._handle)

    def shutdown(self):
        return dll.ShutdownPushConsumer(self._handle)

    def set_group(self, group_id):
        return dll.SetPushConsumerGroupID(group_id.encode('utf-8'))

    def set_namesrv_addr(self, addr):
        return dll.SetPushConsumerNameServerAddress(self._handle, addr.encode('utf-8'))

    def set_namesrv_domain(self, domain):
        return dll.SetPushConsumerNameServerDomain(self._handle, domain.encode('utf-8'))

    def set_session_credentials(self, access_key, access_secret, channel):
        return dll.SetPushConsumerSessionCredentials(self._handle, access_key.encode('utf-8'), access_secret.encode('utf-8'), channel.encode('utf-8'))

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

        dll.Subscribe(self._handle, topic.encode('utf-8'), expression.encode('utf-8'))
        self._register_callback(_on_message)

    def _register_callback(self, callback):
        if self._orderly:
            register_func = dll.RegisterMessageCallbackOrderly
        else:
            register_func = dll.RegisterMessageCallback

        func = MSG_CALLBACK_FUNC(callback)
        self._refs.append(func)
        return register_func(self._handle, func)

    def _unregister_callback(self):
        if self._orderly:
            return dll.UnregisterMessageCallbackOrderly(self._handle)
        return dll.UnregisterMessageCallback(self._handle)

    def set_thread_count(self, thread_count):
        return dll.SetPushConsumerThreadCount(self._handle, thread_count)

    def set_message_batch_max_size(self, max_size):
        return dll.SetPushConsumerMessageBatchMaxSize(self._handle, max_size)

    def set_instance_name(self, name):
        return dll.SetPushConsumerInstanceName(self._handle, name.encode('utf-8'))


class PullConsumer(object):
    def __init__(self, group_id):
        self._handle = dll.CreatePullConsumer(group_id.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            dll.DestroyPullConsumer(self._handle)

    def start(self):
        return dll.StartPullConsumer(self._handle)

    def shutdown(self):
        return dll.ShutdownPullConsumer(self._handle)

    def set_group(self, group_id):
        return dll.SetPullConsumerGroupID(group_id.encode('utf-8'))

    def set_namesrv_addr(self, addr):
        return dll.SetPullConsumerNameServerAddress(self._handle, addr.encode('utf-8'))

    def set_namesrv_domain(self, domain):
        return dll.SetPullConsumerNameServerDomain(self._handle, domain.encode('utf-8'))

    def set_session_credentials(self, access_key, access_secret, channel):
        return dll.SetPullConsumerSessionCredentials(self._handle, access_key.encode('utf-8'), access_secret.encode('utf-8'), channel.encode('utf-8'))

    def pull(self, topic):
        message_queue = ctypes.POINTER(_CMessageQueue)()
        queue_size = ctypes.c_int()
        dll.FetchSubscriptionMessageQueues(self._handle, topic.encode('utf-8'), ctypes.pointer(message_queue), ctypes.pointer(queue_size))
        for i in range(int(queue_size.value)):
            tmp_offset = ctypes.c_longlong()
            while True:
                pull_res = dll.Pull(self._handle, ctypes.pointer(message_queue[i]), b'*', tmp_offset, 32)
                if pull_res.pullStatus != _CPullStatus.BROKER_TIMEOUT:
                    tmp_offset = pull_res.nextBeginOffset
                if pull_res.pullStatus == _CPullStatus.FOUND:
                    for i in range(int(pull_res.size)):
                        yield RecvMessage(pull_res.msgFoundList[i])
                elif pull_res.pullStatus == _CPullStatus.NO_MATCHED_MSG:
                    break
                dll.ReleasePullResult(pull_res)
        dll.ReleaseSubscriptionMessageQueue(message_queue)
