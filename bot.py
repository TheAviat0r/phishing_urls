#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import json

import pika
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import _pickle as cPickle

# Enable logging
from global_config import TELEGRAM_TOKEN, URL_ALGO_QUEUE, QUEUE_HOST, URL_WORKERS_AMOUNT
from util import chunks, submit_to_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    urls = re.findall('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
                      update.message.text)
    if urls:
        for url_chunk in chunks(urls, len(urls) // URL_WORKERS_AMOUNT):
            print(url_chunk)
            submit_to_queue(channel, URL_ALGO_QUEUE, cPickle.dumps((url_chunk, update)))
    # update.message.reply_text(str(urls))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def test_func(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('ААААА БЛЯ КАК БОМБИТ ТО!!!!!')


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("sosi_hui_bot", test_func))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(timeout=0)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST, heartbeat=0))
    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)

    channel.queue_declare(queue=URL_ALGO_QUEUE, durable=True)
    main()
