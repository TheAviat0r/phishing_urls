import pika
import config
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=config.URL_QUEUE, durable=True)

message = json.dumps([1, 2, 3, 4, 5], sort_keys=True)

channel.basic_publish(exchange='',
                      routing_key=config.URL_QUEUE,
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode = 2 # make message persistent
                      ))

print(" [x] Sent %r" % message)

connection.close()
