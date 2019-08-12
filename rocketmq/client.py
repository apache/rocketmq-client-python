# -*- coding: utf-8 -*-
import sys
import ctypes
from ctypes import c_void_p, c_int, POINTER
from enum import IntEnum
from collections import namedtuple

from .ffi import (
    dll, _CSendResult, MSG_CALLBACK_FUNC, _CMessageQueue, _CPullStatus,
    _CConsumeStatus, MessageModel, QUEUE_SELECTOR_CALLBACK,
)
from .exceptions import (
    ffi_check, PushConsumerStartFailed, ProducerSendAsyncFailed,
    NullPointerException,
)
from .consts import MessageProperty


__all__ = ['SendStatus', 'Message', 'RecvMessage', 'Producer', 'PushConsumer', 'PullConsumer']

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str

SendResult = namedtuple('SendResult', ['status', 'msg_id', 'offset'])


class SendStatus(IntEnum):
    OK = 0
    FLUSH_DISK_TIMEOUT = 1
    FLUSH_SLAVE_TIMEOUT = 2
    SLAVE_NOT_AVAILABLE = 3


def _to_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


class Message(object):
    def __init__(self, topic):
        self._handle = dll.CreateMessage(_to_bytes(topic))

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyMessage(self._handle))

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
    if val:
        return val.decode('utf-8')


class RecvMessage(object):
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
        return '<RecvMessage topic={} id={} body={}>'.format(
            repr(self.topic),
            repr(self.id),
            repr(self.body),
        )


def hashing_queue_selector(mq_size, msg, arg):
    arg_int = ctypes.cast(arg, POINTER(c_int))
    return arg_int[0] % mq_size


class Producer(object):
    def __init__(self, group_id, timeout=None, compress_level=None, max_message_size=None):
        self._handle = dll.CreateProducer(_to_bytes(group_id))
        if self._handle is None:
            raise NullPointerException('CreateProducer returned null pointer')
        if timeout is not None:
            self.set_timeout(timeout)
        if compress_level is not None:
            self.set_compress_level(compress_level)
        if max_message_size is not None:
            self.set_max_message_size(max_message_size)
        self._callback_refs = []

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyProducer(self._handle))

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def send_sync(self, msg):
        cres = _CSendResult()
        ffi_check(dll.SendMessageSync(self._handle, msg, ctypes.pointer(cres)))
        return SendResult(
            SendStatus(cres.sendStatus),
            cres.msgId.decode('utf-8'),
            cres.offset
        )

    def send_async(self, msg, success_callback, exception_callback):
        from .ffi import SEND_SUCCESS_CALLBACK, SEND_EXCEPTION_CALLBACK

        def _on_success(csendres):
            try:
                if success_callback:
                    sendres = SendResult(
                        SendStatus(csendres.sendStatus),
                        csendres.msgId.decode('utf-8'),
                        csendres.offset
                    )
                    success_callback(sendres)
            finally:
                self._callback_refs.remove(on_success)

        def _on_exception(cexc):
            try:
                try:
                    raise ProducerSendAsyncFailed(cexc.msg, cexc.error, cexc.file, cexc.line, cexc.type)
                except ProducerSendAsyncFailed as exc:
                    if exception_callback:
                        exception_callback(exc)
                    else:
                        raise exc
            finally:
                self._callback_refs.remove(on_exception)

        on_success = SEND_SUCCESS_CALLBACK(_on_success)
        self._callback_refs.append(on_success)
        on_exception = SEND_EXCEPTION_CALLBACK(_on_exception)
        self._callback_refs.append(on_exception)
        ffi_check(dll.SendMessageAsync(self._handle, msg, on_success, on_exception))

    def send_oneway(self, msg):
        ffi_check(dll.SendMessageOneway(self._handle, msg))

    def send_oneway_orderly(self, msg, arg, queue_selector=hashing_queue_selector):
        def _select_queue(mq_size, cmsg, user_arg):
            msg = RecvMessage(cmsg)
            return queue_selector(mq_size, msg, user_arg)

        queue_select_callback = QUEUE_SELECTOR_CALLBACK(_select_queue)
        self._callback_refs.append(queue_select_callback)
        try:
            ffi_check(dll.SendMessageOnewayOrderly(
                self._handle,
                msg,
                queue_select_callback,
                ctypes.cast(ctypes.pointer(ctypes.c_int(arg)), c_void_p),
            ))
        finally:
            self._callback_refs.remove(queue_select_callback)

    def send_orderly(self, msg, arg,
                     retry_times=3,
                     queue_selector=hashing_queue_selector):
        def _select_queue(mq_size, cmsg, user_arg):
            msg = RecvMessage(cmsg)
            return queue_selector(mq_size, msg, user_arg)

        cres = _CSendResult()
        queue_select_callback = QUEUE_SELECTOR_CALLBACK(_select_queue)
        self._callback_refs.append(queue_select_callback)
        try:
            ffi_check(dll.SendMessageOrderly(
                self._handle,
                msg,
                queue_select_callback,
                ctypes.cast(ctypes.pointer(ctypes.c_int(arg)), c_void_p),
                retry_times,
                ctypes.pointer(cres)
            ))
        finally:
            self._callback_refs.remove(queue_select_callback)
        return SendResult(
            SendStatus(cres.sendStatus),
            cres.msgId.decode('utf-8'),
            cres.offset
        )

    def set_group(self, group_name):
        ffi_check(dll.SetProducerGroupName(_to_bytes(group_name)))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetProducerNameServerAddress(self._handle, _to_bytes(addr)))

    def set_namesrv_domain(self, domain):
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


class PushConsumer(object):
    def __init__(self, group_id, orderly=False, message_model=MessageModel.CLUSTERING):
        self._handle = dll.CreatePushConsumer(_to_bytes(group_id))
        if self._handle is None:
            raise NullPointerException('CreatePushConsumer returned null pointer')
        self._orderly = orderly
        self.set_message_model(message_model)
        self._callback_refs = []

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyPushConsumer(self._handle))

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def set_message_model(self, model):
        ffi_check(dll.SetPushConsumerMessageModel(self._handle, model))

    def start(self):
        ffi_check(dll.StartPushConsumer(self._handle))

    def shutdown(self):
        ffi_check(dll.ShutdownPushConsumer(self._handle))

    def set_group(self, group_id):
        ffi_check(dll.SetPushConsumerGroupID(_to_bytes(group_id)))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetPushConsumerNameServerAddress(self._handle, _to_bytes(addr)))

    def set_namesrv_domain(self, domain):
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
                callback(RecvMessage(msg))
            except Exception as e:
                exc = e
                return _CConsumeStatus.RECONSUME_LATER.value
            finally:
                if exc:
                    raise exc

            return _CConsumeStatus.CONSUME_SUCCESS.value

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


class PullConsumer(object):
    def __init__(self, group_id):
        self._handle = dll.CreatePullConsumer(_to_bytes(group_id))
        if self._handle is None:
            raise NullPointerException('CreatePullConsumer returned null pointer')

    def __del__(self):
        if self._handle is not None:
            ffi_check(dll.DestroyPullConsumer(self._handle))

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def start(self):
        ffi_check(dll.StartPullConsumer(self._handle))

    def shutdown(self):
        ffi_check(dll.ShutdownPullConsumer(self._handle))

    def set_group(self, group_id):
        ffi_check(dll.SetPullConsumerGroupID(_to_bytes(group_id)))

    def set_namesrv_addr(self, addr):
        ffi_check(dll.SetPullConsumerNameServerAddress(self._handle, _to_bytes(addr)))

    def set_namesrv_domain(self, domain):
        ffi_check(dll.SetPullConsumerNameServerDomain(self._handle, _to_bytes(domain)))

    def set_session_credentials(self, access_key, access_secret, channel):
        ffi_check(dll.SetPullConsumerSessionCredentials(
            self._handle,
            _to_bytes(access_key),
            _to_bytes(access_secret),
            _to_bytes(channel)
        ))

    def pull(self, topic, expression='*', max_num=32):
        message_queue = POINTER(_CMessageQueue)()
        queue_size = c_int()
        ffi_check(dll.FetchSubscriptionMessageQueues(
            self._handle,
            _to_bytes(topic),
            ctypes.pointer(message_queue),
            ctypes.pointer(queue_size)
        ))
        for i in range(int(queue_size.value)):
            tmp_offset = ctypes.c_longlong()
            while True:
                pull_res = dll.Pull(
                    self._handle,
                    ctypes.pointer(message_queue[i]),
                    _to_bytes(expression),
                    tmp_offset,
                    max_num,
                )
                if pull_res.pullStatus != _CPullStatus.BROKER_TIMEOUT:
                    tmp_offset = pull_res.nextBeginOffset
                if pull_res.pullStatus == _CPullStatus.FOUND:
                    for i in range(int(pull_res.size)):
                        yield RecvMessage(pull_res.msgFoundList[i])
                elif pull_res.pullStatus in [_CPullStatus.NO_MATCHED_MSG, _CPullStatus.NO_NEW_MSG, _CPullStatus.OFFSET_ILLEGAL]:
                    dll.ReleasePullResult(pull_res)  # NOTE: No need to check ffi return code here
                    break
                else:
                    dll.ReleasePullResult(pull_res)  # NOTE: No need to check ffi return code here
                    break
                dll.ReleasePullResult(pull_res)  # NOTE: No need to check ffi return code here
        ffi_check(dll.ReleaseSubscriptionMessageQueue(message_queue))
