import pika


def send_msg(topic_, content_):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=topic_, durable='true')
    channel.basic_publish(exchange='', routing_key='mq_to_nodejs', body=content_)
    connection.close()

