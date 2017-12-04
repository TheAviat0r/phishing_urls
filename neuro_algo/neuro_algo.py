import time

from algo import Algorithm
from bcolors import bcolors
from container import Container, ElementBase
from global_config import ALGOTMP
import numpy as np
from image_algo.helpers.screenshot import get_screenshot
from neuro_algo.preprocessing_crop_minify import crop_minify
import _pickle as cPickle
from .config import *

caffe_root = '../env/caffe/'
import sys
sys.path.insert(0, caffe_root+'python')
import caffe

NEUROALGOPATH = os.path.dirname(os.path.abspath(__file__))

class NeuroElement(ElementBase):
    def __init__(self, url, *args, **kwargs):
        super(NeuroElement, self).__init__(url, *args, **kwargs)
        driver = args[0]
        self.image_name = str(int(time.time()))
        self.screen_path = os.path.join(PHISH_NEURO_DIR, self.image_name + '.png')

        get_screenshot(PHISH_NEURO_DIR, self, driver)

        crop_minify(self.screen_path)
        self.screen_path = self.screen_path.replace('.png', '.jpg')



class NeuroSuspicousContainer(Container):
    path = os.path.join(ALGOTMP, 'neuro_algo_tmp/')
    element_class = NeuroElement

    def __init__(self, urls, *args, **kwargs):
        super(NeuroSuspicousContainer, self).__init__(urls, *args, **kwargs)

    def get_data(self):
        pass


class NeuroAlgo(Algorithm):
    suspicious_container_class = NeuroSuspicousContainer
    name = "NEURO_ALGO"
    model_file = os.path.join(NEUROALGOPATH, 'phish_deploy_features_headers_net2.prototxt')
    weights_file = os.path.join(NEUROALGOPATH, 'snapshot_headers_net2/snap.caffemodel')
    pca_file = os.path.join(NEUROALGOPATH, 'PCA3.pkl')

    def __init__(self, filename, *args, **kwargs):
        super(NeuroAlgo, self).__init__(filename, *args, **kwargs)
        self.targets = args[0]

        # caffe.set_mode_gpu();
        # caffe.set_device(0);

        self.net = caffe.Net(self.model_file, self.weights_file, caffe.TEST)
        self.pca = cPickle.load(open(self.pca_file, 'rb'), encoding='latin1')

    def get_answer(self, suspect, verbose=False):
        # у таргетов должны быть координаты
        # для suspect вычисляем features->tsne->координаты
        # вычисляем расстояние до ближайшего таргета (dist)
        # 1/dist запихиваем в 1/(1+x**2) -> получаем вероятность фишинга
        answer = []
        img = caffe.io.load_image(suspect.screen_path)
        img = img[:, :, ::-1] * 255.0  # convert RGB->BGR
        img = img.transpose((2, 0, 1))
        img = img[None, :]  # add singleton dimension
        out = self.net.forward_all(data=img)
        coords = self.pca.transform(out['features'].flatten().reshape(1,-1))
        print(coords)
        i = 0
        for target in self.targets:
            print("target coords")
            print(target.coords)
            newdist = np.sqrt(sum([(coords[0][j]-target.coords[0][j])**2 for j in range(len(coords)) ]))
            #newdist = np.sqrt((tcoords[0]-coords[0])**2+(tcoords[1]-tcoords[1])**2)
            print(newdist)
            prob = 1/(1+0.00001*(newdist**2))
            print(prob)
            answer.append((self.targets[i].name, prob))
            if verbose:
                print('------------------------')
                print('phish and target comparison')
                print('------------------------')

                print('target screen: {0}'.format(self.targets[i].screen_path))
                print('phish screen: {0}'.format(suspect.screen_path))
                print('distance: {0}'.format(newdist))
                print('prob: {0}'.format(prob))

            i += 1

        for target_result in answer:
            if target_result[1] >= 0.8:
                return 1

        return 0


    def answers(self):
        return self.results