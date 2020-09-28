# rocketmq-client-python

[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)
[![Build Status](https://travis-ci.org/apache/rocketmq-client-python.svg?branch=master)](https://travis-ci.org/apache/rocketmq-client-python)
[![codecov](https://codecov.io/gh/apache/rocketmq-client-python/branch/ctypes/graph/badge.svg)](https://codecov.io/gh/apache/rocketmq-client-python/branch/ctypes)
[![PyPI](https://img.shields.io/pypi/v/rocketmq-client-python.svg)](https://pypi.org/project/rocketmq-client-python)
[![GitHub release](https://img.shields.io/badge/release-download-default.svg)](https://github.com/apache/rocketmq-client-python/releases)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/apache/rocketmq-client-python.svg)](http://isitmaintained.com/project/apache/rocketmq-client-python "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/apache/rocketmq-client-python.svg)](http://isitmaintained.com/project/apache/rocketmq-client-python "Percentage of issues still open")
![Twitter Follow](https://img.shields.io/twitter/follow/ApacheRocketMQ?style=social)

RocketMQ Python client, based on [rocketmq-client-cpp](https://github.com/apache/rocketmq-client-cpp), supports Linux and macOS
## Prerequisites

### Install `librocketmq`
rocketmq-client-python is a lightweight wrapper around [rocketmq-client-cpp](https://github.com/apache/rocketmq-client-cpp), so you need install 
`librocketmq` first.

#### Download by binary release.
download specific release according you OS: [rocketmq-client-cpp-2.0.0](https://github.com/apache/rocketmq-client-cpp/releases/tag/2.0.0)
- centos
    
    take centos7 as example, you can install the library in centos6 by the same method.
    ```bash
        wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0-centos7.x86_64.rpm
        sudo rpm -ivh rocketmq-client-cpp-2.0.0-centos7.x86_64.rpm
    ```
- debian
    ```bash
        wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0.amd64.deb
        sudo dpkg -i rocketmq-client-cpp-2.0.0.amd64.deb
    ```
- macOS
    ```bash
        wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0-bin-release.darwin.tar.gz
        tar -xzf rocketmq-client-cpp-2.0.0-bin-release.darwin.tar.gz
        cd rocketmq-client-cpp
        mkdir /usr/local/include/rocketmq
        cp include/* /usr/local/include/rocketmq
        cp lib/* /usr/local/lib
        install_name_tool -id "@rpath/librocketmq.dylib" /usr/local/lib/librocketmq.dylib
    ```
#### Build from source
you can also build it manually from source according to [Build and Install](https://github.com/apache/rocketmq-client-cpp/tree/master#build-and-install)

## Installation

```bash
pip install rocketmq-client-python
```

## Usage

### Producer

```python
from rocketmq.client import Producer, Message

producer = Producer('PID-XXX')
producer.set_name_server_address('127.0.0.1:9876')
producer.start()

msg = Message('YOUR-TOPIC')
msg.set_keys('XXX')
msg.set_tags('XXX')
msg.set_body('XXXX')
ret = producer.send_sync(msg)
print(ret.status, ret.msg_id, ret.offset)
producer.shutdown()
```

### PushConsumer

```python
import time

from rocketmq.client import PushConsumer, ConsumeStatus


def callback(msg):
    print(msg.id, msg.body)
    return ConsumeStatus.CONSUME_SUCCESS


consumer = PushConsumer('CID_XXX')
consumer.set_name_server_address('127.0.0.1:9876')
consumer.subscribe('YOUR-TOPIC', callback)
consumer.start()

while True:
    time.sleep(3600)

consumer.shutdown()

```

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) Copyright (C) Apache Software Foundation
