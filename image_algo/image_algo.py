
from algo import Algorithm
from container import Container, ElementBase
from global_config import ALGOTMP
from image_algo.helpers.screenshot import get_screenshot
from .hash import image_hash, hamming_distance

from .config import *


class ImageElement(ElementBase):
    def __init__(self, url, *args, **kwargs):
        super(ImageElement).__init__(url, args, kwargs)
        driver = args[0]
        self.image_name = url[7:]
        self.screen_path = PHISH_IMAGE_DIR + '/' + self.image_name + '.png'

        get_screenshot(PHISH_IMAGE_DIR, self, driver)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        self.target = None
        self.fishing_by_image = False
        self.is_checked = False


class ImageSuspicousContainer(Container):
    path = os.path.join(ALGOTMP, 'image_algo_tmp/')
    element_class = ImageElement

    def __init__(self, urls, *args, **kwargs):
        super(ImageSuspicousContainer).__init__(urls, args, kwargs)

    def get_data(self):
        pass


class ImageAlgo(Algorithm):
    suspicious_container_class = ImageSuspicousContainer

    def __init__(self, filename, *args, **kwargs):
        super(ImageAlgo).__init__(filename, args, kwargs)
        self.targets = args[0]

    def get_answer(self, suspect, verbose=False):
        answs = []
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

            if distance < 0.5 * hash_len:
                answs.append((target.target_name, 1))
            else:
                answs.append((target.target_name, 0))

    def answers(self):
        for elem in self.results:
            elem[0].__str__()
            if elem[1][1] == 0:
                print('Algorithm suppose that %s site is not similar' % elem[1][0])
            else:
                print('Phishing! Tries to compromise %s' % elem[1][0])

