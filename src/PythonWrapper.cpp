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
#include "CMQException.h"
#include <boost/python.hpp>
#include <map>

using namespace boost::python;
using namespace std;

const char *VERSION =
        "PYTHON_CLIENT_VERSION: " PYTHON_CLIENT_VERSION ", BUILD DATE: " PYCLI_BUILD_DATE " ";

map<CPushConsumer *, pair<PyObject *, object>> g_CallBackMap;
map<CProducer *, PyObject *> g_TransactionCheckCallBackMap;


class PyThreadStateLock {
public:
    PyThreadStateLock() {
        state = PyGILState_Ensure();
    }

    ~PyThreadStateLock() {
        // NOTE: must paired with PyGILState_Ensure, otherwise it will cause deadlock!!!
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
    PyEval_InitThreads();  // ensure create GIL, for call Python callback from C.
    return (void *) CreateProducer(groupId);
}

void *PyCreateTransactionProducer(const char *groupId, PyObject *localTransactionCheckerCallback) {
    PyEval_InitThreads();
    CProducer *producer = CreateTransactionProducer(groupId, &PyLocalTransactionCheckerCallback, NULL);
    g_TransactionCheckCallBackMap[producer] = localTransactionCheckerCallback;
    return producer;
}

CTransactionStatus PyLocalTransactionCheckerCallback(CProducer *producer, CMessageExt *msg, void *data) {
    PyThreadStateLock pyThreadLock;  // ensure hold GIL, before call python callback
    PyMessageExt message = {.pMessageExt = msg};
    map<CProducer *, PyObject *>::iterator iter;
    iter = g_TransactionCheckCallBackMap.find(producer);
    if (iter != g_TransactionCheckCallBackMap.end()) {
        PyObject *pCallback = iter->second;
        CTransactionStatus status = boost::python::call<CTransactionStatus>(pCallback, message);
        return status;
    }
    return CTransactionStatus::E_UNKNOWN_TRANSACTION;
}

int PyDestroyProducer(void *producer) {
    return DestroyProducer((CProducer *) producer);
}
int PyStartProducer(void *producer) {
    return StartProducer((CProducer *) producer);
}
int PyShutdownProducer(void *producer) {
    PyThreadStateUnlock PyThreadUnlock;  // Shutdown Producer is a block call, ensure thread don't hold GIL.
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
int PySetProducerCompressLevel(void *producer, int level) {
    return SetProducerCompressLevel((CProducer *)producer, level);
}
int PySetProducerMaxMessageSize(void *producer, int size) {
    return SetProducerMaxMessageSize((CProducer *)producer, size);
}
int PySetProducerLogPath(void *producer, const char *logPath) {
    return SetProducerLogPath((CProducer *) producer, logPath);
}
int PySetProducerLogFileNumAndSize(void *producer, int fileNum, long fileSize) {
    return SetProducerLogFileNumAndSize((CProducer *) producer, fileNum, fileSize);
}
int PySetProducerLogLevel(void *producer, CLogLevel level) {
    return SetProducerLogLevel((CProducer *) producer, level);
}
int PySetProducerSendMsgTimeout(void *producer, int timeout) {
    return SetProducerSendMsgTimeout((CProducer *) producer, timeout);
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

void PySendSuccessCallback(CSendResult result, CMessage *msg, void *pyCallback) {
    PyThreadStateLock PyThreadLock;  // ensure hold GIL, before call python callback
    PySendResult sendResult;
    sendResult.sendStatus = result.sendStatus;
    sendResult.offset = result.offset;
    strncpy(sendResult.msgId, result.msgId, MAX_MESSAGE_ID_LENGTH - 1);
    sendResult.msgId[MAX_MESSAGE_ID_LENGTH - 1] = 0;
    PyCallback *callback = (PyCallback *) pyCallback;
    boost::python::call<void>(callback->successCallback, sendResult, (void *) msg);
    delete pyCallback;
}


void PySendExceptionCallback(CMQException e, CMessage *msg, void *pyCallback) {
    PyThreadStateLock PyThreadLock;  // ensure hold GIL, before call python callback
    PyMQException exception;
    PyCallback *callback = (PyCallback *) pyCallback;
    exception.error = e.error;
    exception.line = e.line;
    strncpy(exception.file, e.file, MAX_EXEPTION_FILE_LENGTH - 1);
    exception.file[MAX_EXEPTION_FILE_LENGTH - 1] = 0;
    strncpy(exception.msg, e.msg, MAX_EXEPTION_MSG_LENGTH - 1);
    exception.msg[MAX_EXEPTION_MSG_LENGTH - 1] = 0;
    strncpy(exception.type, e.type, MAX_EXEPTION_TYPE_LENGTH - 1);
    exception.type[MAX_EXEPTION_TYPE_LENGTH - 1] = 0;
    boost::python::call<void>(callback->exceptionCallback, (void *) msg, exception);
    delete pyCallback;
}

int PySendMessageAsync(void *producer, void *msg, PyObject *sendSuccessCallback, PyObject *sendExceptionCallback) {
    PyCallback *pyCallback = new PyCallback();
    pyCallback->successCallback = sendSuccessCallback;
    pyCallback->exceptionCallback = sendExceptionCallback;
    return SendAsync((CProducer *) producer, (CMessage *) msg, &PySendSuccessCallback, &PySendExceptionCallback,
                     (void *) pyCallback);
}


PySendResult PySendMessageOrderly(void *producer, void *msg, int autoRetryTimes, void *args, PyObject *queueSelector) {
    PySendResult ret;
    CSendResult result;
    PyUserData userData = {queueSelector, args};
    SendMessageOrderly((CProducer *) producer, (CMessage *) msg, &PyOrderlyCallbackInner, &userData, autoRetryTimes,
                       &result);
    ret.sendStatus = result.sendStatus;
    ret.offset = result.offset;
    strncpy(ret.msgId, result.msgId, MAX_MESSAGE_ID_LENGTH - 1);
    ret.msgId[MAX_MESSAGE_ID_LENGTH - 1] = 0;
    return ret;
}

int PyOrderlyCallbackInner(int size, CMessage *msg, void *args) {
    PyUserData *userData = (PyUserData *) args;
    int index = boost::python::call<int>(userData->pyObject, size, (void *) msg, userData->pData);
    return index;
}

PySendResult PySendMessageOrderlyByShardingKey(void *producer, void *msg, const char *shardingKey) {
    PySendResult ret;
    CSendResult result;
    SendMessageOrderlyByShardingKey((CProducer *) producer, (CMessage *) msg, shardingKey, &result);
    ret.sendStatus = result.sendStatus;
    ret.offset = result.offset;
    strncpy(ret.msgId, result.msgId, MAX_MESSAGE_ID_LENGTH - 1);
    ret.msgId[MAX_MESSAGE_ID_LENGTH - 1] = 0;
    return ret;
}

CTransactionStatus PyLocalTransactionExecuteCallback(CProducer *producer, CMessage *msg, void *data) {
    PyUserData *localCallback = (PyUserData *) data;
    CTransactionStatus status = boost::python::call<CTransactionStatus>(localCallback->pyObject, (void *) msg,
                                                                        localCallback->pData);
    return status;
}

PySendResult PySendMessageInTransaction(void *producer, void *msg, PyObject *localTransactionCallback, void *args) {
    PyUserData userData = {localTransactionCallback, args};
    PySendResult ret;
    CSendResult result;
    SendMessageTransaction((CProducer *) producer, (CMessage *) msg, &PyLocalTransactionExecuteCallback, &userData,
                           &result);
    ret.sendStatus = result.sendStatus;
    ret.offset = result.offset;
    strncpy(ret.msgId, result.msgId, MAX_MESSAGE_ID_LENGTH - 1);
    ret.msgId[MAX_MESSAGE_ID_LENGTH - 1] = 0;
    return ret;
}

//SendResult
const char *PyGetSendResultMsgID(CSendResult &sendResult) {
    return (const char *) (sendResult.msgId);
}
//consumer
void *PyCreatePushConsumer(const char *groupId) {
    PyEval_InitThreads();  // ensure create GIL, for call Python callback from C.
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
int PyDestroyTransactionProducer(void *producer) {
    CProducer *producerInner = (CProducer *) producer;
    map<CProducer *, PyObject *>::iterator iter;
    iter = g_TransactionCheckCallBackMap.find(producerInner);
    if (iter != g_TransactionCheckCallBackMap.end()) {
        g_TransactionCheckCallBackMap.erase(iter);
    }
    return DestroyProducer(producerInner);
}
int PyStartPushConsumer(void *consumer) {
    return StartPushConsumer((CPushConsumer *) consumer);
}
int PyShutdownPushConsumer(void *consumer) {
    PyThreadStateUnlock PyThreadUnlock;  // ShutdownPushConsumer is a block call, ensure thread don't hold GIL.
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

int PyRegisterMessageCallbackOrderly(void *consumer, PyObject *pCallback, object args) {
    CPushConsumer *consumerInner = (CPushConsumer *) consumer;
    g_CallBackMap[consumerInner] = make_pair(pCallback, std::move(args));
    return RegisterMessageCallbackOrderly(consumerInner, &PythonMessageCallBackInner);
}

int PythonMessageCallBackInner(CPushConsumer *consumer, CMessageExt *msg) {
    PyThreadStateLock PyThreadLock;  // ensure hold GIL, before call python callback
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
int PySetPushConsumerMessageModel(void *consumer, CMessageModel messageModel) {
    return SetPushConsumerMessageModel((CPushConsumer *) consumer, messageModel);
}

int PySetPushConsumerLogPath(void *consumer, const char *logPath) {
    return SetPushConsumerLogPath((CPushConsumer *) consumer, logPath);
}

int PySetPushConsumerLogFileNumAndSize(void *consumer, int fileNum, long fileSize) {
    return SetPushConsumerLogFileNumAndSize((CPushConsumer *) consumer, fileNum, fileSize);
}

int PySetPushConsumerLogLevel(void *consumer, CLogLevel level) {
    return SetPushConsumerLogLevel((CPushConsumer *) consumer, level);
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

    class_<PyMQException>("MQException")
            .def_readonly("error", &PyMQException::error, "error")
            .def_readonly("line", &PyMQException::line, "line")
            .def("GetFile", &PyMQException::GetFile)
            .def("GetMsg", &PyMQException::GetMsg)
            .def("GetType", &PyMQException::GetType);
    enum_<CMessageModel>("CMessageModel")
            .value("BROADCASTING", BROADCASTING)
            .value("CLUSTERING", CLUSTERING);

    enum_<CLogLevel>("CLogLevel")
            .value("E_LOG_LEVEL_FATAL", E_LOG_LEVEL_FATAL)
            .value("E_LOG_LEVEL_ERROR", E_LOG_LEVEL_ERROR)
            .value("E_LOG_LEVEL_WARN", E_LOG_LEVEL_WARN)
            .value("E_LOG_LEVEL_INFO", E_LOG_LEVEL_INFO)
            .value("E_LOG_LEVEL_DEBUG", E_LOG_LEVEL_DEBUG)
            .value("E_LOG_LEVEL_TRACE", E_LOG_LEVEL_TRACE)
            .value("E_LOG_LEVEL_LEVEL_NUM", E_LOG_LEVEL_LEVEL_NUM);

    enum_<CTransactionStatus>("TransactionStatus")
            .value("E_COMMIT_TRANSACTION", E_COMMIT_TRANSACTION)
            .value("E_ROLLBACK_TRANSACTION", E_ROLLBACK_TRANSACTION)
            .value("E_UNKNOWN_TRANSACTION", E_UNKNOWN_TRANSACTION);

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
    def("CreateTransactionProducer", PyCreateTransactionProducer, return_value_policy<return_opaque_pointer>());
    def("DestroyProducer", PyDestroyProducer);
    def("DestroyTransactionProducer", PyDestroyTransactionProducer);
    def("StartProducer", PyStartProducer);
    def("ShutdownProducer", PyShutdownProducer);
    def("SetProducerNameServerAddress", PySetProducerNameServerAddress);
    def("SetProducerNameServerDomain", PySetProducerNameServerDomain);
    def("SetProducerInstanceName", PySetProducerInstanceName);
    def("SetProducerSessionCredentials", PySetProducerSessionCredentials);
    def("SetProducerCompressLevel", PySetProducerCompressLevel);
    def("SetProducerMaxMessageSize", PySetProducerMaxMessageSize);
    def("SetProducerSendMsgTimeout", PySetProducerSendMsgTimeout);

    def("SetProducerLogPath", PySetProducerLogPath);
    def("SetProducerLogFileNumAndSize", PySetProducerLogFileNumAndSize);
    def("SetProducerLogLevel", PySetProducerLogLevel);

    def("SendMessageSync", PySendMessageSync);
    def("SendMessageAsync", PySendMessageAsync);

    def("SendMessageOneway", PySendMessageOneway);
    def("SendMessageOrderly", PySendMessageOrderly);
    def("SendMessageOrderlyByShardingKey", PySendMessageOrderlyByShardingKey);
    def("SendMessageInTransaction", PySendMessageInTransaction);

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
    def("RegisterMessageCallbackOrderly", PyRegisterMessageCallbackOrderly);
    def("SetPushConsumerLogPath", PySetPushConsumerLogPath);
    def("SetPushConsumerLogFileNumAndSize", PySetPushConsumerLogFileNumAndSize);
    def("SetPushConsumerLogLevel", PySetPushConsumerLogLevel);

    //pull consumer
    def("SetPullConsumerNameServerDomain", PySetPullConsumerNameServerDomain);
    def("SetPushConsumerMessageModel", PySetPushConsumerMessageModel);

    //For Version
    def("GetVersion", PyGetVersion);
}

