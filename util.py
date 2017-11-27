from bcolors import bcolors
from algo import BAD_SAMPLE_CONSTANT

import pika
import sys

def get_output_message(answer, algo_type):
    response = bcolors.BOLD + str.ljust(answer[0].url, 40) + (' - [%s]' % algo_type)

    assert answer[1] == -9999 or answer[1] == 0 or answer[1] == 1

    if answer[1] == 0:
        response += " --->" + bcolors.BOLD + bcolors.OKGREEN + " Not phishing" + bcolors.ENDC
    if answer[1] == 1:
        response += " --->" + bcolors.BOLD + bcolors.FAIL + " Phishing" + bcolors.ENDC 
    if answer[1] == BAD_SAMPLE_CONSTANT:
        response += " --->" + bcolors.BOLD + bcolors.WARNING + " Bad sample" + bcolors.ENDC

    return response

def connect_to_queue(queue_host, algo_queue, answer_queue, worker_callback):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(queue_host))
    except pika.exceptions.ConnectionClosed:
        print('ERROR: Unable to connect to queue host - ' + queue_host)
        sys.exit()

    channel = connection.channel()

    channel.queue_declare(queue=algo_queue, durable=True)
    channel.queue_declare(queue=answer_queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(worker_callback,
                          queue=algo_queue)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    return channel, connection

def submit_to_queue(ch, queue_name, message):
    ch.basic_publish(exchange='',
                     routing_key=queue_name,
                     body=message,
                     properties=pika.BasicProperties(
                     delivery_mode = 2 # make message persistent
                     ))
