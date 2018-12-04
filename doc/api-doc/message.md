----------
## Api docs

### 1. Message
* message = CreateMessage("topicName") <br />
  - function description<br />
    create a message instance, by setting topic field<br />

  - input <br />
    topicName: a topic name<br />

  - return<br />
    a new message instance, after used it, you need call DestroyMessage(message)<br />

* DestroyMessage(message) <br />
  - function description<br />
    destroy a message instance, delete memmory<br />

  - input <br />
    message: message instance<br />

* SetMessageTopic(message, topic) <br />
  - function description<br />
    set topic field value for the message<br />

  - input <br />
    message: message instance<br />
    topic: a topic name

* SetMessageTags(message, tags) <br />
  - function description<br />
    set tag field value for the message<br />

  - input <br />
    message: message instance<br />
    tags: tag for the topic

* SetMessageKeys(message, keys) <br />
  - function description<br />
    set key field value for the message<br />

  - input <br />
    message: message instance<br />
    keys: key for the topic

* SetMessageBody(message, stringBody) <br />
  - function description<br />
    set body for the message<br />

  - input <br />
    message: message instance<br />
    body: message body as string

* SetByteMessageBody(message, byteBody, byteLength) <br />
  - function description<br />
    set body for the message<br />

  - input <br />
    message: message instance<br />
    byteBody: message body as byte[]
    byteLength: byteBody's length

* SetMessageProperty(message, key, value) <br />
  - function description<br />
    set extend k-v for message<br />

  - input <br />
    message: message instance<br />
    key: string key
    value: string value

* SetMessageDelayTimeLevel(message, level) <br />
  - function description<br />
    set delay level<br />

  - input <br />
    message: message instance<br />
    level: delay level as int


### 2. MessageExt
* topic = GetMessageTopic(msgExt) <br />
  - function description<br />
    get topic name from a message instance<br />

  - input <br />
    msgExt: message instance<br />
  - return<br />
    topic: topic name

* tag = GetMessageTags(msgExt) <br />
  - function description<br />
    get tag from a message instance<br />

  - input <br />
    msgExt: message instance<br />
  - return<br />
    tag: tag

* key = GetMessageKeys(msgExt) <br />
  - function description<br />
    get message key from a message instance<br />

  - input <br />
    msgExt: message instance<br />
  - return<br />
    key: message key

* body = GetMessageBody(msgExt) <br />
  - function description<br />
    get message body from a message instance<br />

  - input <br />
    msgExt: message instance<br />
  - return<br />
    body: message body as string

* value = GetMessageProperty(msgExt, key) <br />
  - function description<br />
    get a message proprty value from a message instance<br />

  - input <br />
    msgExt: message instance<br />
    key: property key
  - return<br />
    value: property value as string

* messageId = GetMessageId(msgExt) <br />
  - function description<br />
    get a message id from a message instance<br />

  - input <br />
    msgExt: message instance<br />
  - return<br />
    messageId: message id as string