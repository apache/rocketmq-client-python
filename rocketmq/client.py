# -*- coding: utf-8 -*-
import ctypes
from collections import namedtuple

from .ffi import dll, _CSendResult


SendResult = namedtuple('SendResult', ['status', 'msg_id', 'offset'])


class Message(object):
    def __init__(self, topic):
        self._handle = dll.CreateMessage(topic.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            dll.DestroyMessage(self._handle)

    def set_keys(self, keys):
        return dll.SetMessageKeys(self._handle, keys.encode('utf-8'))

    def set_body(self, body):
        return dll.SetMessageBody(self._handle, body.encode('utf-8'))

    def set_property(self, key, value):
        return dll.SetMessageProperty(self._handle, key.encode('utf-8'), value.encode('utf-8'))

    @property
    def _as_parameter_(self):
        return self._handle


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
    def __init__(self, group_id):
        self._handle = dll.CreatePushConsumer(group_id.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            dll.DestroyPushConsumer(self._handle)

    def start(self):
        dll.StartPushConsumer(self._handle)

    def shutdown(self):
        dll.ShutdownPushConsumer(self._handle)

    def set_group(self, group_id):
        return dll.SetPushConsumerGroupID(group_id.encode('utf-8'))

    def set_namesrv_addr(self, addr):
        return dll.SetPushConsumerNameServerAddress(self._handle, addr.encode('utf-8'))

    def set_namesrv_domain(self, domain):
        return dll.SetPushConsumerNameServerDomain(self._handle, domain.encode('utf-8'))

    def set_session_credentials(self, access_key, access_secret, channel):
        return dll.SetPushConsumerSessionCredentials(self._handle, access_key.encode('utf-8'), access_secret.encode('utf-8'), channel.encode('utf-8'))

    def subscribe(self, topic, expression):
        return dll.Subscribe(self._handle, topic.encode('utf-8'), expression.encode('utf-8'))

    def register_callback(self, callback, orderly=False):
        from .ffi import MSG_CALLBACK_FUNC

        if orderly:
            register_func = dll.RegisterMessageCallbackOrderly
        else:
            register_func = dll.RegisterMessageCallback
        return register_func(self._handle, MSG_CALLBACK_FUNC(callback))

    def unregister_callback(self, orderly=False):
        if orderly:
            return dll.UnregisterMessageCallbackOrderly(self._handle)
        return dll.UnregisterMessageCallback(self._handle)

    def set_thread_count(self, thread_count):
        return dll.SetPushConsumerThreadCount(self._handle, thread_count)

    def set_message_batch_max_size(self, max_size):
        return dll.SetPushConsumerMessageBatchMaxSize(self._handle, max_size)

    def set_instance_name(self, name):
        return dll.SetPushConsumerInstanceName(self._handle, name.encode('utf-8'))
