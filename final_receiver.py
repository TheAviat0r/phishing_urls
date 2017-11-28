import pika
import time
import sys

from global_config import *

def callback(ch, method, properties, body):
    response = body.decode('utf-8')
    print(" [x] Url processed - " + response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOST))
channel = connection.channel()

channel.queue_declare(queue=ANSWER_QUEUE, durable=True)

channel.basic_consume(callback,
                      queue=ANSWER_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('Keyword interrupt, exiting right now')
    connection.close()
    sys.exit()
