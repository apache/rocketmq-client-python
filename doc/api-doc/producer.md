----------
## Api docs

### Producer
* producer = CreateProducer("producerName") <br />
  - function description<br />
    create a producer instance<br />

  - input <br />
    producerName: producer group name<br />

  - return<br />
    a new producer instance, can send messages<br />

* SetProducerNameServerAddress(producer, "namesrv address")
  - function description<br />
    set namesrv address for the producer instance<br />

  - input<br />
    producer : a producer instance <br />

    namesrv address : like 127.0.0.1:9876<br />
  - return : no <br />
* SetProducerInstanceName(producer, "instance name")
  - function description<br />
    set instance name for the producer

  - input<br />
    producer : a producer instance <br />
    intance name : a producer instance name<br />
  - return : no <br />
    
* SetProducerSessionCredentials(producer, accessKey, secretKey, channel)
  - function description<br />
    set access keys for accessing broker in the session

  - input<br />
    producer : a producer instance <br />
    accessKey : accessKey<br />
    secretKey : secretKey<br />
    channel : channel<br />
  - return : no <br />

* StartProducer(producer)
  - function description<br />
    start the producer instance

  - input<br />
    producer : a producer instance <br />
   
  - return : no <br />

* ShutdownProducer(producer)
  - function description<br />
    shutdown the producer instance

  - input<br />
    producer : a producer instance <br />
   
  - return : no <br />

* DestroyProducer(producer)
  - function description<br />
    destroy the producer instance

  - input<br />
    producer : a producer instance <br />
   
  - return : no <br />

* PySendResult result = SendMessageSync(producer, msg)
  - function description<br />
    send a message sync

  - input<br />
    producer : a producer instance <br />
    msg : a message instance <br />
    
  - return<br />
    result.GetMsgId(): if send successfuly, it is the message id<br />
    result.offset : message offset in broker<br />
    result.sendStatus<br />
      SEND_OK: <br />
      SEND_FLUSH_DISK_TIMEOUT,<br />
      SEND_FLUSH_SLAVE_TIMEOUT,<br />
      SEND_SLAVE_NOT_AVAILABLE<br />

* SendMessageOneway(producer, msg)
  - function description<br />
    send a message one way, no matter about the result

  - input<br />
    producer : a producer instance <br />
    msg : a message instance <br />

* SendMessageOrderly(producer, msg, autoRetryTimes,arg, queueSelectorCallback)
  - function description<br />
    send a message orderly

  - input<br />
    producer : a producer instance <br />
    msg : a message instance <br />
    autoRetryTimes: retry times when send fail<br />
    arg: send args<br />
    queueSelectorCallback: callback for which queue choose to send message to. return queue index start from 0 to (max queue count -1)

