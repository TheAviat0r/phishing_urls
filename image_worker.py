from image_algo.image_algo import ImageAlgo
from image_algo.supply import ImageAlgoTarget
from global_config import *
from selenium import webdriver
from util import *
from worker import *

import pika
import json
import sys

class ImageWorker(AlgoWorker):
    def __init__(self, queue_host, algo_queue, answer_queue, driver, targets):
        super(ImageWorker, self).__init__(queue_host, algo_queue, answer_queue, ImageAlgo, 'IMAGE_ALGO')
        self.driver = driver
        self.targets = targets

    def run_algorithm(self, urls, *args, **kwargs):
        algo_instance = ImageAlgo(urls, self.targets)
        algo_instance.run(self.driver)

        return algo_instance.answers()

    def exit_actions(self):
        self.driver.quit()

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)

targets = []
for key, value in source_websites.items():
    targets.append(ImageAlgoTarget(value, key, driver))

image_worker = ImageWorker(QUEUE_HOST, IMAGE_ALGO_QUEUE,
                           ANSWER_QUEUE, driver,
                           targets)
image_worker.start()
