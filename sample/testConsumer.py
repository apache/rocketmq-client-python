import base
import time
from librocketmqclientpython import *
totalMsg = 0
def consumerMessage(msg):
     global totalMsg
     totalMsg += 1
     print(">>ConsumerMessage Called:",totalMsg)
     print(GetMessageTopic(msg))
     print(GetMessageTags(msg))
     print(GetMessageBody(msg))
     print(GetMessageId(msg))
     return 0

print("Consumer Starting.....")

consumer = CreatePushConsumer("awtTest_Producer_Python_Test")
print(consumer)
SetPushConsumerNameServerAddress(consumer,"172.17.0.5:9876")
SetPushConsumerThreadCount(consumer,1)
Subscribe(consumer, "T_TestTopic", "*")
RegisterMessageCallback(consumer,consumerMessage)
StartPushConsumer(consumer)
i = 1
while i <= 60:
    print(i)
    i += 1
    time.sleep(10) 

ShutdownPushConsumer(consumer)
DestroyPushConsumer(consumer)
print("Consumer Down....")
