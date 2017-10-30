import os

from container import ElementBase
from image_algo.config import TARGET_IMAGE_DIR, DEFAULT_HASH_SIZE
from image_algo.image_algo import get_screenshot
from .hash import image_hash
from PIL import Image


class ImageAlgoTarget(ElementBase):
    def __init__(self, url, target_name, driver, *args, **kwargs):
        super(ImageAlgoTarget, self).__init__(url, *args, **kwargs)
        self.name = target_name
        self.screen_path = TARGET_IMAGE_DIR + '/' + self.name + '.png'

        get_screenshot(TARGET_IMAGE_DIR, self, driver)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        with Image.open(self.screen_path) as image:
            self.image = image

    def __str__(self):
        output = '------------------------\n'
        output += 'target_name: ' + self.name + '\n'
        output += 'url: ' + self.url + '\n'
        output += 'screen_path: ' + self.screen_path + '\n'
        output += 'image_hash: ' + self.hash + '\n'
        output += '------------------------'

        return output