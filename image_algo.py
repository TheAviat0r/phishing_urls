import os, glob

from hash import image_hash, hamming_distance
from selenium import webdriver
from PIL import Image

from config import *

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)

class PhishUrl:
    def __init__(self, url, image_name):
        self.url = url
        self.image_name = image_name
        self.screen_path = PHISH_IMAGE_DIR + '/' + image_name
        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        self.target = None
        self.fishing_by_image = False
        self.is_checked = False

    def __str__(self):
        output = '------------------------\n'
        output += 'phish url dump'
        output += 'url: ' + self.url + '\n'
        output += 'screen path: ' + self.screen_path + '\n'
        output += 'hash: ' + self.hash + '\n'
        output += '------------------------\n'
        return output

    def compare(self, target, verbose=False):
        distance = hamming_distance(target.hash, self.hash)

        if verbose:
            print('------------------------')
            print('phish and target comparison')
            print('------------------------')

            print('target screen: {0}'.format(target.screen_path))
            print('phish screen: {0}'.format(self.screen_path))
            print('target hash: {0}'.format(target.hash))
            print('phish hash: {0}'.format(self.hash))

            print('"{0}" and "{1}" distance: {2} / {3}'.format(target.target_name,
                                                               self.image_name,
                                                               distance, len(self.hash)))

        if distance / len(self.hash) <= 0.5:
            return True
        else:
            return False

class Target:
    def __init__(self, target_name, login_url):
        self.target_name = target_name
        self.login_url = login_url
        self.screen_path = TARGET_IMAGE_DIR + '/' + self.target_name + '.png'

        self.get_screenshot(self.login_url)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        with Image.open(self.screen_path) as image:
            self.image = image

    def get_screenshot(self, login_url):
        if not os.path.exists(TARGET_IMAGE_DIR):
            os.mkdir(TARGET_IMAGE_DIR)

        if not os.path.exists(self.screen_path):
            driver.get(login_url)
            if os.path.exists(self.screen_path):
                os.remove(self.screen_path)
            driver.save_screenshot(self.screen_path)

    def __str__(self):
        output = '------------------------\n'
        output += 'target_name: ' + self.target_name + '\n'
        output += 'login_url: ' + self.login_url + '\n'
        output += 'screen_path: ' + self.screen_path + '\n'
        output += 'image_hash: ' + self.hash + '\n'
        output += '------------------------'
        
        return output

def compare_with_targets(phish, targets):
    for target in targets:
        result = phish.compare(target)
        if result:
            phish.target = target
            phish.is_checked = True
            phish.fishing_by_image = True
            return
    
    assert phish.target == None
    phish.is_checked = True
    phish.is_finish = False

def run_algorithm():
    targets = []

    for target_name, target_url in source_websites.items():
        target = Target(target_name, target_url)
        targets.append(target)

    suspicious_sites = []

    for root, dirs, files in os.walk(PHISH_IMAGE_DIR, topdown=False):
        for image in files:
            if image.endswith('.jpg') or image.endswith('.png'):
                phish = PhishUrl('test', image)
                suspicious_sites.append(phish)

    for site in suspicious_sites:
        compare_with_targets(site, targets)
        assert site.is_checked == True
        if site.fishing_by_image:
            print('{} - PHISHING to {}'.format(site.image_name.ljust(20), site.target.target_name))
        else:
            print('{} - VALID'.format(site.image_name.ljust(20)))

if __name__ == '__main__':
    run_algorithm()
