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
import pika
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import _pickle as cPickle

# Enable logging
from global_config import TELEGRAM_TOKEN, URL_ALGO_QUEUE, QUEUE_HOST, URL_WORKERS_AMOUNT
from util import chunks, submit_to_queue

logger = logging.getLogger(__name__)
logger.info("Starting...")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    if re.search('DO_NOT_BAN', update.message.text):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                           update.message.text)
        reply = ''
        for url in urls:
            reply = reply + url + ' '
        while True:
            try:
                logger.debug("Trying to send message")
                if update.message.reply_text("WARNING: do not ban %s" % (reply), timeout=10):
                    break
            except telegram.error.TimedOut:
                logger.warning("Timeout error, will try to resend message")
        return

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      update.message.text)

    if urls:
        logger.info("Got %s" % urls)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=URL_ALGO_QUEUE, durable=True)
        for url_chunk in chunks(urls, len(urls) // URL_WORKERS_AMOUNT):
            logger.debug("Sending %s" % url_chunk)
            submit_to_queue(channel, URL_ALGO_QUEUE, cPickle.dumps((url_chunk, update)))
            logger.debug("Submitted to %s queue" % URL_ALGO_QUEUE)
        connection.close()
        # update.message.reply_text(str(urls))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
