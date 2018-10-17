import __init__
from librocketmqclientpython import *
 
def initProducer(name):
    print("---------Create Producer---------------")
    producer =CreateProducer(name)
    SetProducerNameServerAddress(producer,"172.17.0.5:9876")
    StartProducer(producer)
    return producer

def testSendMssage(producer,topic,key,body):
    print("Starting Sending.....")
    msg = CreateMessage(topic)
    SetMessageBody(msg, body)
    SetMessageKeys(msg, key)
    SetMessageTags(msg, "ThisMessageTag.")
    result = SendMessageSync(producer,msg)
    print(result)
    print("Msgid:")
    print(result.GetMsgId())
    print("Offset:")
    print(result.offset)
    print("sendStatus:")
    print(result.sendStatus)
    DestroyMessage(msg)
    print("Done...............")

def releaseProducer(producer):
    ShutdownProducer(producer)
    DestroyProducer(producer)
    print("--------Release producer-----------")

