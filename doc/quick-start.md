----------
## Qucik start

* set cpp despendencies
    ```bash
    wget https://opensource-rocketmq-client.oss-cn-hangzhou.aliyuncs.com/cpp-client/linux/1.0.2/RHEL7.x/librocketmq.tar.gz

    tar -zxvf librocketmq.tar.gz

    cd librocketmq

    cp -R rocketmq /usr/local/include

    cd librocketmq.a librocketmq.so /usr/local/lib

    set LD_LIBRARY_PATH

    ```

* build python client from source. if you already had it, ignore this step
    - [how to build](https://github.com/apache/rocketmq-client-python/blob/master/doc/Introduction.md)

    - copy the build result [librocketmqclientpython.so](#) to /usr/local/lib
    
*  how to produce a message<br />
    ```python
    from librocketmqclientpython import *
    ### how to init a producer instance
    def init_producer():
        producer = CreateProducer('your producer group name')
        SetProducerNameServerAddress(producer, 'your name srv address')
        StartProducer(producer)
        return producer
    ### how to send a message
    def send(body):
        msg = CreateMessage(topic)
        SetMessageBody(msg, body)
        result = SendMessageSync(producer, msg)
        DestroyMessage(msg)
        print 'done . msg id = ' + result.GetMsgId()
    ```

* how to consume the message
    ```python
    from librocketmqclientpython import *
    ## how to init a consumer intance
    def build_consumer(_group, _topic, _tag):
        consumer = CreatePushConsumer(_group)
        SetPushConsumerNameServerAddress(consumer, name_srv)
        SetPushConsumerThreadCount(consumer, 1)
        Subscribe(consumer, _topic, _tag)
        RegisterMessageCallback(consumer, callback)
        StartPushConsumer(consumer)
        print 'consumer is ready...'
        return consumer
    ## callback to consume the messages
    def callback(msg):
        print 'topic=%s' % GetMessageTopic(msg)
        print 'tag=%s' % GetMessageTags(msg)
        print 'body=%s' % GetMessageBody(msg)
        print 'msg id=%s' % GetMessageId(msg)
        print 'map.keys %s' % GetMessageKeys(msg)
        return 0
    ```