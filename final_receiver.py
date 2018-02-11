import json

import pika
import sys

import telegram

from global_config import *
import _pickle as cPickle

logger = logging.getLogger(__name__)
logger.info("Starting...")


def callback(ch, method, properties, body):
    logger.debug("Final receiver callback is here")
    response = cPickle.loads(body)
    algo_name = response[0]
    answer_pair = response[1]  # url and answer here
    message = response[2]
    updateObject = response[3]
    prob = float(answer_pair[1])
    logger.info("Url processed %s %s" % (message, str(prob)))
    if prob == 1.0:
        mes = "🆘❗👮🏿 \n It's a trap! Beware of %s \n👮🏿❗🆘" % answer_pair[0].url
    else:
        mes = "Not phishing %s" % answer_pair[0].url
    logger.debug(mes)
    while True:
        try:
            logger.debug("Trying to send message")
            if updateObject.message.reply_text(mes, timeout=10):
                break
        except telegram.error.TimedOut:
            logger.warning("Timeout error, will try to resend message")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.debug("Sent answer, processed %s" % answer_pair[0].url)


logger.debug("Initializing connection")
connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOST))
channel = connection.channel()

logger.debug("Declare queue")
channel.queue_declare(queue=ANSWER_QUEUE, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=ANSWER_QUEUE)

try:
    logger.debug("Start consuming...")
    channel.start_consuming()
except KeyboardInterrupt:
    logger.debug('Keyword interrupt, exiting right now')
    connection.close()
    sys.exit()
