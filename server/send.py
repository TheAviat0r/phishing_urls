import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

for i in range(10):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=('Hello, world - %d' % i))

    print(" [x] Sent 'Hello, world!' ")

connection.close()

