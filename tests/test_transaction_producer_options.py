# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ctypes
import os
import sys
import types
import unittest
from enum import IntEnum


class _RecordingDLL(object):
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def call(*args):
            self.calls.append((name, args))
            if name == 'CreateTransactionProducer':
                return 123
            if name in ('CreateProducer', 'CreateOrderlyProducer'):
                return 456
            return 0
        return call


class TransactionProducerOptionsTest(unittest.TestCase):
    def setUp(self):
        self.package_name = '_rocketmq_transaction_test_{}'.format(id(self))
        self.package = types.ModuleType(self.package_name)
        self.package.__path__ = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rocketmq'))]
        sys.modules[self.package_name] = self.package

        self.dll = _RecordingDLL()
        ffi = types.ModuleType(self.package_name + '.ffi')
        ffi.dll = self.dll
        ffi._CSendResult = type('_CSendResult', (ctypes.Structure,), {
            '_fields_': [('sendStatus', ctypes.c_int), ('msgId', ctypes.c_char * 256),
                         ('offset', ctypes.c_longlong)]
        })
        ffi.MSG_CALLBACK_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
        ffi.TRANSACTION_CHECK_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
                                                          ctypes.c_void_p)
        ffi.LOCAL_TRANSACTION_EXECUTE_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p,
                                                                 ctypes.c_void_p, ctypes.c_void_p)
        ffi.MessageModel = IntEnum('MessageModel', {'BROADCASTING': 0, 'CLUSTERING': 1})
        ffi.TraceModel = IntEnum('TraceModel', {'OPEN': 0, 'CLOSE': 1})
        sys.modules[ffi.__name__] = ffi

        exceptions = types.ModuleType(self.package_name + '.exceptions')
        exceptions.ffi_check = lambda status: None
        exceptions.NullPointerException = type('NullPointerException', (Exception,), {})
        sys.modules[exceptions.__name__] = exceptions

        consts = types.ModuleType(self.package_name + '.consts')
        consts.MessageProperty = type('MessageProperty', (), {})
        sys.modules[consts.__name__] = consts

        module_name = self.package_name + '.client'
        self.client = __import__(module_name, fromlist=[''])

    def tearDown(self):
        for module_name in list(sys.modules):
            if module_name == self.package_name or module_name.startswith(self.package_name + '.'):
                del sys.modules[module_name]

    def test_default_constructor_allocates_only_transaction_producer(self):
        producer = self.client.TransactionMQProducer(
            'transaction-group',
            lambda message: self.client.TransactionStatus.UNKNOWN,
        )

        calls = self.dll.calls
        self.assertEqual(producer._handle, 123)
        self.assertEqual([name for name, args in calls].count('CreateTransactionProducer'), 1)
        self.assertEqual([name for name, args in calls].count('CreateProducer'), 0)
        self.assertEqual([name for name, args in calls].count('CreateOrderlyProducer'), 0)
        self.assertEqual([name for name, args in calls if name.startswith('SetProducer')], [])

    def test_options_configure_only_transaction_producer(self):
        producer = self.client.TransactionMQProducer(
            'transaction-group',
            lambda message: self.client.TransactionStatus.UNKNOWN,
            timeout=1234,
            compress_level=3,
            max_message_size=2048,
        )

        calls = self.dll.calls
        self.assertEqual(producer._handle, 123)
        self.assertEqual([name for name, args in calls].count('CreateTransactionProducer'), 1)
        self.assertEqual([name for name, args in calls].count('CreateProducer'), 0)
        self.assertEqual([name for name, args in calls].count('CreateOrderlyProducer'), 0)
        self.assertEqual([args for name, args in calls if name == 'SetProducerSendMsgTimeout'], [(123, 1234)])
        self.assertEqual([args for name, args in calls if name == 'SetProducerCompressLevel'], [(123, 3)])
        self.assertEqual([args for name, args in calls if name == 'SetProducerMaxMessageSize'], [(123, 2048)])


if __name__ == '__main__':
    unittest.main()
