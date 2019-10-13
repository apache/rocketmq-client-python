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
#include "CPullConsumer.h"
#include "CMQException.h"
#include <boost/python.hpp>

using namespace boost::python;

typedef struct _PySendResult_ {
    CSendStatus sendStatus;
    char msgId[MAX_MESSAGE_ID_LENGTH];
    long long offset;

    const char *GetMsgId() {
        return (const char *) msgId;
    }
} PySendResult;

typedef struct _PyMQException_ {
    int error;
    int line;
    char file[MAX_EXEPTION_FILE_LENGTH];
    char msg[MAX_EXEPTION_MSG_LENGTH];
    char type[MAX_EXEPTION_TYPE_LENGTH];

    const char *GetFile() {
        return (const char *) file;
    }

    const char *GetMsg() {
        return (const char *) msg;
    }

    const char *GetType() {
        return (const char *) type;
    }
} PyMQException;


typedef struct _PyMessageExt_ {
    CMessageExt *pMessageExt;
} PyMessageExt;

typedef struct _PyUserData_ {
    PyObject *pyObject;
    void *pData;
} PyUserData;

typedef struct _PyCallback_ {
    PyObject *successCallback;
    PyObject *exceptionCallback;
} PyCallback;

#define PYTHON_CLIENT_VERSION "1.2.0"
#define PYCLI_BUILD_DATE "04-12-2018"

#ifdef __cplusplus
extern "C" {
#endif

//message
void *PyCreateMessage(const char *topic);
int PyDestroyMessage(void *msg);
int PySetMessageTopic(void *msg, const char *topic);
int PySetMessageTags(void *msg, const char *tags);
int PySetMessageKeys(void *msg, const char *keys);
int PySetMessageBody(void *msg, const char *body);
int PySetByteMessageBody(void *msg, const char *body, int len);
int PySetMessageProperty(void *msg, const char *key, const char *value);
int PySetMessageDelayTimeLevel(void *msg, int level);

//messageExt
const char *PyGetMessageTopic(PyMessageExt msgExt);
const char *PyGetMessageTags(PyMessageExt msgExt);
const char *PyGetMessageKeys(PyMessageExt msgExt);
const char *PyGetMessageBody(PyMessageExt msgExt);
const char *PyGetMessageProperty(PyMessageExt msgExt, const char *key);
const char *PyGetMessageId(PyMessageExt msgExt);

//producer
void *PyCreateProducer(const char *groupId);
CTransactionStatus PyLocalTransactionCheckerCallback(CProducer *producer, CMessageExt *msg, void *data);
CTransactionStatus PyLocalTransactionExecuteCallback(CProducer *producer, CMessage *msg, void *data);
void *PyCreateTransactionProducer(const char *groupId, PyObject *localTransactionCheckerCallback);

int PyDestroyProducer(void *producer);
int PyDestroyTransactionProducer(void *producer);
int PyStartProducer(void *producer);
int PyShutdownProducer(void *producer);
int PySetProducerNameServerAddress(void *producer, const char *namesrv);
int PySetProducerNameServerDomain(void *producer, const char *domain);
int PySetProducerInstanceName(void *producer, const char *instanceName);
int PySetProducerSessionCredentials(void *producer, const char *accessKey, const char *secretKey, const char *channel);
int PySetProducerCompressLevel(void *producer, int level);
int PySetProducerMaxMessageSize(void *producer, int size);
int PySetProducerLogPath(void *producer, const char *logPath);
int PySetProducerLogFileNumAndSize(void *producer, int fileNum, long fileSize);
int PySetProducerLogLevel(void *producer, CLogLevel level);
int PySetProducerSendMsgTimeout(void *producer, int timeout);

PySendResult PySendMessageSync(void *producer, void *msg);
int PySendMessageOneway(void *producer, void *msg);

void PySendSuccessCallback(CSendResult result, CMessage *msg, void *pyCallback);
void PySendExceptionCallback(CMQException e, CMessage *msg, void *pyCallback);
int PySendMessageAsync(void *producer, void *msg, PyObject *sendSuccessCallback, PyObject *sendExceptionCallback);

PySendResult PySendMessageOrderly(void *producer, void *msg, int autoRetryTimes, void *args, PyObject *queueSelector);
PySendResult PySendMessageOrderlyByShardingKey(void *producer, void *msg, const char *shardingKey);
PySendResult PySendMessageInTransaction(void *producer , void *msg, PyObject *localTransactionExecuteCallback , void *args);

int PyOrderlyCallbackInner(int size, CMessage *msg, void *args);

//sendResult
const char *PyGetSendResultMsgID(CSendResult &sendResult);

//consumer
void *PyCreatePushConsumer(const char *groupId);
int PyDestroyPushConsumer(void *consumer);
int PyStartPushConsumer(void *consumer);
int PyShutdownPushConsumer(void *consumer);
int PySetPushConsumerNameServerAddress(void *consumer, const char *namesrv);
int PySetPushConsumerNameServerDomain(void *consumer, const char *domain);
int PySubscribe(void *consumer, const char *topic, const char *expression);
int PyRegisterMessageCallback(void *consumer, PyObject *pCallback, object args);
int PyRegisterMessageCallbackOrderly(void *consumer, PyObject *pCallback, object args);
int PythonMessageCallBackInner(CPushConsumer *consumer, CMessageExt *msg);
int PySetPushConsumerThreadCount(void *consumer, int threadCount);
int PySetPushConsumerMessageBatchMaxSize(void *consumer, int batchSize);
int PySetPushConsumerInstanceName(void *consumer, const char *instanceName);
int PySetPushConsumerSessionCredentials(void *consumer, const char *accessKey, const char *secretKey, const char *channel);
int PySetPushConsumerMessageModel(void *consumer, CMessageModel messageModel);
int PySetPushConsumerLogPath(void *consumer, const char *logPath);
int PySetPushConsumerLogFileNumAndSize(void *consumer, int fileNum, long fileSize);
int PySetPushConsumerLogLevel(void *consumer, CLogLevel level);

//push consumer
int PySetPullConsumerNameServerDomain(void *consumer, const char *domain);
//version
const char *PyGetVersion();

#ifdef __cplusplus
};
#endif

