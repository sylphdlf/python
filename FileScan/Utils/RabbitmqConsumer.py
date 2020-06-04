import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))

channel = connection.channel()

channel.queue_declare(queue='mq_to_nodejs')


def callback(ch, method, properties, body):
    print (" [x] Received %r" % (body,))
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume('mq_to_nodejs', callback, False)

channel.start_consuming()