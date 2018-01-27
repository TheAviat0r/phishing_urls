import os
GLOBAL_PATH = os.path.dirname(os.path.abspath(__file__))

QUEUE_HOST = 'localhost'
URL_ALGO_QUEUE = 'url_algo_queue'
IMAGE_ALGO_QUEUE = 'image_algo_queue'
NEURO_ALGO_QUEUE = 'neuro_algo_queue'
ANSWER_QUEUE = 'answer_queue'

URL_WORKERS_AMOUNT = 1
IMAGE_WORKERS_AMOUNT = 1
NEURO_WORKERS_AMOUNT = 1

ENABLE_WEB_INTERFACE = 0


TELEGRAM_TOKEN = open("tgtoken", "r").readline().replace("\n", "")

source_websites = {
    'PayPal' : 'https://www.paypal.com/signin?country.x=US',
    'Mail' : 'https://mail.ru/',
    'Blizzard' : 'https://us.battle.net/login/en/',
}

SUPPLY_PATH = os.path.join(GLOBAL_PATH, 'supply/')

ALGOTMP = os.path.join(GLOBAL_PATH, 'algotmp/')

BAD_SAMPLE_CONSTANT = -9999

CHUNK_SIZE = 10
