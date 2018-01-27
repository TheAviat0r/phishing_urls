import time

from algo import Algorithm
from bcolors import bcolors
from container import Container, ElementBase
from global_config import ALGOTMP
from image_algo.hash import image_hash, hamming_distance
from image_algo.helpers.screenshot import get_screenshot

from .config import *


class ImageElement(ElementBase):
    def __init__(self, url, *args, **kwargs):
        super(ImageElement, self).__init__(url, *args, **kwargs)
        driver = args[0]
        self.image_name = str(int(time.time()))
        self.screen_path = os.path.join(PHISH_IMAGE_DIR, self.image_name + '.png')

        get_screenshot(PHISH_IMAGE_DIR, self, driver)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        self.target = None
        self.fishing_by_image = False
        self.is_checked = False


class ImageSuspicousContainer(Container):
    path = os.path.join(Container.path, 'image_algo_tmp/')
    element_class = ImageElement

    def __init__(self, urls, *args, **kwargs):
        super(ImageSuspicousContainer, self).__init__(urls, *args, **kwargs)

    def get_data(self):
        pass


class ImageAlgo(Algorithm):
    suspicious_container_class = ImageSuspicousContainer
    name = "IMAGE ALGO"

    def __init__(self, filename, *args, **kwargs):
        super(ImageAlgo, self).__init__(filename, *args, **kwargs)
        self.targets = args[0]

    def get_answer(self, suspect, verbose=False):
        answer = []
        for target in self.targets:
            hash_len = len(target.hash)
            distance = hamming_distance(target.hash, suspect.hash)

            if verbose:
                print('------------------------')
                print('phish and target comparison')
                print('------------------------')

                print('target screen: {0}'.format(target.screen_path))
                print('phish screen: {0}'.format(suspect.screen_path))
                print('target hash: {0}'.format(target.hash))
                print('phish hash: {0}'.format(suspect.hash))

                print('"{0}" and "{1}" distance: {2} / {3}'.format(target.target_name,
                                                                   suspect.image_name,
                                                                   distance, len(suspect.hash)))

            probability = 1 - distance/hash_len
            answer.append(probability)

        return max(answer)


    def answers(self):
        return self.results


