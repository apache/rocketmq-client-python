----------
## RocketMQ Client Python

### 1. Python Runtime Version
* python 2.7.x 


### 2. Dependency of Python Client

* CPP Core: [librocketmq](https://github.com/apache/rocketmq-client-cpp)	
* python-devel 2.7.x
* boost-python 1.58.0
      
### 3. Build and Install
#### Linux Platform
* Install compile tools:
    ```
    - sudo yum install make
    - sudo yum install cmake
    - sudo yum install gcc-c++
    ```
* Install dependency:
 
    1. python-devel
       ```
       sudo yum install python-devel
       ```
    
    2. zlib-devel
       ```
       sudo yum install zlib-devel
       ```
    3. boost-python
       ```
       sudo sh install_boostpython.sh
       ```
    4. [librocketmq](https://github.com/apache/rocketmq-client-cpp), choose one method below:
      
       - build from source: [Build and Install](https://github.com/apache/rocketmq-client-cpp/tree/master#build-and-install)
         
       - download specific release: [rocketmq-client-cpp](https://www.apache.org/dyn/closer.cgi?path=rocketmq/rocketmq-client-cpp/1.2.4/rocketmq-client-cpp-1.2.4-bin-release.tar.gz) and unzip the package, please choose the right version according to your OS and unzip it, then copy the library files to to your `/usr/local/lib/` directory and copy the head files under `include` path to `/usr/local/include/rocketmq/`. and please make sure your `/usr/local/lib/` directory is under the `LD_LIBRARY_PATH`.
     
* Make and install module manually
   1. Using Dynamic RocketMQ and boost python libraries are recommended.
      ```
      - mkdir build && cd build
      - cmake ../ -DBoost_USE_STATIC_LIBS=OFF -DROCKETMQ_USE_STATIC_LIBS=OFF
      - make
      - make install
      ```
      
   2. Also you can using static libraries.
      ```
         - mkdir build & cd build
         - cmake ../ -DBoost_USE_STATIC_LIBS=ON -DROCKETMQ_USE_STATIC_LIBS=ON
         - make
         - make install
      ```
* Check verion
   ```
   strings librocketmqclientpython.so |grep PYTHON_CLIENT_VERSION
   ```
#### macOS Mojave 10.14.2
* Compile tools:
    ```
    - make: 3.8
    - cmake 3.12
    - Apple LLVM(clang) 10
    ```
* Install dependency:
 
    1. python-devel
    
    2. zlib-devel
    
    3. boost-python
       ```
       sh install_boostpython.sh
       ```
    4. [librocketmq](https://github.com/apache/rocketmq-client-cpp), choose one method below:
      
       - build from source: [Build and Install](https://github.com/apache/rocketmq-client-cpp/tree/master#build-and-install)
         
       - quick install: there are no cpp binary release for macos, below script can only be used for dev env.
       ```
       mkdir rocketmqlib
       cd rocketmqlib
       wget https://opensource-rocketmq-client.oss-cn-hangzhou.aliyuncs.com/cpp-client/mac/1.2.4/librocketmq.tar.gz
       tar -xzf librocketmq.tar.gz
       cp librocketmq.dylib librocketmq.a /usr/local/lib/
       cp -r rocketmq /usr/local/include/
       ```
   
     
* Make and install module manually
   ```
      - mkdir build && cd build
      - cmake ../ -DBoost_USE_STATIC_LIBS=OFF -DROCKETMQ_USE_STATIC_LIBS=OFF
      - make
      - make install
   ```
* Check verion
   ```
   strings librocketmqclientpython.so |grep PYTHON_CLIENT_VERSION
   ```
    
----------
## How to use
- set LD_LIBRARY_PATH
  ```
  export LD_LIBRARY_PATH=/usr/local/lib
  ```
  
- import module
  ```
  from librocketmqclientpython import *
  ```
  
- create message by following interface:
  ```
  - msg = CreateMessage("your_topic.")
  - SetMessageBody(msg, "this_message_body.")
  - SetMessageKeys(msg, "this_message_keys.")
  - SetMessageTags(msg, "this_message_tag.")
  ```
- producer must invoke following interface:
  ```
  - producer = CreateProducer("please_rename_unique_group_name");
  - SetProducerNameServerAddress(producer, "please_rename_unique_name_server")
  - StartProducer(producer)
  - SendMessageSync(producer, msg)
  - ShutdownProducer(producer)
  - DestroyProducer(producer)
  ```
- how to consumer messages
  ```
  - def consumerMessage(msg, args):
  -     topic = GetMessageTopic(msg)
  -     body = GetMessageBody(msg)
  -     tags = GetMessageTags(msg)
  -     msgid = GetMessageId(msg)
  -     # handle message...
  -     return 0
  ```
- pushconsumer must invoke following interface:
  ```
  - consumer = CreatePushConsumer("please_rename_unique_group_name_1");
  - SetPushConsumerNameServerAddress(consumer, "please_rename_unique_name_server")
  - Subscribe(consumer, "your_topic", "*")
  - RegisterMessageCallback(consumer, consumerMessage, args)
  - StartPushConsumer(consumer)
  - ShutdownPushConsumer(consumer)
  - DestroyPushConsumer(consumer)
  ```
----------
## Demo
- sync producer
  - python testProducer.py
- push consumer
  - python testConsumer.py

