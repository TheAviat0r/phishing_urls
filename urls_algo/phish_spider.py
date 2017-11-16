import scrapy
from scrapy.utils.project import get_project_settings


def round_robin(arr):
    to_yield_idx = 0
    length = len(arr)
    while True:
        yield arr[to_yield_idx % length]
        to_yield_idx += 1


class PhishSpider(scrapy.Spider):
    name = "phish"
    handle_httpstatus_list = [200, 302]

    def __init__(self, *args, **kwargs):
        super(PhishSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()
        print(kwargs)
        self.urls = kwargs['urls_objects']
        self.redirect_counter = 0
        self.url_number = 0
        if self.settings['PROXY_LIST']:
            self.proxy_iter = round_robin(self.settings['PROXY_LIST'])

    def start_requests(self):
        for idx in range(len(self.urls)):
            request = scrapy.Request(url=self.urls[idx].url, callback=self.parse, meta={'url_number':idx})
            if self.settings['PROXY_LIST']:
                request.meta['proxy'] = next(self.proxy_iter)
            yield request
            self.url_number += 1

    def parse(self, response):
        if response.status == 200:
            yield {
                'response': response,
                'url_number': response.meta['url_number'],
                'redirect_count': self.redirect_counter
            }
            self.redirect_counter = 0
        if response.status == 302:
            self.redirect_counter += 1
