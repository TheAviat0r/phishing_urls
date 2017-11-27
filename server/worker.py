import pika
import time
import config
import json
import sys

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.URL_HOST))
except pika.exceptions.ConnectionClosed:
    print('ERROR: Unable to connect to URL_QUEUE')
    sys.exit()

channel = connection.channel()

channel.queue_declare(queue=config.URL_QUEUE, durable=True)
channel.queue_declare(queue=config.ANSWER_QUEUE, durable=True)

def worker_callback(ch, method, properties, body):
    message = json.loads(body)
    print(" [x] Received %s" % body)
    time.sleep(1)
    
    algo1 = UrlsAlgo(mock_json)
    algo1.run()
    urls_answers = algo1.answers()

    print('URL ALGO ANSWERS:')
    print(urls_answers)

    '''
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)

    targets = []
    for key, value in source_websites.items():
        targets.append(ImageAlgoTarget(value, key, driver))

    algo2 = ImageAlgo(mock_json, targets)
    algo2.run(driver)

    #driver.quit()
    print("URLS ALGO REPORT")
    #algo1.answers()

    print("IMAGE ALGO REPORT")
    #algo2.answers()

    for url in message:
        channel.basic_publish(exchange='',
                              routing_key=config.ANSWER_QUEUE,
                              body=url,
                              properties=pika.BasicProperties(
                              delivery_mode = 2 # make message persistent
                              ))

    print(" [x] Done")
    '''

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(worker_callback,
                      queue=config.URL_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
    sys.exit()

