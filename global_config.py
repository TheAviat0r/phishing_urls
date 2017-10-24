import os
GLOBAL_PATH = os.path.dirname(os.path.abspath(__file__))

source_websites = {
    'PayPal' : 'https://www.paypal.com/signin?country.x=US',
    'Mail' : 'https://mail.ru',
    'Blizzard' : 'https://us.battle.net/login/en/',
}

SUPPLY_PATH = os.path.join(GLOBAL_PATH, 'supply/')

ALGOTMP = os.path.join(GLOBAL_PATH, 'algotmp/')

