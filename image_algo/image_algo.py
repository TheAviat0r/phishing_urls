import os, glob

from hash import image_hash, hamming_distance
from selenium import webdriver
from PIL import Image

from config import *

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)

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

def read_urls(urls_file_name):
    urls_file = open(urls_file_name)
    urls = urls_file.read().split()

    urls_to_check = []

    for url in urls:
        phish = PhishUrl(url)
        urls_to_check.append(phish)

    print(urls_to_check)

    return urls_to_check

def get_screenshot(image_dir, website, verbose=False):
    if verbose:
        print('get_screenshot:')
        print(image_dir)

    if not os.path.exists(image_dir):
        if verbose:
            print('DIRECTORY CREATED: ' + image_dir)
        os.mkdir(image_dir)

    driver.get(website.url)

    if os.path.exists(website.screen_path):
        if verbose:
            print('website was already screened: ' + website.screen_path)
        os.remove(website.screen_path)

    driver.save_screenshot(website.screen_path)

def image_algorithm(urls_file_name):
    suspicious_sites = read_urls(urls_file_name)

    for site in suspicious_sites:
        print(site)

    targets = []

    for target_name, target_url in source_websites.items():
        target = Target(target_name, target_url)
        targets.append(target)

    for target in targets:
        print(target)

    processing_result = []

    for site in suspicious_sites:
        compare_with_targets(site, targets)

        processing_result.append(site.get_output())
        assert site.is_checked == True
        if site.fishing_by_image:
            print('{} - PHISHING to {}'.format(site.image_name.ljust(20), site.target.name))
        else:
            print('{} - VALID'.format(site.name.ljust(20)))

    return processing_result

class PhishUrl:
    def __init__(self, url):
        self.url = url
        self.image_name = url[7:]
        self.screen_path = PHISH_IMAGE_DIR + '/' + self.image_name + '.png'

        get_screenshot(PHISH_IMAGE_DIR, self)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        self.target = None
        self.fishing_by_image = False
        self.is_checked = False

    def __str__(self):
        output = '------------------------\n'
        output += 'phish url dump\n'
        output += 'url: ' + self.url + '\n'
        output += 'screen path: ' + self.screen_path + '\n'
        output += 'hash: ' + self.hash + '\n'
        output += '------------------------\n'
        return output

    def compare(self, target, verbose=False):
        hash_len = len(target.hash)
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

        if distance < 0.5 * hash_len:
            return True
        else:
            return False

    def get_output(self):
        return (self.url, self.fishing_by_image)


class Target:
    def __init__(self, target_name, login_url):
        self.name = target_name
        self.url = login_url
        self.screen_path = TARGET_IMAGE_DIR + '/' + self.name + '.png'

        get_screenshot(TARGET_IMAGE_DIR, self)

        self.hash = image_hash(self.screen_path, hash_size=DEFAULT_HASH_SIZE)
        with Image.open(self.screen_path) as image:
            self.image = image


    def __str__(self):
        output = '------------------------\n'
        output += 'target_name: ' + self.name + '\n'
        output += 'login_url: ' + self.url + '\n'
        output += 'screen_path: ' + self.screen_path + '\n'
        output += 'image_hash: ' + self.hash + '\n'
        output += '------------------------'
        
        return output

if __name__ == '__main__':
    result = image_algorithm('urls.txt')
    print(result)
    driver.quit()
