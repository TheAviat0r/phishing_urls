import logging
import os

GLOBAL_PATH = os.path.dirname(os.path.abspath(__file__))

QUEUE_HOST = 'localhost'
URL_ALGO_QUEUE = 'url_algo_queue'
ANSWER_QUEUE = 'answer_queue'

URL_WORKERS_AMOUNT = 1

TELEGRAM_TOKEN = open(os.path.join(GLOBAL_PATH,"tgtoken"), "r").readline().replace("\n", "")

SUPPLY_PATH = os.path.join(GLOBAL_PATH, 'supply/')

ALGOTMP = os.path.join(GLOBAL_PATH, 'algotmp/')

BAD_SAMPLE_CONSTANT = -9999

CHUNK_SIZE = 10

LOGLEVEL = logging.WARNING
logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOGLEVEL)

