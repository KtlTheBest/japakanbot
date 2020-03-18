from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, RegexHandler, MessageHandler

import logging
import os

import tasks

import bot_states

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getToken():
    token = ""
    name = 'token'
    with open(name) as f:
        logger.debug("Opened token file")
        token = f.readline().rstrip()
        logger.debug("BOT_TOKEN value set to token from file")
        logger.debug("TOKEN value is {}".format(token))

    return token

def main():
    logger.debug("Start of the script")
    updater = Updater(getToken(), use_context = True)
    logger.info("Initiated updater")

    logger.debug("Started initiating Command Handlers")
    start_handler = CommandHandler('start', tasks.start_task)
    help_handler = CommandHandler('help', tasks.help_task)
    quiz_handler = CommandHandler('quiz', tasks.quiz_task)
    ask_questions_handler = MessageHandler(Filters.text, tasks.askQuestions)
    logger.info("Initiated all Command Handlders")

    logger.debug("Started initiating Conversation Handler")
    quiz_conversation_handler = ConversationHandler(
            entry_points = [quiz_handler, ask_questions_handler],
            states = {
                bot_states.QUESTIONS: [ask_questions_handler]
                },
            fallbacks=[MessageHandler(Filters.regex('[/]*'), tasks.done)]
            )
    logger.info("Initiated Conversation Handler")

    bot_handlers = [
            start_handler,
            help_handler,
            quiz_handler,
            quiz_conversation_handler
            ]

    for handler in bot_handlers:
        updater.dispatcher.add_handler(handler)

    updater.start_polling()
    logger.info("Started polling")

if __name__ == "__main__":
    main()
