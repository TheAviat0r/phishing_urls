from urls_algo.urls_algo import UrlsAlgo
from global_config import *
from util import *
from worker import *

class UrlWorker(AlgoWorker):
    def __init__(self, queue_host, algo_queue, answer_queue):
        super(UrlWorker, self).__init__(queue_host,
                                        algo_queue, answer_queue,
                                        UrlsAlgo, "URLS_ALGO")

url_worker = UrlWorker(QUEUE_HOST, URL_ALGO_QUEUE, ANSWER_QUEUE)
url_worker.start()



