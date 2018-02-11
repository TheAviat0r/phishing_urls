# -*- coding: UTF-8 -*-
import _pickle as cPickle
import os

import numpy as np
import sklearn # restoring model from cPickle byte format, important!

from container import Container, ElementBase
from global_config import BAD_SAMPLE_CONSTANT
from urls_algo.helpers import url_analyse

from algo import Algorithm

URLSALGOPATH = os.path.dirname(os.path.abspath(__file__))


class UrlElement(ElementBase):
    vector = []

    def __init__(self, url, *args, **kwargs):
        super(UrlElement, self).__init__(url, *args, **kwargs)


class UrlsSuspicousContainer(Container):
    element_class = UrlElement
    features_file = 'scrapyres/features.csv'

    def __init__(self, urls, *args, **kwargs):
        super(UrlsSuspicousContainer, self).__init__(urls, *args, **kwargs)

    def get_data(self):
        dt = np.dtype(list(zip(['feature', 'value'], [('unicode', 50), 'int'])))
        for idx, url in enumerate(self.elems):
            features = np.array([url_analyse(url.url)], dtype=dt)
            self.logger.debug("Features vector %s " % features)
            self.elems[idx].vector = features['value'].reshape(1, -1)


class UrlsAlgo(Algorithm):
    path = os.path.join(Container.path, 'urls_algo_tmp/')
    suspicious_container_class = UrlsSuspicousContainer
    model_file = os.path.join(URLSALGOPATH, 'tree_model.bin')
    name = "URLS ALGO"

    def get_answer(self, suspect):
        loaded_model = cPickle.load(open(self.model_file, 'rb'), encoding='latin1')
        if np.any(suspect.vector):
            return loaded_model.predict(suspect.vector)[0]
        else:
            return BAD_SAMPLE_CONSTANT
