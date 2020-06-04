from rocketmq.client import Producer, Message

def send_msg(key, tag, content):
    producer = Producer('LOG_MONITOR')
    producer.set_name_server_address('127.0.0.1:9876')
    producer.start()

    msg = Message('LOG_MONITOR_TOPIC')
    msg.set_keys('key1')
    msg.set_tags('tag1')
    msg.set_body(content)
    ret = producer.send_sync(msg)
    print(ret.status, ret.msg_id, ret.offset)
    producer.shutdown()

