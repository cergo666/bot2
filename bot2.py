import csv
import json
import logging
import os
import random
import re
import time
import urllib.request

from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.chataction import ChatAction
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler)

from data.config import *
from data.token import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater.bot.send_message(164811956, text='Стартуем')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Че надо?")


def echo(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    f = open('data/1.txt', 'r', encoding='UTF-8')
    words = f.read().split('\n')
    f.close()
# Запись фразы в словарь
    my_file = open("data/1.txt", "a")
# Проверка, что слова нет в словаре
    if update.message.text not in words:
        my_file.writelines(update.message.text+'\n')
        logging.critical(update.message.text+' добавлено в словарь: ' +
                         str(update.message.from_user.username))
# Рандомный ответ от бота из файла
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=random.choice(words))
    my_file.close()


def m(update, context):
    urllib.request.urlretrieve(
        "https://tesis.xras.ru/upload_test/files/kp_R4LB.png", "tmp/m.png")
    im = Image.open('tmp/m.png')
    fill_color = (0, 0, 0)
    im = im.convert("RGBA")
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background
    im.convert("RGB").save('tmp/m.jpg')
    file = open('tmp/m.jpg', 'rb')
    updater.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    updater.bot.send_photo(update.effective_chat.id, file,
                           caption='Магнитные бури за 3 дня')
    file.close()
    os.remove('tmp/m.jpg')
    os.remove('tmp/m.png')


def sun(update, context):
    urllib.request.urlretrieve(
        "https://tesis.xras.ru/upload_test/files/flares_R4LB.png", "tmp/sun.png")
    im = Image.open('tmp/sun.png')
    fill_color = (0, 0, 0)
    im = im.convert("RGBA")
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background
    im.convert("RGB").save('tmp/sun.jpg')
    file1 = open('tmp/sun.jpg', 'rb')
    updater.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    updater.bot.send_photo(update.effective_chat.id, file1,
                           caption='Вспышки на солнце за 2 дня')
    file1.close()
    os.remove('tmp/sun.jpg')
    os.remove('tmp/sun.png')


def id(update, context):
    msg = ''.join(context.args)
    print(msg)
    search = re.search(r"(7[0-9]{10})", msg)
    print(search)
    if search:
        phone = search.group()
        count = 0
        fileid = ('tmp/dbpn/'+phone[0:2]+'/'+phone[2:4] +
                  '/'+phone[4:6]+'/'+phone[6:8]+'.csv')
        if os.path.isfile(fileid) and os.access(fileid, os.R_OK):
            print(fileid)
            csvfile = open(fileid, 'r')
            reader = csv.DictReader(csvfile, delimiter=',')
            if reader:
                for row in reader:
                    if row['phone_number'] == phone:
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Телефон:'+str(row['phone_number'])+'\nСдэк:'+str(row['cdek_full_name'])+'\nЗаказы Яндекс:'+str(
                            row['yandex_place_name'])+'\nАдрес: г.'+str(row['yandex_address_city'])+',ул. '+str(row['yandex_address_street'])+' ,д. '+str(row['yandex_address_house'])+' ,кв. '+str(row['yandex_address_entrance']))
                        count += 1

                if count == 0:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text='Не нашел такого в базе')
                    return
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Не нашел такого вообще')
        csvfile.close()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Иди нахуй, это не телефон.\nВведи в формате 7хххххххххх')


def v(update, context):
    cmd = 'ffmpeg -user_agent %s -headers "origin: %s" -headers "referer: %s" -i "https://cctv.on-telecom.ru:4080/hls/%s/playlist.m3u8" -ss 00:00:01 -vframes 1 -q:v 1 tmp/v.png' % (
        user_agent, url, url, kreml_id)
    os.system(cmd)
    file = open('tmp/v.png', 'rb')
    context.bot.send_photo(update.effective_chat.id, file,
                           caption='Кремль')
    file.close()
    os.remove('tmp/v.png')


def w(update, context):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(gismeteo10_url)
    element = driver.find_element(By.CLASS_NAME, "widget-weather")
    element.screenshot('tmp/w.png')
    fileww = open('tmp/w.png', 'rb')
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileww,
                           caption='Погода на 10 дней')
    fileww.close()
    os.remove('tmp/w.png')


def rain(update, context):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1600, 900)
    driver.get(rain_url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    mydivs = soup.find(
        "div", {"class": "weather-maps-fact__nowcast-alert"}).text
    print(mydivs)
    element = driver.find_element(By.CLASS_NAME, "weather-maps__map")
    time.sleep(1)
    element.screenshot('tmp/wy.png')
    fileya = open('tmp/wy.png', 'rb')
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileya,
                           caption=mydivs)
    fileya.close()
    os.remove('tmp/wy.png')


def yaw(update, context):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(pogoda_url)
    element = driver.find_element(By.CLASS_NAME, "forecast-briefly")
    time.sleep(1)
    element.screenshot('tmp/yaw.png')
    fileya = open('tmp/yaw.png', 'rb')
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileya,
                           caption='Погода')
    fileya.close()
    os.remove('tmp/yaw.png')


def getto(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    with urllib.request.urlopen('%s' % (narodmon_url)) as url:
        data = json.loads(url.read().decode())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Влажность ' + str(data['sensors'][0]['value'])+'\n'+'Давление ' + str(
                                 data['sensors'][1]['value'])+'\n'+'Температура ' + str(data['sensors'][3]['value'])+'⚡')


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
start_handler = CommandHandler('start', start)
m_handler = CommandHandler('m', m)
sun_handler = CommandHandler('sun', sun)
id_handler = CommandHandler('id', id)
v_handler = CommandHandler('v', v)
w_handler = CommandHandler('w', w)
rain_handler = CommandHandler('rain', rain)
yaw_handler = CommandHandler('yaw', yaw)
getto_handler = CommandHandler('getto', getto)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(m_handler)
dispatcher.add_handler(sun_handler)
dispatcher.add_handler(id_handler)
dispatcher.add_handler(v_handler)
dispatcher.add_handler(w_handler)
dispatcher.add_handler(rain_handler)
dispatcher.add_handler(yaw_handler)
dispatcher.add_handler(getto_handler)
updater.start_polling()
updater.idle()
