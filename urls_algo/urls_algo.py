# -*- coding: UTF-8 -*-
import _pickle as cPickle
import os

import numpy as np
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
import sklearn

from container import Container, ElementBase
from global_config import ALGOTMP, BAD_SAMPLE_CONSTANT
from .phish_spider import PhishSpider
import csv

from algo import Algorithm

URLSALGOPATH = os.path.dirname(os.path.abspath(__file__))


class UrlElement(ElementBase):
    vector = []

    def __init__(self, url, *args, **kwargs):
        super(UrlElement, self).__init__(url, *args, **kwargs)


class UrlsSuspicousContainer(Container):
    path = os.path.join(ALGOTMP, 'urls_algo_tmp/')
    element_class = UrlElement
    features_file = 'scrapyres/features.csv'

    def __init__(self, urls, *args, **kwargs):
        super(UrlsSuspicousContainer, self).__init__(urls, *args, **kwargs)

    def get_data(self):

        settings = Settings()

        settings.set("ROBOTSTXT_OBEY", False)
        settings.set("DOWNLOADER_MIDDLEWARES", {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
            'random_useragent.RandomUserAgentMiddleware': 400,
        })
        settings.set("ITEM_PIPELINES", {'urls_algo.pipelines.SaveHtmlFilesAndProcessFeaturesPipeline': 400, })
        settings.set("PROXY_LIST", [])
        settings.set("USER_AGENT_LIST", os.path.join(URLSALGOPATH, 'user_agents.txt'))

        process = CrawlerProcess(settings)

        process.crawl(PhishSpider, urls_objects=self.elems)

        process.start()

        with open(os.path.join(self.path, self.features_file), 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                arr = np.array(row, dtype=np.int32).reshape(1,-1)
                self.elems[int(arr[0][0])].vector = arr[:,1:]


class UrlsAlgo(Algorithm):
    suspicious_container_class = UrlsSuspicousContainer
    model_file = os.path.join(URLSALGOPATH, 'tree_model.bin')

    def get_answer(self, suspect):
        loaded_model = cPickle.load(open(self.model_file, 'rb'), encoding='latin1')
        if np.any(suspect.vector):
            return loaded_model.predict(suspect.vector)[0]
        else:
            return BAD_SAMPLE_CONSTANT
