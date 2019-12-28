import telegram
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN

def getToken():
    global BOT_TOKEN
    name = 'token'
    with open(name) as f:
        logger.debug("Opened token file")
        BOT_TOKEN = f.readline().rstrip()
        logger.debug("BOT_TOKEN value set to token from file")

def main():
    logger.info("Script started")
    getToken()
    logger.info("Got bot token")


    pass

if __name__ == "__main__":
    main()
