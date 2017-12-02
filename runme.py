from bcolors import bcolors
from image_algo.image_algo import ImageAlgo
from image_algo.supply import ImageAlgoTarget
from urls_algo.urls_algo import UrlsAlgo

from global_config import *

import pika
import json
import math


# хотелось бы, чтобы запуск алгоритмов происходил исходя из конфига, то-есть,
# чтобы не приходилось сюда дописывать ImageAlgoTarget(...), или AnotherAlgoTarget(...)
# чтобы информация читалась из конфига и таргетам алгоритмов передавались нужные параметры

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=URL_ALGO_QUEUE, durable=True)
    channel.queue_declare(queue=IMAGE_ALGO_QUEUE, durable=True)

    urls_to_check = []
    with open('urls.txt', 'r') as f:
        for elem in list(f):
            urls_to_check.append(elem.replace('\n', ''))

    for url_chunk in chunks(urls_to_check, len(urls_to_check) // URL_WORKERS_AMOUNT):
        print(url_chunk)
        chunk_json = json.dumps(url_chunk, sort_keys=True)
        channel.basic_publish(exchange='',
                              routing_key=URL_ALGO_QUEUE,
                              body=chunk_json,
                              properties=pika.BasicProperties(
                                  delivery_mode=2  # make message persistent
                              ))

    for url_chunk in chunks(urls_to_check, len(urls_to_check) // IMAGE_WORKERS_AMOUNT):
        print(url_chunk)
        chunk_json = json.dumps(url_chunk, sort_keys=True)
        print(type(chunk_json))
        channel.basic_publish(exchange='',
                              routing_key=IMAGE_ALGO_QUEUE,
                              body=chunk_json,
                              properties=pika.BasicProperties(
                                  delivery_mode=2  # make message persistent
                              ))

    connection.close()
