import logging
import os
import random
import sys

from telegram.chataction import ChatAction
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler)

from data.config import *
from data.token import *
from utils import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
updater.bot.send_message(164811956, text='Стартуем')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Че надо?")


def echo(update, context):
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    f = open('data/1.txt', 'r', encoding='UTF-8')
    words = f.read().split('\n')
    f.close()
    my_file = open("data/1.txt", "a")
    if update.message.text not in words:
        my_file.writelines(update.message.text+'\n')
        logging.critical(update.message.text+' добавлено в словарь: ' +
                         str(update.message.from_user.username))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=random.choice(words))
    my_file.close()


dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('sun', sun))
dispatcher.add_handler(CommandHandler('id', get_phone))
dispatcher.add_handler(CommandHandler('cam', cam))
dispatcher.add_handler(CommandHandler('w', w))
dispatcher.add_handler(CommandHandler('traffic', get_traffic))
dispatcher.add_handler(CallbackQueryHandler(menu_actions))
dispatcher.add_handler(CallbackQueryHandler(cam))
updater.start_polling()
updater.idle()
