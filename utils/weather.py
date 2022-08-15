import json
import tempfile
import time
import urllib.request

from data.config import *
from data.token import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram.chataction import ChatAction


def get_gis10(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(binary, options=options)
    driver.get(gismeteo10_url)
    element = driver.find_element(By.CLASS_NAME, "widget-weather")
    element.screenshot(impng.name)
    fileww = open(impng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileww,
                           caption='Погода на 10 дней')
    fileww.close()
    driver.close()


def get_ya10(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(binary, options=options)
    driver.get(pogoda_url)
    element = driver.find_element(By.CLASS_NAME, "forecast-briefly")
    time.sleep(1)
    element.screenshot(impng.name)
    fileya = open(impng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileya,
                           caption='Погода')
    fileya.close()
    driver.close()


def get_rain(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(binary, options=options)
    driver.set_window_size(1600, 900)
    driver.get(rain_url)
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "weather-maps__map")))
    except TimeoutException as ex:
        driver.close()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Яндекс пропал"+str(ex.msg))
    try:
        weather_base = driver.find_element(
            By.CLASS_NAME, "weather-maps-fact__condition").text
    except NoSuchElementException:
        weather_base = ""
    try:
        weather_more = driver.find_element(
            By.CLASS_NAME, "weather-maps-fact__nowcast-alert").text
    except NoSuchElementException:
        weather_more = ""
    time.sleep(2)
    element.screenshot(impng.name)
    fileya = open(impng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, fileya,
                           caption=weather_base+'\n'+weather_more)
    fileya.close()
    driver.close()


def get_sensor(update, context):
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    with urllib.request.urlopen('%s' % (narodmon_url)) as url:
        data = json.loads(url.read().decode())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='🌡️'+'Температура ' + str(data['sensors'][3]['value'])+'\n'+'🗜'+'Давление ' + str(
                                 data['sensors'][1]['value'])+'\n'+'💧'+'Влажность ' + str(data['sensors'][0]['value'])+'\n'+'☢️'+'Радиация ' + str(data['sensors'][2]['value']))
