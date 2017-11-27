import pika
import time
import config
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(config.URL_HOST))
channel = connection.channel()

channel.queue_declare(queue=config.ANSWER_QUEUE, durable=True)

def callback(ch, method, properties, body):
    url = body
    print(" [x] Url processed - %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue=config.ANSWER_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('Keyword interrupt, exiting right now')
    connection.close()
    sys.exit()

