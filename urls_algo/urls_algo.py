# -*- coding: UTF-8 -*-
import _pickle as cPickle
import os
from scrapy import signals, log
from scrapy.crawler import Crawler
from scrapy.settings import Settings

from container import Container, ElementBase
from global_config import ALGOTMP
from .phish_spider import PhishSpider
import csv

from algo import Algorithm


class UrlElement(ElementBase):
    vector = []

    def __init__(self, url, vector, *args, **kwargs):
        super(UrlElement).__init__(url, args, kwargs)


class UrlsSuspicousContainer(Container):
    path = os.path.join(ALGOTMP, 'urls_algo_tmp/')
    element_class = UrlElement
    features_file = 'scrapyres/feautres.csv'

    def __init__(self, urls, *args, **kwargs):
        super(UrlsSuspicousContainer).__init__(urls, args, kwargs)

    def get_data(self):
        def spider_closing(spider):
            """Activates on spider closed signal"""
            log.msg("Closing reactor", level=log.INFO)

        settings = Settings()

        settings.set("ROBOTSTXT_OBEY", False)
        settings.set("DOWNLOADER_MIDDLEWARES", {
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 100,
            'random_useragent.RandomUserAgentMiddleware': 400,
        })
        settings.set("ITEM_PIPELINES", {'pipelines.SaveHtmlFilesAndProcessFeaturesPipeline': 400, })
        settings.set("FILES_STORE", 'scrapyres')
        settings.set("PROXY_LIST", [])
        settings.set("USER_AGENT_LIST", 'user_agents.txt')

        crawler = Crawler(settings)

        # stop reactor when spider closes
        crawler.signals.connect(spider_closing, signal=signals.spider_closed)

        crawler.crawl(PhishSpider(self.elems))

        with open(os.path.join(self.path, self.features_file), 'r') as f:
            vectors_reader = csv.DictReader(f)
            idx = 0
            for vector in vectors_reader:
                self.elems[idx].vector = vector
                idx += 1


class UrlsAlgo(Algorithm):
    suspicious_container_class = UrlsSuspicousContainer
    model_file = 'tree_model.bin'

    def get_answer(self, suspect):
        loaded_model = cPickle.load(open(self.model_file, 'rb'))
        return loaded_model.predict(suspect.vector)
