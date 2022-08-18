
from data.config import *
from data.token import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.camera import *
from utils.sun import *
from utils.weather import *


def sun(update, context):
    menu_main = [[InlineKeyboardButton('Вспышки на солнце', callback_data='b1_sun')],
                 [InlineKeyboardButton('Магнитные бури', callback_data='b2_m')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Че надо?', reply_markup=reply_markup)


def w(update, context):
    menu_main = [[InlineKeyboardButton('10 дней(Гисметео)', callback_data='b1_gis10')],
                 [InlineKeyboardButton(
                     "10 дней(Яндекс)", callback_data='b2_ya10')],
                 [InlineKeyboardButton('Осадки', callback_data='b3_rain')],
                 [InlineKeyboardButton('Датчик в гетто', callback_data='b4_sensor')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Че надо?', reply_markup=reply_markup)


def cam(update, context):
    menu_main = [[InlineKeyboardButton('Фото с камер', callback_data='b1_cam')],
                 [InlineKeyboardButton("Видео с камер", callback_data='b2_video')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Че надо?', reply_markup=reply_markup)


def menu_actions(update, context):
    query = update.callback_query
    if query.data == 'b1_sun':
        get_sun(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b2_m':
        get_m(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b1_gis10':
        get_gis10(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b2_ya10':
        get_ya10(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b3_rain':
        get_rain(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b4_sensor':
        get_sensor(update, context)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 'b1_cam':
        menu_1 = [[InlineKeyboardButton('Кремль', callback_data='s1_cam')],
                  [InlineKeyboardButton('Почтовая', callback_data='s2_cam')]]
        reply_markup = InlineKeyboardMarkup(menu_1)
        print(InlineKeyboardButton)
        updater.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text='Че надо?',
                                      reply_markup=reply_markup)
    elif query.data == 'b2_video':
        menu_2 = [[InlineKeyboardButton('Кремль', callback_data='s1_video')],
                  [InlineKeyboardButton('Почтовая', callback_data='s2_video')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        updater.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text='Че надо?',
                                      reply_markup=reply_markup)
    elif query.data == 's1_cam':
        get_photo(update, context, kreml_id)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 's2_cam':
        get_photo(update, context, post_id)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 's1_video':
        get_video(update, context, kreml_id)
        update.callback_query.edit_message_reply_markup(None)
    elif query.data == 's2_video':
        get_video(update, context, post_id)
        update.callback_query.edit_message_reply_markup(None)
