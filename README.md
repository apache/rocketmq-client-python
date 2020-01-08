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

#### include file
```bash
git clone https://github.com/apache/rocketmq-client-cpp

# By default, CFLAGS contains `/usr/local/include`
sudo mkdir -p /usr/local/include/rocketmq/
sudo cp rocketmq-client-cpp/include/* /usr/local/include/rocketmq
```

#### binary library
your could download directly or build manually:

- download specific release: [rocketmq-client-cpp](https://archive.apache.org/dist/rocketmq/rocketmq-client-cpp/1.2.4/rocketmq-client-cpp-1.2.4-bin-release.tar.gz)
 and unzip the package, please choose the right version according to your OS and unzip it, then copy the library files to to your `LD_LIBRARY_PATH` directory(as default, `/usr/local/lib/` works finely).
- build from source: [Build and Install](https://github.com/apache/rocketmq-client-cpp/tree/master#build-and-install)

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

from rocketmq.client import PushConsumer


def callback(msg):
    print(msg.id, msg.body)


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
