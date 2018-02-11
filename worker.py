# encoding: utf-8
import _pickle as cPickle
import logging

import sys

import os

from global_config import ANSWER_QUEUE
from util import connect_to_queue, submit_to_queue, get_output_message


class AlgoWorker:

    def __init__(self, queue_host, algo_queue, answer_queue, algo, name):
        self.queue_host = queue_host
        self.algo_queue = algo_queue
        self.answer_queue = answer_queue
        self.algo_class = algo
        self.algo_name = name
        self.logger = logging.getLogger("%s(pid: %s)" % (self.__class__.__name__, os.getpid()))

    def worker_callback(self, ch, method, properties, body):
        self.logger.info("Worker callback is here")
        response = cPickle.loads(body)
        urls = response[0]  # url
        updateObject = response[1]  # объект для отправки сообщения в чат
        self.logger.debug("Decoded %s" % urls)
        self.logger.info("Starting algorithm")

        urls_answers = self.run_algorithm(urls)

        self.logger.debug("Algorithm finished, got these answers" % urls_answers)

        for answer in urls_answers:
            response = get_output_message(answer, self.algo_name)
            self.logger.debug("Sending to final receiver")
            submit_to_queue(ch, ANSWER_QUEUE, cPickle.dumps((self.algo_name, response[0], response[1], updateObject)))

        ch.basic_ack(delivery_tag=method.delivery_tag)

        self.logger.debug("Sent basic_ack to queue, done")

    def run_algorithm(self, urls, *args, **kwargs):
        self.logger.debug("Getting algo instance")
        algo_instance = self.algo_class(urls, *args, **kwargs)
        self.logger.debug("Calling run method")
        algo_instance.run()
        self.logger.debug("Run method finished")
        return algo_instance.answers()

    def exit_actions(self):
        pass

    def start(self):
        self.logger.debug("Connecting to queue")
        channel, connection = connect_to_queue(self.queue_host,
                                               algo_queue=self.algo_queue,
                                               answer_queue=self.answer_queue,
                                               worker_callback=self.worker_callback)

        try:
            self.logger.debug("Worker start consuming")
            channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.debug("Keyboard interrupt, exiting")
            connection.close()
            self.exit_actions()
            sys.exit()
