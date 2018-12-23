/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "CCommon.h"
#include "CMessage.h"
#include "CMessageExt.h"
#include "CSendResult.h"
#include "CProducer.h"
#include "CPushConsumer.h"
#include "PythonWrapper.h"
#include <boost/python.hpp>
#include <boost/thread.hpp>
#include <map>

using namespace boost::python;
using namespace std;

const char *VERSION =
        "PYTHON_CLIENT_VERSION: " PYTHON_CLIENT_VERSION ", BUILD DATE: " PYCLI_BUILD_DATE " ";

map<CPushConsumer *, PyObject *> g_CallBackMap;

class PyThreadStateLock {
public:
    PyThreadStateLock() {
        state = PyGILState_Ensure();
    }

    ~PyThreadStateLock() {
        // NOTE: 必须跟 PyGILState_Ensure 成对出现，否则可能出现死锁!!!
        PyGILState_Release(state);
    }

private:
    PyGILState_STATE state;
};

class PyThreadStateUnlock {
public:
    PyThreadStateUnlock() : _save(NULL) {
        Py_UNBLOCK_THREADS
    }

    ~PyThreadStateUnlock() {
        Py_BLOCK_THREADS
    }

private:
    PyThreadState *_save;
};

#ifdef __cplusplus
extern "C" {
#endif
void *PyCreateMessage(const char *topic) {

    return (void *) CreateMessage(topic);
}

int PyDestroyMessage(void *msg) {
    return DestroyMessage((CMessage *) msg);
}
int PySetMessageTopic(void *msg, const char *topic) {
    return SetMessageTopic((CMessage *) msg, topic);
}
int PySetMessageTags(void *msg, const char *tags) {
    return SetMessageTags((CMessage *) msg, tags);
}
int PySetMessageKeys(void *msg, const char *keys) {
    return SetMessageKeys((CMessage *) msg, keys);
}
int PySetMessageBody(void *msg, const char *body) {
    return SetMessageBody((CMessage *) msg, body);
}
int PySetByteMessageBody(void *msg, const char *body, int len) {
    return SetByteMessageBody((CMessage *) msg, body, len);
}
int PySetMessageProperty(void *msg, const char *key, const char *value) {
    return SetMessageProperty((CMessage *) msg, key, value);
}
int PySetMessageDelayTimeLevel(void *msg, int level) {
    return SetDelayTimeLevel((CMessage *) msg, level);
}
//messageExt
const char *PyGetMessageTopic(PyMessageExt msgExt) {
    return GetMessageTopic((CMessageExt *) msgExt.pMessageExt);
}
const char *PyGetMessageTags(PyMessageExt msgExt) {
    return GetMessageTags((CMessageExt *) msgExt.pMessageExt);
}
const char *PyGetMessageKeys(PyMessageExt msgExt) {
    return GetMessageKeys((CMessageExt *) msgExt.pMessageExt);
}
const char *PyGetMessageBody(PyMessageExt msgExt) {
    return GetMessageBody((CMessageExt *) msgExt.pMessageExt);
}
const char *PyGetMessageProperty(PyMessageExt msgExt, const char *key) {
    return GetMessageProperty((CMessageExt *) msgExt.pMessageExt, key);
}
const char *PyGetMessageId(PyMessageExt msgExt) {
    return GetMessageId((CMessageExt *) msgExt.pMessageExt);
}

//producer
void *PyCreateProducer(const char *groupId) {
    return (void *) CreateProducer(groupId);
}
int PyDestroyProducer(void *producer) {
    return DestroyProducer((CProducer *) producer);
}
int PyStartProducer(void *producer) {
    return StartProducer((CProducer *) producer);
}
int PyShutdownProducer(void *producer) {
    return ShutdownProducer((CProducer *) producer);
}
int PySetProducerNameServerAddress(void *producer, const char *namesrv) {
    return SetProducerNameServerAddress((CProducer *) producer, namesrv);
}
int PySetProducerNameServerDomain(void *producer, const char *domain) {
    return SetProducerNameServerDomain((CProducer *) producer, domain);
}
int PySetProducerInstanceName(void *producer, const char *instanceName) {
    return SetProducerInstanceName((CProducer *)producer, instanceName);
}
int PySetProducerSessionCredentials(void *producer, const char *accessKey, const char *secretKey, const char *channel) {
    return SetProducerSessionCredentials((CProducer *)producer, accessKey, secretKey, channel);
}
PySendResult PySendMessageSync(void *producer, void *msg) {
    PySendResult ret;
    CSendResult result;
    SendMessageSync((CProducer *) producer, (CMessage *) msg, &result);
    ret.sendStatus = result.sendStatus;
    ret.offset = result.offset;
    strncpy(ret.msgId, result.msgId, MAX_MESSAGE_ID_LENGTH - 1);
    ret.msgId[MAX_MESSAGE_ID_LENGTH - 1] = 0;
    return ret;
}

int PySendMessageOneway(void *producer, void *msg) {
    return SendMessageOneway((CProducer *) producer, (CMessage *) msg);
}

//SendResult
const char *PyGetSendResultMsgID(CSendResult &sendResult) {
    return (const char *) (sendResult.msgId);
}
//consumer
void *PyCreatePushConsumer(const char *groupId) {
    PyEval_InitThreads();  // 因为从 C 中发起对 python 的回调，确保初始化对多线程的支持（主要是创建GIL）
    return (void *) CreatePushConsumer(groupId);
}
int PyDestroyPushConsumer(void *consumer) {
    CPushConsumer *consumerInner = (CPushConsumer *) consumer;
    map<CPushConsumer *, pair<PyObject *, object>>::iterator iter;
    iter = g_CallBackMap.find(consumerInner);
    if (iter != g_CallBackMap.end()) {
        UnregisterMessageCallback(consumerInner);
        g_CallBackMap.erase(iter);
    }
    return DestroyPushConsumer(consumerInner);
}
int PyStartPushConsumer(void *consumer) {
    return StartPushConsumer((CPushConsumer *) consumer);
}
int PyShutdownPushConsumer(void *consumer) {
    PyThreadStateUnlock PyThreadUnlock;  // 存在阻塞调用，确保线程不持有 GIL
    return ShutdownPushConsumer((CPushConsumer *) consumer);
}
int PySetPushConsumerNameServerAddress(void *consumer, const char *namesrv) {
    return SetPushConsumerNameServerAddress((CPushConsumer *) consumer, namesrv);
}
int PySetPushConsumerNameServerDomain(void *consumer, const char *domain){
    return SetPushConsumerNameServerDomain((CPushConsumer *) consumer, domain);
}
int PySubscribe(void *consumer, const char *topic, const char *expression) {
    return Subscribe((CPushConsumer *) consumer, topic, expression);
}
int PyRegisterMessageCallback(void *consumer, PyObject *pCallback, object args) {
    CPushConsumer *consumerInner = (CPushConsumer *) consumer;
    g_CallBackMap[consumerInner] = make_pair(pCallback, std::move(args));
    return RegisterMessageCallback(consumerInner, &PythonMessageCallBackInner);
}

int PythonMessageCallBackInner(CPushConsumer *consumer, CMessageExt *msg) {
    boost::this_thread::disable_interruption di;  // 调用 python 回调，线程不应被中断
    PyThreadStateLock PyThreadLock;  // 调用 python 回调，确保线程持有 GIL
    PyMessageExt message = { .pMessageExt = msg };
    map<CPushConsumer *, pair<PyObject *, object>>::iterator iter;
    iter = g_CallBackMap.find(consumer);
    if (iter != g_CallBackMap.end()) {
        pair<PyObject *, object> callback = iter->second;
        PyObject * pCallback = callback.first;
        object& args = callback.second;
        if (pCallback != NULL) {
            int status = boost::python::call<int>(pCallback, message, args);
            return status;
        }
    }
    return 1;
}

int PySetPushConsumerThreadCount(void *consumer, int threadCount) {
    return SetPushConsumerThreadCount((CPushConsumer *) consumer, threadCount);
}
int PySetPushConsumerMessageBatchMaxSize(void *consumer, int batchSize) {
    return SetPushConsumerMessageBatchMaxSize((CPushConsumer *) consumer, batchSize);
}
int PySetPushConsumerInstanceName(void *consumer, const char *instanceName){
    return SetPushConsumerInstanceName((CPushConsumer *)consumer, instanceName);
}
int PySetPushConsumerSessionCredentials(void *consumer, const char *accessKey, const char *secretKey,
                                       const char *channel){
    return SetPushConsumerSessionCredentials((CPushConsumer *)consumer, accessKey, secretKey, channel);
}

//push consumer
int PySetPullConsumerNameServerDomain(void *consumer, const char *domain) {
    return SetPullConsumerNameServerDomain((CPullConsumer *) consumer, domain);
}
//version
const char *PyGetVersion() {
    return VERSION;
}
#ifdef __cplusplus
};
#endif
BOOST_PYTHON_MODULE (librocketmqclientpython) {
/*
    class_<CMessage>("CMessage");
    class_<CMessageExt>("CMessageExt");
    class_<CProducer>("CProducer");
    class_<CPushConsumer>("CPushConsumer");
*/
    enum_<CStatus>("CStatus")
            .value("OK", OK)
            .value("NULL_POINTER", NULL_POINTER);

    enum_<CSendStatus>("CSendStatus")
            .value("E_SEND_OK", E_SEND_OK)
            .value("E_SEND_FLUSH_DISK_TIMEOUT", E_SEND_FLUSH_DISK_TIMEOUT)
            .value("E_SEND_FLUSH_SLAVE_TIMEOUT", E_SEND_FLUSH_SLAVE_TIMEOUT)
            .value("E_SEND_SLAVE_NOT_AVAILABLE", E_SEND_SLAVE_NOT_AVAILABLE);

    enum_<CConsumeStatus>("CConsumeStatus")
            .value("E_CONSUME_SUCCESS", E_CONSUME_SUCCESS)
            .value("E_RECONSUME_LATER", E_RECONSUME_LATER);

    class_<PySendResult>("SendResult")
            .def_readonly("offset", &PySendResult::offset, "offset")
                    //.def_readonly("msgId", &PySendResult::msgId, "msgId")
            .def_readonly("sendStatus", &PySendResult::sendStatus, "sendStatus")
            .def("GetMsgId", &PySendResult::GetMsgId);
    class_<PyMessageExt>("CMessageExt");

    //For Message
    def("CreateMessage", PyCreateMessage, return_value_policy<return_opaque_pointer>());
    def("DestroyMessage", PyDestroyMessage);
    def("SetMessageTopic", PySetMessageTopic);
    def("SetMessageTags", PySetMessageTags);
    def("SetMessageKeys", PySetMessageKeys);
    def("SetMessageBody", PySetMessageBody);
    def("SetByteMessageBody", PySetByteMessageBody);
    def("SetMessageProperty", PySetMessageProperty);
    def("SetDelayTimeLevel", PySetMessageDelayTimeLevel);

    //For MessageExt
    def("GetMessageTopic", PyGetMessageTopic);
    def("GetMessageTags", PyGetMessageTags);
    def("GetMessageKeys", PyGetMessageKeys);
    def("GetMessageBody", PyGetMessageBody);
    def("GetMessageProperty", PyGetMessageProperty);
    def("GetMessageId", PyGetMessageId);

    //For producer
    def("CreateProducer", PyCreateProducer, return_value_policy<return_opaque_pointer>());
    def("DestroyProducer", PyDestroyProducer);
    def("StartProducer", PyStartProducer);
    def("ShutdownProducer", PyShutdownProducer);
    def("SetProducerNameServerAddress", PySetProducerNameServerAddress);
    def("SetProducerNameServerDomain", PySetProducerNameServerDomain);
    def("SetProducerInstanceName", PySetProducerInstanceName);
    def("SetProducerSessionCredentials", PySetProducerSessionCredentials);
    def("SendMessageSync", PySendMessageSync);
    def("SendMessageOneway", PySendMessageOneway);

    //For Consumer
    def("CreatePushConsumer", PyCreatePushConsumer, return_value_policy<return_opaque_pointer>());
    def("DestroyPushConsumer", PyDestroyPushConsumer);
    def("StartPushConsumer", PyStartPushConsumer);
    def("ShutdownPushConsumer", PyShutdownPushConsumer);
    def("SetPushConsumerNameServerAddress", PySetPushConsumerNameServerAddress);
    def("SetPushConsumerNameServerDomain", PySetPushConsumerNameServerDomain);
    def("SetPushConsumerThreadCount", PySetPushConsumerThreadCount);
    def("SetPushConsumerMessageBatchMaxSize", PySetPushConsumerMessageBatchMaxSize);
    def("SetPushConsumerInstanceName", PySetPushConsumerInstanceName);
    def("SetPushConsumerSessionCredentials", PySetPushConsumerSessionCredentials);
    def("Subscribe", PySubscribe);
    def("RegisterMessageCallback", PyRegisterMessageCallback);

    //pull consumer
    def("SetPullConsumerNameServerDomain", PySetPullConsumerNameServerDomain);

    //For Version
    def("GetVersion", PyGetVersion);
}

