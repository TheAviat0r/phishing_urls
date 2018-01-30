import datetime
import re
from urllib.parse import urlparse
import requests
import subprocess
from IPy import IP
from api import get_alexa, get_semrush
import sys


def url_analyse(url):
    ip_in_url = 0
    is_long_url = 0
    is_tiny_url = 0
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
    alexa_rank = sys.maxsize
    semrush = 0
    standart_ports = {21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389}
    phish_terms = {"log", "pay", "web", "cmd", "account", "dispatch", "free", "confirm", "login", "secure", "web", "app"}
    tiny_url_services = ["goo.gl", "bit.ly", "tinyurl.com", "tiny.cc", "lc.chat", "is.gd", "soo.gd", "s2r.co", "clicky.me", "budurl.com", "bc.vc", "i-to.cc"]
    whois_not_found = ["No entries found", "No match for", "No whois server is known", "No Data", "NOT FOUND"]

    if any(x in url for x in tiny_url_services):
        is_tiny_url = 1

    try:
        resp = requests.get(url, timeout=(15,15))
        if resp.history:
            is_redirect = 1
            url = resp.url
        if url.startswith("https"):
            is_https = 1
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects) as e:
        pass
    except requests.exceptions.SSLError:
        is_https = 0

    domain = urlparse(url).netloc

    try:
        ip_in_url = IP(domain)
        ip_in_url = 1
    except ValueError as e:
        pass

    is_long_url = len(url)
    if is_long_url < 20:
        is_long_url = 0
    elif is_long_url < 50:
        is_long_url = 1
    else:
        is_long_url = 2

    if "@" in url:
        at_in_url = 1

    if "-" in domain:
        dash_in_domain = 1

    # Count number of subdomains, but ignore top level domain and www, if it is present
    subdomain_depth = domain.count(".")
    if "www." in url:
        subdomain_depth -= 1
        domain = domain[4:]


    try:
        p = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            out = out.decode('utf-8')
        if err:
            err = err.decode('utf-8')
        if not any(x in out for x in whois_not_found):
            dns_record = 1
            searchDate = re.search(r'(Creation Date: |created:       )(.*)', out)
            if searchDate:
                registration_date = searchDate.group(2)
                registration_months = int(registration_date[:4]) * 12 + int(registration_date[5:7])
                now = datetime.datetime.now()
                months_now = 12 * now.year + now.month
                if months_now - registration_months >= 6:
                    age_of_domain = 1
            searchDate = re.search(r'(Registry Expiry Date: |paid-till:     )(.*)', out)
            if searchDate:
                registration_date = searchDate.group(2)
                registration_months = int(registration_date[:4]) * 12 + int(registration_date[5:7])
                now = datetime.datetime.now()
                months_now = 12 * now.year + now.month
                if registration_months - months_now >= 6:
                    registration_length = 1
        else:
            pass
    except TypeError:
        pass

    alexa_rank = get_alexa(url)
    if alexa_rank == None:
        alexa_rank = sys.maxsize
    semrush = get_semrush(url)
    if semrush == None:
        semrush = 0

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

    if (any(char.isdigit() for char in domain)):
        has_digits = 1

    for phish_term in phish_terms:
        if phish_term in url:
            has_phish_terms = 1
            break


    return [
            ("https_in_domain", https_in_domain),
            ("registration_length", registration_length),
            ("is_redirect", is_redirect),
            ("age_of_domain", age_of_domain),
            ("is_long_url", is_long_url),
            ("is_tiny_url", is_tiny_url),
            ("at_in_url", at_in_url),
            ("ip_in_url", ip_in_url),
            ("is_https", is_https),
            ("dash_in_domain", dash_in_domain),
            ("subdomain_depth", subdomain_depth),
            ("dns_record", dns_record),
            ("has_non_standart_ports", has_non_standart_ports),
            ("has_digits", has_digits),
            ("has_phish_terms", has_phish_terms),
            ("alexa_rank", alexa_rank),
            ("semrush", semrush)
        ]
