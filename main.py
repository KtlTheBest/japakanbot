from telegram.ext import Updater
import logging
import os
import schedule
from tasks import startQuiz

# My files

import handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getToken():
    token = ""
    name = 'token'
    with open(name) as f:
        logger.debug("Opened token file")
        token = f.readline().rstrip()
        logger.debug("BOT_TOKEN value set to token from file")

    return token

def loadBot():
    global updater
    token = getToken()
    updater = Updater(token)

def main():
    logger.info("Script started")
    loadBot()
    logger.info("Initiated bot")

    for handler in handlers.bot_handlers:
        updater.dispatcher.add_handler(handler)

    updater.start_polling()

    schedule.every().day.at("12:00").do(startQuiz)

if __name__ == "__main__":
    main()
