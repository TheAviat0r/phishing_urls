import json

import pika
import sys

from global_config import *
from util import submit_to_queue
import _pickle as cPickle


def callback(ch, method, properties, body):
    response = cPickle.loads(body)
    algo_name = response[0]
    answer_pair = response[1]  # url и ответ
    message = response[2]
    print(" [x] Url processed - " + message + str(float(answer_pair[1])))
    if ENABLE_WEB_INTERFACE:
        to_send = json.dumps({
            'algo': algo_name,
            'url': answer_pair[0].url,
            'answer': float(answer_pair[1])
        })
        submit_to_queue(ch, 'website_queue', to_send)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOST))
channel = connection.channel()

channel.queue_declare(queue=ANSWER_QUEUE, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=ANSWER_QUEUE)

if ENABLE_WEB_INTERFACE:
    channel.queue_declare(queue='website_queue',
                          durable=True)  # тут бы какое-нибудь уникальное имя, которая также можно получить из js

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('Keyword interrupt, exiting right now')
    connection.close()
    sys.exit()
