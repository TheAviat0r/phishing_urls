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
    path = os.path.join(ALGOTMP, 'image_algo_tmp/')
    element_class = ImageElement

    def __init__(self, urls, *args, **kwargs):
        super(ImageSuspicousContainer, self).__init__(urls, *args, **kwargs)

    def get_data(self):
        pass


class ImageAlgo(Algorithm):
    suspicious_container_class = ImageSuspicousContainer

    def __init__(self, filename, *args, **kwargs):
        super(ImageAlgo, self).__init__(filename, *args, **kwargs)
        self.targets = args[0]

    def get_answer(self, suspect, verbose=False):
        answers = []
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
                answers.append((target.name, 1))
            else:
                answers.append((target.name, 0))
        return answers

    def answers(self):
        output = "====================\n"
        for elem in self.results:
            output += elem[0].url + "\n"
            flag = 0
            flagcheckfailed = 0
            for siteres in elem[1]:
                if siteres[1] == 0:
                    output += "---> %s." % siteres[0] + bcolors.OKGREEN + " Not similar" + bcolors.ENDC + "\n"
                if siteres[1] == 1:
                    flag = 1
                    output += "---> %s." % siteres[0] + bcolors.FAIL + " Similar!" + bcolors.ENDC + "\n"
                if len(siteres) < 2:
                    flagcheckfailed = 1
                    output += "---> %s." % siteres[0] + bcolors.WARNING + " Check failed" + bcolors.ENDC + "\n"
            if flagcheckfailed == 0:
                if flag == 1:
                    output += elem[0].url + " --->" + bcolors.FAIL + " Phishing" + bcolors.ENDC + "\n"
                if flag == 0:
                    output += elem[0].url + " --->" + bcolors.OKGREEN + " Not phishing" + bcolors.ENDC + "\n"
            else:
                output += bcolors.WARNING + "Some checks failed" + bcolors.ENDC + "\n"
                if flag == 1:
                    output += elem[0].url + " --->" + bcolors.FAIL + " Phishing" + bcolors.ENDC + "\n"
            output += "====================\n"
        print(output)


