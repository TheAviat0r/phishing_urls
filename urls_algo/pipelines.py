# -*- coding: utf-8 -*-
import os

import errno

import datetime
import re

from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import subprocess
import requests
from IPy import IP
import csv

from global_config import ALGOTMP


def url_analyse(url):
    ip_in_url = 0
    is_long_url = 0
    is_shortened_url = 0
    at_in_url = 0
    is_redirect = 0
    dash_in_domain = 0
    subdomain_depth = 0
    is_https = 0
    registration_length = 0
    has_non_standart_ports = 0
    https_in_domain = 0

    age_of_domain = 0
    dns_record = 0

    has_digits = 0
    has_phish_terms = 0

    standart_ports = {21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389}
    phish_terms = {"log", "pay", "web", "cmd", "account", "dispatch", "free", "confirm"}

    domain = urlparse(url).netloc

    try:
        ip_in_url = IP(domain)
        ip_in_url = 1
    except ValueError as e:
        pass

    is_long_url = len(url)

    try:
        resp = requests.get(url, allow_redirects=False)
        if resp.status_code < 300 and resp.url != url:
            is_tiny_url = 1
    except requests.exceptions.ConnectionError as e:
        pass

    if "@" in url:
        at_in_url = 1

    if url.count("//") > 1:
        is_redirect = 1

    if "-" in domain:
        dash_in_domain = 1

    # Count number of subdomains, but ignore top level domain and www, if it is present
    subdomain_depth = domain.count(".")
    if "www." in url:
        subdomain_depth -= 1

    if url.startswith("https"):
        is_https = 1

    p = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    if out.startswith("No match for"):
        pass
    else:
        dns_record = 1
        searchDate = re.search(r'Creation Date: (.*)', out)
        if searchDate:
            registration_date = searchDate.group(1)
            registration_months = int(registration_date[:4]) * 12 + int(registration_date[5:7])
            now = datetime.datetime.now()
            months_now = 12 * now.year + now.month
            if months_now - registration_months >= 6:
                registration_length = 1
                age_of_domain = 1

    port_tokens = url.split(":")
    try:
        if len(port_tokens) > 1:

            port = int(port_tokens[-1])
            if port not in standart_ports:
                has_non_standart_ports = 1
    except ValueError:
        pass

    if "https" in domain:
        https_in_domain = 1

    if(any(char.isdigit() for char in domain)):
        has_digits = 1

    for phish_term in phish_terms:
        if phish_term in domain:
            has_phish_terms = 1
            break



    return (
            ("https_in_domain", https_in_domain),
            ("registration_length", registration_length),
            ("is_redirect", is_redirect),
            ("age_of_domain", age_of_domain),
            ("is_long_url", is_long_url),
            ("is_shortened_url", is_shortened_url),
            ("at_in_url", at_in_url),
            ("ip_in_url", ip_in_url),
            ("is_https", is_https),
            ("dash_in_domain", dash_in_domain),
            ("subdomain_depth", subdomain_depth),
            ("dns_record", dns_record),
            ("has_non_standart_ports", has_non_standart_ports),
            ("has_digits", has_digits),
            ("has_phish_terms", has_phish_terms)
        )


class SaveHtmlFilesAndProcessFeaturesPipeline(object):
    def process_item(self, item, spider):
        features = url_analyse(item['response'].url)

        filename = os.path.join(ALGOTMP, 'urls_algo_tmp/scrapyres/features.csv')
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'a') as f:
            row = '%d,' % item['url_number']
            flen = len(features)
            for idx in range(flen):
                row += str(features[idx][1])
                if idx != flen-1:
                    row += ','
                else:
                    row += '\n'
            f.write(row)


