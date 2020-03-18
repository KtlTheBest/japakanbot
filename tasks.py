import os
import random
import pandas as pd

import logging

import bot_messages
import bot_states

from telegram.ext import ConversationHandler

logger = logging.getLogger(__name__)

KANJI_FILE = "data.csv"

def chooseRandom():
    logger.debug("Got into 'chooseRandom' function")
    kanjifile = open(KANJI_FILE)
    logger.debug("Opened KANJI_FILE: {}".format(KANJI_FILE))
    csv_reader = csv.reader(kanjifile, delimiter = ',')
    logger.debug("Read csv file and loaded kanji into csv_reader")
    kanjifile.close()
    logger.debug("Closed {} file".format(KANJI_FILE))

    ids = []
    q = []
    while len(ids) != 30:
        val = random.randint(0, len(csv_reader) - 1)
        if val not in ids:
            ids.append(val)
            q.append((val, csv_reader[0], csv_reader[1]))

    return q

def getNewQuestion():
    logger.debug("Got into 'getNewQuestion' function")
    df = pd.read_csv(KANJI_FILE)
    logger.debug("Read csv file and loaded kanji into DataFrame")
    randrow = random.randrange(0, len(df))
    logger.debug("Generated random number {}".format(randrow))
    k = df.loc[randrow, 'kanji']
    a = df.loc[randrow, 'tran']
    i = df.loc[randrow, 'id']
    logger.debug("Successfully got all the data: i - {}, k - {}, a - {}".format(i, k, a))
    return k, a, i

def start_task(update, context):
    logger.info("Got /start message from {}".format(update.message.chat_id))
    newFile = open(str(update.message.chat_id) + ".csv", "w")
    logger.debug("Opened a file {}.csv".format(update.message.chat_id))
    newFile.write("id,count\n")
    newFile.close()
    logger.debug("Initiated csv file")
    update.message.reply_html(bot_messages.START)
    logger.debug("Sent a bot_messages.START message to {}".format(update.message_chat_id))
    return ConversationHandler.END

def help_task(update, context):
    logger.info("Received /help message from {}".format(update.message.chat_id))
    update.message.reply_html(bot_messages.HELP)
    logger.debug("Sent bot_messages.HELP to {}".format(update.message.chat_id))
    return ConversationHandler.END

def quiz_task(update, context):
    logger.info("Preparing a quiz for {}".format(update.message.chat_id))
    context.user_data['n'] = 0
    return askQuestions(update, context)

def askQuestions(update, context):
    logger.info("Got into askQuestions by request from {}".format(update.message.chat_id))
    questionNo = context.user_data['n']
    if questionNo != 0:
        userAns = update.message.text
        corrAns = context.user_data['a']
        k = context.user_data['k']

        if userAns.lower() != corrAns.lower():
            logger.debug("The answer by {} is wrong!".format(update.message.chat_id))
            update.message.reply_html(bot_messages.INCORRECT_ANSWER.format(corrAns, k))
            logger.debug("Sent bot_messages.INCORRECT_ANSWER to {}".format(update.message.chat_id))
            return bot_states.QUESTIONS

        logger.debug("The answer by {} is right!".format(update.message.chat_id))
        update.message.reply_html(bot_messages.CORRECT_ANSWER)
        logger.debug("Sent bot_messages.CORRECT_ANSWER to {}".format(update.message.chat_id))

    k, a, i = getNewQuestion()
    logger.debug("Generated a new question for {}".format(update.message.chat_id))

    update.message.reply_html(bot_messages.NEW_QUESTION.format(k))
    logger.debug("Sent bot_messages.NEW_QUESTION to {}".format(update.message.chat_id))
    context.user_data['k'] = k
    context.user_data['a'] = a
    context.user_data['i'] = i
    logger.debug("Updated question context for {}".format(update.message.chat_id))

    if questionNo == 30:
        logger.info("The quiz for {} is finished!".format(update.message.chat_id))
        update.message.reply_html(bot_messages.QUIZ_FINISH)
        logger.debug("Sent bot_messages.QUIZ_FINISH to {}".format(update.message.chat_id))
        return ConversationHandler.END

    context.user_data['n'] = questionNo + 1
    logger.debug("Updated questionNo context for {} which is now {}".format(update.message.chat_id, questionNo + 1))

    return bot_states.QUESTIONS

def done(update, context):
    logger.info("Executing done() for {}".format(update.message.chat_id))
    update.message.reply_html(bot_messages.ABORT)
    logger.debug("Sent bot_messages.ABORT to {}".format(update.message.chat_id))
    return ConversationHandler.END
