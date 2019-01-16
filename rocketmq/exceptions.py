# -*- coding: utf-8 -*-
from .ffi import _CStatus


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
    raise exc_cls()


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


@_register(_CStatus.PUSHCONSUMER_START_FAILED)
class PushConsumerStartFailed(ConsumerException):
    pass


@_register(_CStatus.PULLCONSUMER_START_FAILED)
class PullConsumerStartFailed(ConsumerException):
    pass


@_register(_CStatus.PULLCONSUMER_FETCH_MQ_FAILED)
class PullConsumerFetchMQFailed(ConsumerException):
    pass


@_register(_CStatus.PULLCONSUMER_FETCH_MQ_FAILED)
class PullConsumerFetchMessageFailed(ConsumerException):
    pass