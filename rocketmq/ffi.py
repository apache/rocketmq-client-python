# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from ctypes.util import find_library
from ctypes import c_char, c_char_p, c_void_p, c_int, c_long, c_longlong, Structure, POINTER
from enum import IntEnum


_DYLIB_SUFFIX = '.so'
if sys.platform.lower() == 'darwin':
    _DYLIB_SUFFIX = '.dylib'
_CURR_DIR = os.path.abspath(os.path.dirname(__file__))
_PKG_DYLIB_PATH = os.path.join(_CURR_DIR, 'librocketmq' + _DYLIB_SUFFIX)
_DYLIB_PATH = find_library('rocketmq')
if os.path.exists(_PKG_DYLIB_PATH):
    # Prefer packaged librocketmq dylib
    _DYLIB_PATH = _PKG_DYLIB_PATH

dll = ctypes.cdll.LoadLibrary(_DYLIB_PATH)


class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class _CStatus(CtypesEnum):
    OK = 0
    NULL_POINTER = 1
    MALLOC_FAILED = 2
    # producer
    PRODUCER_START_FAILED = 10
    PRODUCER_SEND_SYNC_FAILED = 11
    PRODUCER_SEND_ONEWAY_FAILED = 12
    PRODUCER_SEND_ORDERLY_FAILED = 13
    PRODUCER_SEND_ASYNC_FAILED = 14
    # push consumer
    PUSHCONSUMER_START_FAILED = 20
    # pull consumer
    PULLCONSUMER_START_FAILED = 30
    PULLCONSUMER_FETCH_MQ_FAILED = 31
    PULLCONSUMER_FETCH_MESSAGE_FAILED = 32


class _CLogLevel(CtypesEnum):
    FATAL = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6
    LEVEL_NUM = 7


class MessageModel(CtypesEnum):
    BROADCASTING = 0
    CLUSTERING = 1


class _CSendResult(Structure):
    _fields_ = [
        ('sendStatus', c_int),
        ('msgId', c_char * 256),
        ('offset', c_longlong),
    ]


class _CMessageQueue(Structure):
    _fields_ = [
        ('topic', c_char * 512),
        ('brokerName', c_char * 256),
        ('queueId', c_int),
    ]


class _CMQException(Structure):
    _fields_ = [
        ('error', c_int),
        ('line', c_int),
        ('file', c_char * 512),
        ('msg', c_char * 512),
        ('type', c_char * 512),
    ]


class _CPullStatus(CtypesEnum):
    FOUND = 0
    NO_NEW_MSG = 1
    NO_MATCHED_MSG = 2
    OFFSET_ILLEGAL = 3
    BROKER_TIMEOUT = 4


class _CPullResult(Structure):
    _fields_ = [
        ('pullStatus', c_int),
        ('nextBeginOffset', c_longlong),
        ('minOffset', c_longlong),
        ('maxOffset', c_longlong),
        ('msgFoundList', POINTER(c_void_p)),
        ('size', c_int),
        ('pData', c_void_p),
    ]


class _CConsumeStatus(CtypesEnum):
    CONSUME_SUCCESS = 0
    RECONSUME_LATER = 1


# Message
dll.CreateMessage.argtypes = [c_char_p]
dll.CreateMessage.restype = c_void_p
dll.DestroyMessage.argtypes = [c_void_p]
dll.DestroyMessage.restype = _CStatus
dll.SetMessageKeys.argtypes = [c_void_p, c_char_p]
dll.SetMessageKeys.restype = _CStatus
dll.SetMessageTags.argtypes = [c_void_p, c_char_p]
dll.SetMessageTags.restype = _CStatus
dll.SetMessageBody.argtypes = [c_void_p, c_char_p]
dll.SetMessageBody.restype = _CStatus
dll.SetByteMessageBody.argtypes = [c_void_p, c_char_p, c_int]
dll.SetByteMessageBody.restype = _CStatus
dll.SetMessageProperty.argtypes = [c_void_p, c_char_p, c_char_p]
dll.SetMessageProperty.restype = _CStatus
dll.SetDelayTimeLevel.argtypes = [c_void_p, c_int]
dll.SetDelayTimeLevel.restype = _CStatus
dll.GetMessageTopic.argtypes = [c_void_p]
dll.GetMessageTopic.restype = c_char_p
dll.GetMessageTags.argtypes = [c_void_p]
dll.GetMessageTags.restype = c_char_p
dll.GetMessageKeys.argtypes = [c_void_p]
dll.GetMessageKeys.restype = c_char_p
dll.GetMessageBody.argtypes = [c_void_p]
dll.GetMessageBody.restype = c_char_p
dll.GetMessageProperty.argtypes = [c_void_p, c_char_p]
dll.GetMessageProperty.restype = c_char_p
dll.GetMessageId.argtypes = [c_void_p]
dll.GetMessageId.restype = c_char_p
dll.GetMessageDelayTimeLevel.argtypes = [c_void_p]
dll.GetMessageDelayTimeLevel.restype = c_int
dll.GetMessageQueueId.argtypes = [c_void_p]
dll.GetMessageQueueId.restype = c_int
dll.GetMessageReconsumeTimes.argtypes = [c_void_p]
dll.GetMessageReconsumeTimes.restype = c_int
dll.GetMessageStoreSize.argtypes = [c_void_p]
dll.GetMessageStoreSize.restype = c_int
dll.GetMessageBornTimestamp.argtypes = [c_void_p]
dll.GetMessageBornTimestamp.restype = c_longlong
dll.GetMessageStoreTimestamp.argtypes = [c_void_p]
dll.GetMessageStoreTimestamp.restype = c_longlong
dll.GetMessageQueueOffset.argtypes = [c_void_p]
dll.GetMessageQueueOffset.restype = c_longlong
dll.GetMessageCommitLogOffset.argtypes = [c_void_p]
dll.GetMessageCommitLogOffset.restype = c_longlong
dll.GetMessagePreparedTransactionOffset.argtypes = [c_void_p]
dll.GetMessagePreparedTransactionOffset.restype = c_longlong

# Producer

QUEUE_SELECTOR_CALLBACK = ctypes.CFUNCTYPE(c_int, c_int, c_void_p, c_void_p)
SEND_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, POINTER(_CSendResult))
SEND_EXCEPTION_CALLBACK = ctypes.CFUNCTYPE(None, _CMQException)

dll.CreateProducer.argtypes = [c_char_p]
dll.CreateProducer.restype = c_void_p
dll.DestroyProducer.argtypes = [c_void_p]
dll.DestroyProducer.restype = _CStatus
dll.StartProducer.argtypes = [c_void_p]
dll.StartProducer.restype = _CStatus
dll.ShutdownProducer.argtypes = [c_void_p]
dll.ShutdownProducer.restype = _CStatus
dll.SetProducerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetProducerNameServerAddress.restype = _CStatus
dll.SetProducerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetProducerNameServerDomain.restype = _CStatus
dll.SetProducerGroupName.argtypes = [c_void_p, c_char_p]
dll.SetProducerGroupName.restype = _CStatus
dll.SetProducerInstanceName.argtypes = [c_void_p, c_char_p]
dll.SetProducerInstanceName.restype = _CStatus
dll.SetProducerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetProducerSessionCredentials.restype = _CStatus
dll.SetProducerLogPath.argtypes = [c_void_p, c_char_p]
dll.SetProducerLogPath.restype = _CStatus
dll.SetProducerLogFileNumAndSize.argtypes = [c_void_p, c_int, c_long]
dll.SetProducerLogFileNumAndSize.restype = _CStatus
dll.SetProducerLogLevel.argtypes = [c_void_p, _CLogLevel]
dll.SetProducerLogLevel.restype = _CStatus
dll.SetProducerSendMsgTimeout.argtypes = [c_void_p, c_int]
dll.SetProducerSendMsgTimeout.restype = _CStatus
dll.SetProducerCompressLevel.argtypes = [c_void_p, c_int]
dll.SetProducerCompressLevel.restype = _CStatus
dll.SetProducerMaxMessageSize.argtypes = [c_void_p, c_int]
dll.SetProducerMaxMessageSize.restype = _CStatus
dll.SendMessageSync.argtypes = [c_void_p, c_void_p, POINTER(_CSendResult)]
dll.SendMessageSync.restype = _CStatus
dll.SendMessageAsync.argtypes = [c_void_p, c_void_p, SEND_SUCCESS_CALLBACK, SEND_EXCEPTION_CALLBACK]
dll.SendMessageAsync.restype = _CStatus
dll.SendMessageOneway.argtypes = [c_void_p, c_void_p]
dll.SendMessageOneway.restype = _CStatus
dll.SendMessageOrderly.argtypes = [c_void_p, c_void_p, QUEUE_SELECTOR_CALLBACK, c_void_p, c_int, POINTER(_CSendResult)]
dll.SendMessageOrderly.restype = _CStatus
dll.SendMessageOnewayOrderly.argtypes = [c_void_p, c_void_p, QUEUE_SELECTOR_CALLBACK, c_void_p]
dll.SendMessageOnewayOrderly.restype = _CStatus

# Pull Consumer
dll.CreatePullConsumer.argtypes = [c_char_p]
dll.CreatePullConsumer.restype = c_void_p
dll.DestroyPullConsumer.argtypes = [c_void_p]
dll.DestroyPullConsumer.restype = _CStatus
dll.StartPullConsumer.argtypes = [c_void_p]
dll.StartPullConsumer.restype = _CStatus
dll.ShutdownPullConsumer.argtypes = [c_void_p]
dll.ShutdownPullConsumer.restype = _CStatus
dll.SetPullConsumerGroupID.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerGroupID.restype = _CStatus
dll.GetPullConsumerGroupID.argtypes = [c_void_p]
dll.GetPullConsumerGroupID.restype = c_char_p
dll.SetPullConsumerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerNameServerAddress.restype = _CStatus
dll.SetPullConsumerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerNameServerDomain.restype = _CStatus
dll.SetPullConsumerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetPullConsumerSessionCredentials.restype = _CStatus
dll.SetPullConsumerLogPath.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerLogPath.restype = _CStatus
dll.SetPullConsumerLogFileNumAndSize.argtypes = [c_void_p, c_int, c_long]
dll.SetPullConsumerLogFileNumAndSize.restype = _CStatus
dll.SetPullConsumerLogLevel.argtypes = [c_void_p, _CLogLevel]
dll.SetPullConsumerLogLevel.restype = _CStatus
dll.FetchSubscriptionMessageQueues.argtypes = [c_void_p, c_char_p, POINTER(POINTER(_CMessageQueue)), POINTER(c_int)]
dll.FetchSubscriptionMessageQueues.restype = _CStatus
dll.ReleaseSubscriptionMessageQueue.argtypes = [POINTER(_CMessageQueue)]
dll.ReleaseSubscriptionMessageQueue.restype = _CStatus
dll.Pull.argtypes = [c_void_p, POINTER(_CMessageQueue), c_char_p, c_longlong, c_int]
dll.Pull.restype = _CPullResult
dll.ReleasePullResult.argtypes = [_CPullResult]
dll.ReleasePullResult.restype = _CStatus

# Push Consumer
MSG_CALLBACK_FUNC = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)
dll.CreatePushConsumer.argtypes = [c_char_p]
dll.CreatePushConsumer.restype = c_void_p
dll.DestroyPushConsumer.argtypes = [c_void_p]
dll.DestroyPushConsumer.restype = _CStatus
dll.StartPushConsumer.argtypes = [c_void_p]
dll.StartPushConsumer.restype = _CStatus
dll.ShutdownPushConsumer.argtypes = [c_void_p]
dll.ShutdownPushConsumer.restype = _CStatus
dll.SetPushConsumerGroupID.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerGroupID.restype = _CStatus
dll.GetPushConsumerGroupID.argtypes = [c_void_p]
dll.GetPushConsumerGroupID.restype = c_char_p
dll.SetPushConsumerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerNameServerAddress.restype = _CStatus
dll.SetPushConsumerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerNameServerDomain.restype = _CStatus
dll.Subscribe.argtypes = [c_void_p, c_char_p, c_char_p]
dll.Subscribe.restype = _CStatus
dll.RegisterMessageCallbackOrderly.argtypes = [c_void_p, MSG_CALLBACK_FUNC]
dll.RegisterMessageCallbackOrderly.restype = _CStatus
dll.RegisterMessageCallback.argtypes = [c_void_p, MSG_CALLBACK_FUNC]
dll.RegisterMessageCallback.restype = _CStatus
dll.UnregisterMessageCallbackOrderly.argtypes = [c_void_p]
dll.UnregisterMessageCallbackOrderly.restype = _CStatus
dll.UnregisterMessageCallback.argtypes = [c_void_p]
dll.UnregisterMessageCallback.restype = _CStatus
dll.SetPushConsumerThreadCount.argtypes = [c_void_p, c_int]
dll.SetPushConsumerThreadCount.restype = _CStatus
dll.SetPushConsumerMessageBatchMaxSize.argtypes = [c_void_p, c_int]
dll.SetPushConsumerMessageBatchMaxSize.restype = _CStatus
dll.SetPushConsumerInstanceName.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerInstanceName.restype = _CStatus
dll.SetPushConsumerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetPushConsumerSessionCredentials.restype = _CStatus
dll.SetPushConsumerLogPath.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerLogPath.restype = _CStatus
dll.SetPushConsumerLogFileNumAndSize.argtypes = [c_void_p, c_int, c_long]
dll.SetPushConsumerLogFileNumAndSize.restype = _CStatus
dll.SetPushConsumerLogLevel.argtypes = [c_void_p, _CLogLevel]
dll.SetPushConsumerLogLevel.restype = _CStatus
dll.SetPushConsumerMessageModel.argtypes = [c_void_p, MessageModel]
dll.SetPushConsumerMessageModel.restype = _CStatus
