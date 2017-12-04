from selenium import webdriver

from neuro_algo.neuro_algo import NeuroAlgo
from neuro_algo.supply import NeuroAlgoTarget
from worker import *
import caffe
import _pickle as cPickle

class NeuroWorker(AlgoWorker):
    def __init__(self, queue_host, algo_queue, answer_queue, driver, targets):
        super(NeuroWorker, self).__init__(queue_host, algo_queue, answer_queue, NeuroAlgo, 'NEURO_ALGO')
        self.driver = driver
        self.targets = targets

    def run_algorithm(self, urls, *args, **kwargs):
        algo_instance = NeuroAlgo(urls, self.targets)
        algo_instance.run(self.driver)

        return algo_instance.answers()

    def exit_actions(self):
        self.driver.quit()

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)
model = 'neuro_algo/phish_deploy_features_headers_net2.prototxt'
weights = 'neuro_algo/snapshot_headers_net2/snap.caffemodel'

targets = []
for key, value in source_websites.items():
    targets.append(NeuroAlgoTarget(value, key, driver,
                                   caffe.Net(model, weights, caffe.TEST),
                                   cPickle.load(open("neuro_algo/PCA3.pkl", 'rb'), encoding='latin1')))

neuro_worker = NeuroWorker(QUEUE_HOST, NEURO_ALGO_QUEUE,
                           ANSWER_QUEUE, driver,
                           targets)
neuro_worker.start()
