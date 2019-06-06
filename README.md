# rocketmq-python

[![Build Status](https://travis-ci.com/messense/rocketmq-python.svg?branch=master)](https://travis-ci.com/messense/rocketmq-python)
[![codecov](https://codecov.io/gh/messense/rocketmq-python/branch/master/graph/badge.svg)](https://codecov.io/gh/messense/rocketmq-python)
[![PyPI](https://img.shields.io/pypi/v/rocketmq.svg)](https://pypi.org/project/rocketmq)

RocketMQ Python client

## Installation

```bash
pip install rocketmq
```

## Usage

### Producer

```python
from rocketmq.client import Producer, Message

producer = Producer('PID-XXX')
producer.set_namesrv_domain('http://onsaddr-internet.aliyun.com/rocketmq/nsaddr4client-internet')
# For ip and port name server address, use `set_namesrv_addr` method, for example:
# producer.set_namesrv_addr('127.0.0.1:9887')
producer.set_session_credentials('XXX', 'XXXX', 'ALIYUN') # No need to call this function if you don't use Aliyun.
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
consumer.set_namesrv_domain('http://onsaddr-internet.aliyun.com/rocketmq/nsaddr4client-internet')
# For ip and port name server address, use `set_namesrv_addr` method, for example:
# consumer.set_namesrv_addr('127.0.0.1:9887')
consumer.set_session_credentials('XXX', 'XXXX', 'ALIYUN') # No need to call this function if you don't use Aliyun.
consumer.subscribe('YOUR-TOPIC', callback)
consumer.start()

while True:
    time.sleep(3600)

consumer.shutdown()

```

### PullConsumer

```python
from rocketmq.client import PullConsumer


consumer = PullConsumer('CID_XXX')
consumer.set_namesrv_domain('http://onsaddr-internet.aliyun.com/rocketmq/nsaddr4client-internet')
# For ip and port name server address, use `set_namesrv_addr` method, for example:
# consumer.set_namesrv_addr('127.0.0.1:9887')
consumer.set_session_credentials('XXX', 'XXXX', 'ALIYUN') # No need to call this function if you don't use Aliyun.
consumer.start()

for msg in consumer.pull('YOUR-TOPIC'):
    print(msg.id, msg.body)

consumer.shutdown()
```

## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.
