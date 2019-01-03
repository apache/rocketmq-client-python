# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from ctypes import c_char, c_char_p, c_void_p, c_int, c_long, c_longlong, Structure, POINTER
from enum import IntEnum


_DYLIB_NAMES = {
    'darwin': 'librocketmq.dylib',
    'linux': 'librocketmq.so',
}
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DYLIB_PATH = os.path.join(CURR_DIR, _DYLIB_NAMES[sys.platform.lower()])
dll = ctypes.cdll.LoadLibrary(DYLIB_PATH)


class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class _CStatus(CtypesEnum):
    OK = 0
    NULL_POINTER = 1
    MALLOC_FAILED = 2
    PRODUCER_ERROR_CODE_START = 10
    PRODUCER_START_FAILED = 10
    PRODUCER_SEND_SYNC_FAILED = 11
    PRODUCER_SEND_ONEWAY_FAILED = 12
    PRODUCER_SEND_ORDERLY_FAILED = 13
    PUSHCONSUMER_ERROR_CODE_START = 20
    PUSHCONSUMER_START_FAILED = 20
    PULLCONSUMER_ERROR_CODE_START = 30
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


class _CSendStatus(CtypesEnum):
    OK = 0
    FLUSH_DISK_TIMEOUT = 1
    FLUSH_SLAVE_TIMEOUT = 2
    SLAVE_NOT_AVAILABLE = 3


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
dll.DestroyMessage.restype = c_int
dll.SetMessageKeys.argtypes = [c_void_p, c_char_p]
dll.SetMessageKeys.restype = c_int
dll.SetMessageTags.argtypes = [c_void_p, c_char_p]
dll.SetMessageTags.restype = c_int
dll.SetMessageBody.argtypes = [c_void_p, c_char_p]
dll.SetMessageBody.restype = c_int
dll.SetByteMessageBody.argtypes = [c_void_p, c_char_p, c_int]
dll.SetByteMessageBody.restype = c_int
dll.SetMessageProperty.argtypes = [c_void_p, c_char_p, c_char_p]
dll.SetMessageProperty.restype = c_int
dll.SetDelayTimeLevel.argtypes = [c_void_p, c_int]
dll.SetDelayTimeLevel.restype = c_int
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
dll.CreateProducer.argtypes = [c_char_p]
dll.CreateProducer.restype = c_void_p
dll.DestroyProducer.argtypes = [c_void_p]
dll.DestroyProducer.restype = c_int
dll.StartProducer.argtypes = [c_void_p]
dll.StartProducer.restype = c_int
dll.ShutdownProducer.argtypes = [c_void_p]
dll.ShutdownProducer.restype = c_int
dll.SetProducerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetProducerNameServerAddress.restype = c_int
dll.SetProducerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetProducerNameServerDomain.restype = c_int
dll.SetProducerGroupName.argtypes = [c_void_p, c_char_p]
dll.SetProducerGroupName.restype = c_int
dll.SetProducerInstanceName.argtypes = [c_void_p, c_char_p]
dll.SetProducerInstanceName.restype = c_int
dll.SetProducerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetProducerSessionCredentials.restype = c_int
dll.SendMessageSync.argtypes = [c_void_p, c_void_p, POINTER(_CSendResult)]
dll.SendMessageSync.restype = c_int
dll.SendMessageOneway.argtypes = [c_void_p, c_void_p]
dll.SendMessageOneway.restype = c_int

# Pull Consumer
dll.CreatePullConsumer.argtypes = [c_char_p]
dll.CreatePullConsumer.restype = c_void_p
dll.DestroyPullConsumer.argtypes = [c_void_p]
dll.DestroyPullConsumer.restype = c_int
dll.StartPullConsumer.argtypes = [c_void_p]
dll.StartPullConsumer.restype = c_int
dll.ShutdownPullConsumer.argtypes = [c_void_p]
dll.ShutdownPullConsumer.restype = c_int
dll.SetPullConsumerGroupID.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerGroupID.restype = c_int
dll.GetPullConsumerGroupID.argtypes = [c_void_p]
dll.GetPullConsumerGroupID.restype = c_char_p
dll.SetPullConsumerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerNameServerAddress.restype = c_int
dll.SetPullConsumerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerNameServerDomain.restype = c_int
dll.SetPullConsumerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetPullConsumerSessionCredentials.restype = c_int
dll.SetPullConsumerLogPath.argtypes = [c_void_p, c_char_p]
dll.SetPullConsumerLogPath.restype = c_int
dll.SetPullConsumerLogFileNumAndSize.argtypes = [c_void_p, c_int, c_long]
dll.SetPullConsumerLogFileNumAndSize.restype = c_int
dll.SetPullConsumerLogLevel.argtypes = [c_void_p, _CLogLevel]
dll.SetPullConsumerLogLevel.restype = c_int
dll.FetchSubscriptionMessageQueues.argtypes = [c_void_p, c_char_p, POINTER(POINTER(_CMessageQueue)), POINTER(c_int)]
dll.FetchSubscriptionMessageQueues.restype = c_int
dll.ReleaseSubscriptionMessageQueue.argtypes = [POINTER(_CMessageQueue)]
dll.Pull.argtypes = [c_void_p, POINTER(_CMessageQueue), c_char_p, c_longlong, c_int]
dll.Pull.restype = _CPullResult
dll.ReleasePullResult.argtypes = [_CPullResult]
dll.ReleasePullResult.restype = c_int

# Push Consumer
MSG_CALLBACK_FUNC = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)
dll.CreatePushConsumer.argtypes = [c_char_p]
dll.CreatePushConsumer.restype = c_void_p
dll.DestroyPushConsumer.argtypes = [c_void_p]
dll.DestroyPushConsumer.restype = c_int
dll.StartPushConsumer.argtypes = [c_void_p]
dll.StartPushConsumer.restype = c_int
dll.ShutdownPushConsumer.argtypes = [c_void_p]
dll.ShutdownPushConsumer.restype = c_int
dll.SetPushConsumerGroupID.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerGroupID.restype = c_int
dll.GetPushConsumerGroupID.argtypes = [c_void_p]
dll.GetPushConsumerGroupID.restype = c_char_p
dll.SetPushConsumerNameServerAddress.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerNameServerAddress.restype = c_int
dll.SetPushConsumerNameServerDomain.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerNameServerDomain.restype = c_int
dll.Subscribe.argtypes = [c_void_p, c_char_p, c_char_p]
dll.Subscribe.restype = c_int
dll.RegisterMessageCallbackOrderly.argtypes = [c_void_p, MSG_CALLBACK_FUNC]
dll.RegisterMessageCallbackOrderly.restype = c_int
dll.RegisterMessageCallback.argtypes = [c_void_p, MSG_CALLBACK_FUNC]
dll.RegisterMessageCallback.restype = c_int
dll.UnregisterMessageCallbackOrderly.argtypes = [c_void_p]
dll.UnregisterMessageCallbackOrderly.restype = c_int
dll.UnregisterMessageCallback.argtypes = [c_void_p]
dll.UnregisterMessageCallback.restype = c_int
dll.SetPushConsumerThreadCount.argtypes = [c_void_p, c_int]
dll.SetPushConsumerThreadCount.restype = c_int
dll.SetPushConsumerMessageBatchMaxSize.argtypes = [c_void_p, c_int]
dll.SetPushConsumerMessageBatchMaxSize.restype = c_int
dll.SetPushConsumerInstanceName.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerInstanceName.restype = c_int
dll.SetPushConsumerSessionCredentials.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.SetPushConsumerSessionCredentials.restype = c_int
dll.SetPushConsumerLogPath.argtypes = [c_void_p, c_char_p]
dll.SetPushConsumerLogPath.restype = c_int
dll.SetPushConsumerLogFileNumAndSize.argtypes = [c_void_p, c_int, c_long]
dll.SetPushConsumerLogFileNumAndSize.restype = c_int
dll.SetPushConsumerLogLevel.argtypes = [c_void_p, _CLogLevel]
dll.SetPushConsumerLogLevel.restype = c_int
dll.SetPushConsumerMessageModel.argtypes = [c_void_p, MessageModel]
dll.SetPushConsumerMessageModel.restype = c_int
