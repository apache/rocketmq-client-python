----------
## Api docs

### 1. Push Consumer
* consumer = CreatePushConsumer(consumerGroup) <br />
  - function description<br />
    create a push consumer instance, by setting consumer group<br />

  - input <br />
    consumerGroup: consumer group<br />
    
  - return<br />
    consumer: consumer instance

* SetPushConsumerNameServerAddress(consumer, namesrv) <br />
  - function description<br />
    set name srv address for the consumer instance<br />

  - input <br />
    consumer: consumer intance<br />
    namesrv: name srv address. like : 127.0.0.1:9876

  - return : no<br />

* Subscribe(consumer, topic, tag) <br />
  - function description<br />
    make consumer subscribe the topic and tag <br />

  - input <br />
    consumer: consumer intance<br />
    topic: topic name
    tag: topic tag

* RegisterMessageCallback(consumer, pyCallBack) <br />
  - function description<br />
    set callback for push consumer instance <br />

  - input <br />
    consumer: consumer intance<br />
    pyCallBack: py callback method. when message pulled, they would be send to a pyCallback method

* SetPushConsumerThreadCount(consumer, threadCount)
  - function description<br />
    set push consumer thread count<br />

  - input <br />
    consumer: consumer intance<br />
    threadCount: thread count

* SetPushConsumerMessageBatchMaxSize(consumer, batchSize)
  - function description<br />
    set message count for one push<br />

  - input <br />
    consumer: consumer intance<br />
    batchSize: message count 

* SetPushConsumerInstanceName(consumer, instanceName)
  - function description<br />
    set consumer instance name<br />

  - input <br />
    consumer: consumer intance<br />
    instanceName: consumer instance name

* SetPushConsumerSessionCredentials(consumer, accessKey, secretKey,channel)
  - function description<br />
    set consumer access keys<br />

  - input <br />
    consumer: consumer intance<br />
    accessKey: accessKey<br />
    secretKey: secretKey<br />
    channel: channel<br />
    





