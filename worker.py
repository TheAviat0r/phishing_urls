from global_config import *
from util import *
from worker import *

import json

class AlgoWorker:
    def __init__(self, queue_host, algo_queue, answer_queue, algo, name):
        self.queue_host = queue_host
        self.algo_queue = algo_queue
        self.answer_queue = answer_queue
        self.algo_class = algo
        self.algo_name = name

    def worker_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        urls = json.loads(body.decode('utf-8'))
        print(" [x] Decoded %r" % urls)    

        urls_answers = self.run_algorithm(urls)

        for answer in urls_answers:
            response = get_output_message(answer, self.algo_name)
            submit_to_queue(ch, ANSWER_QUEUE, response)

        print(" [x] Done")

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def run_algorithm(self, urls, *args, **kwargs):
        algo_instance = self.algo_class(urls, *args, **kwargs)
        algo_instance.run()

        return algo_instance.answers()

    def exit_actions(self):
        pass
        
    def start(self):
        channel, connection = connect_to_queue(self.queue_host,
                                               algo_queue=self.algo_queue,
                                               answer_queue=self.answer_queue,
                                               worker_callback=self.worker_callback)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            connection.close()
            self.exit_actions()
            sys.exit()

