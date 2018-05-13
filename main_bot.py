'''
 Main module on project "Telegram Bot"
 Describes telegram bot commands and launches it
 Version: beto 1.0
 Creator: Levashov Artem, MIPT DIHT 790, 2018
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from wiki_parse import TrainRequest
from text_generator import train, generate
from statistics import PreCountStat, NonDefinedOrder
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Constant string for message, while bot is not trained yet
NOT_TRAINED_MSG = "Model is not trained yet! Give me wikipedia or " \
                  "wikia link to train."


def start(bot, update):
    '''/start handler'''
    chat = update.message.chat_id
    sender = update.message.from_user.username
    bot.send_message(chat_id=chat,
                     text='Hello, @{}! I\'m ready to work!'.format(sender))


def train_bot(bot, update):
    '''/echo handler - trains bot on given article'''
    r = TrainRequest(update.message.text)
    user = update.message.from_user.username
    # Path to save this users model
    path = os.path.join(os.getcwd(), 'models_stats')
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        train.train_model(r.article, r.max_depth, path, user)
        bot.send_message(chat_id=update.message.chat_id,
                         text='I\'m successfully trained on article {} '
                              'from {} wiki with search recursion {}'
                              ''.format(r.article.header,
                                        r.article.wiki, r.max_depth))
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Oops, something went wrong!'
                              ' Error is: \n' + str(e))


def help_command(bot, update):
    '''/help handler'''
    bot.send_message(chat_id=update.message.chat_id,
                     text='Hello! I can train on articles from wikipedia '
                          'and wikia projects and then generate texts '
                          'or visualise data.\n\nYou can send me message in '
                          'format "<article> N", where:\n\nN - depth of search '
                          '(default is 1 - only given article),\n'
                          '<article> can be:\n'
                          ' - link to article on wikipedia or wikia project;\n'
                          ' - name of article on wikipedia;\n'
                          ' - <wikia_name>.wikia <name_of_article>\n\n'
                          'Supported commands:\n'
                          '/help - shows available commands of this bot\n'
                          '/write N - generate sequence based on trained model'
                          ' with length of N words\n'
                          '/top N (asc | desc) - find N most (or less) frequent'
                          'words in model\n'
                          '/stopwords - find all stop words in trained model'
                          'In all commands default N is 10')


def write(bot, update):
    '''/write N handler - generates N words from model'''
    cmd = update.message.text.split()
    try:
        if len(cmd) > 2:
            msg_text = 'Invalid command syntax! Usage: \n' \
                       '/write N'
        else:
            n = 10
            if len(cmd) > 1:
                n = int(cmd[1])
            user_model = '{}_model.txt'.format(update.message.from_user.username)
            path = os.path.join(os.getcwd(), 'models_stats', user_model)
            if os.path.exists(path):
                msg_text = generate.generate_sequence(path, n)
            else:
                msg_text = NOT_TRAINED_MSG
    except ValueError:
        msg_text = 'N must be an integer value!'
    except generate.NonPositiveLength:
        msg_text = 'N must be positive!'
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg_text)


def find_top(bot, update):
    '''/top N handler - finds most or least N frequent words in model'''
    cmd = update.message.text.split()
    invalid_syntax = 'Invalid command syntax! Usage: \n /top N (asc | desc)'
    try:
        if len(cmd) > 3:
            msg_text = invalid_syntax
        else:
            user_stats = '{}_stats.txt'.format(update.message.from_user.username)
            path = os.path.join(os.getcwd(), 'models_stats', user_stats)
            order = 'asc'
            n = 10
            if len(cmd) > 1:
                n = int(cmd[1])
                if len(cmd) == 3:
                    order = cmd[-1]
            if os.path.exists(path):
                stat = PreCountStat(path)
                words_freq = stat.find_top(n, order)
                msg_text = 'Top {} {} frequently words:\n'.format(
                    n, 'most' if order == 'asc' else 'least')
                for word, freq in words_freq.items():
                    msg_text += '{} - {}\n'.format(word, freq)
            else:
                msg_text = NOT_TRAINED_MSG
    except ValueError:
        msg_text = 'N must be an integer value!'
    except generate.NonPositiveLength:
        msg_text = 'N must be positive!'
    except NonDefinedOrder:
        msg_text = invalid_syntax
    bot.send_message(chat_id=update.message.chat_id, text=msg_text)


def stop_words(bot, update):
    '''/stopwords - find 'stop words' which are far from mean frequency '''
    cmd = update.message.text.split()
    if len(cmd) > 1:
        msg_text = 'Invalid command syntax! Usage:\n /stopwords'
    else:
        user_stats = '{}_stats.txt'.format(update.message.from_user.username)
        path = os.path.join(os.getcwd(), 'models_stats', user_stats)
        if os.path.exists(path):
            stat = PreCountStat(path)
            ejections = stat.stop_words()
            msg_text = 'Stop words in model are:\n'
            for word, freq in ejections.items():
                msg_text += '{} - {}\n'.format(word, freq)
        else:
            msg_text = NOT_TRAINED_MSG
    bot.send_message(chat_id=update.message.chat_id, text=msg_text)


def main():

    # Creating bot and bots dispatcher
    bot = Updater(token='561528667:AAFYbWaz2mUBVMGcg3pmm8jqdwrjmgP1Urg')
    dispatcher = bot.dispatcher

    # Assigning handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    echo_handler = MessageHandler(Filters.text, train_bot)
    write_handler = CommandHandler('write', write)
    top_handler = CommandHandler('top', find_top)
    stopwords_handler = CommandHandler('stopwords', stop_words)

    # Adding handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(write_handler)
    dispatcher.add_handler(top_handler)
    dispatcher.add_handler(stopwords_handler)

    # Start bot
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
