import time

from rocketmq.client import PushConsumer, ConsumeStatus


def callback(msg):
    print((msg.body).decode("utf-8"))
    return ConsumeStatus.CONSUME_SUCCESS


consumer = PushConsumer('LOG_MONITOR')
consumer.set_name_server_address('127.0.0.1:9876')
consumer.subscribe('LOG_MONITOR_TOPIC', callback)
consumer.start()

while True:
    time.sleep(3600)

# consumer.shutdown()