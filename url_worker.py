from image_algo.image_algo import ImageAlgo
from image_algo.supply import ImageAlgoTarget
from urls_algo.urls_algo import UrlsAlgo
from bcolors import bcolors
from global_config import *
from util import *

import pika
import json
import sys

def worker_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    urls = json.loads(body.decode('utf-8'))
    print(" [x] Decoded %r" % urls)    

    algo1 = UrlsAlgo(urls)
    algo1.run()
    urls_answers = algo1.answers()


    for answer in urls_answers:
        response = get_response(answer, 'URL_ALGO')
        channel.basic_publish(exchange='',
                              routing_key=ANSWER_QUEUE,
                              body=response,
                              properties=pika.BasicProperties(
                              delivery_mode = 2 # make message persistent
                              ))

    print(" [x] Done")

    ch.basic_ack(delivery_tag = method.delivery_tag)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOST))
except pika.exceptions.ConnectionClosed:
    print('ERROR: Unable to connect to URL_QUEUE')
    sys.exit()

channel = connection.channel()

channel.queue_declare(queue=URL_ALGO_QUEUE, durable=True)
channel.queue_declare(queue=ANSWER_QUEUE, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(worker_callback,
                      queue=URL_ALGO_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
    sys.exit()

