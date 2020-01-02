from telegram.ext import CommandHandler, MessageHandler, Filters
import logging

import messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler('activity.log')
fileHandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname): %(message)s')
fileHandler.setFormatter(formatter)

logger.addHandler(handler)

def send_message(bot, chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
    except:
        logger.error('There is no chat with id {}'.format(chat_id))

def unknown_command(bot, update):
    logging.warn("{} called an unknown {} command!".format(
        update.message.chat_id,
        update.message.text
    ))

    send_message(bot, update.message.chat_id, messages.unknown_command_response)

def start(bot, update):
    logger.info('{} started conversation'.format(update.message.chat_id))
    send_message(bot, update.message.chat_id, messages.start_response)

def any_message_log(bot, update):
    """
    What I want this function to do, is to log any message
    that is written by anybody, show a short snippet of
    message in the logs and then store the full text some-
    where in the file. The problem is that if somebody
    would spam the bot and take up the whole space on the
    disk. If you have any ideas on how to do it ingenious-
    ly, I am listening.
    """
    pass

start_handler = CommandHandler('start', start)
any_message_handler = MessageHandler(Filters.text, any_message_log)
unknown_command_handler = MessageHandler(Filters.command, unknown_command)

bot_handlers = [
    start_handler,
    any_message_handler,
    unknown_command_handler
]
