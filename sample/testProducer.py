from base import *
import time


producer = initProducer("TestPythonProducer")
topic = "T_TestTopic"
key = "TestKeys"
body = "ThisIsTestBody"
i = 0
while i < 10000:
    i += 1
    testSendMssage(producer,topic,key,body)
    
    print("Now Send Message:",i)

releaseProducer(producer)
