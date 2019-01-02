# -*- coding: utf-8 -*-
import os
import ctypes
from ctypes import c_char, c_char_p, c_void_p, c_int, c_longlong, Structure, POINTER


CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DYLIB_PATH = os.path.join(CURR_DIR, 'librocketmq.dylib')
dll = ctypes.cdll.LoadLibrary(DYLIB_PATH)


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


class _CPullResult(Structure):
    _fields_ = [
        ('pullStatus', c_int),
        ('nextBeginOffset', c_longlong),
        ('minOffset', c_longlong),
        ('maxOffset', c_longlong),
        ('msgFoundList', c_void_p),
        ('size', c_int),
        ('pData', c_void_p),
    ]


# Message
dll.CreateMessage.argtypes = [c_char_p]
dll.CreateMessage.restype = c_void_p
dll.DestroyMessage.argtypes = [c_void_p]
dll.DestroyMessage.restype = c_int
dll.SetMessageKeys.argtypes = [c_void_p, c_char_p]
dll.SetMessageKeys.restype = c_int
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
