import tempfile
import time

from data.config import *
from data.token import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram.chataction import ChatAction


def get_fires(update, context):
    firepng = tempfile.NamedTemporaryFile(suffix='.png')
    driver=driver_init()
    driver.get(fires_url)
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ymaps-2-1-79-inner-panes")))
        button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'ymaps-2-1-79-zoom__button ')))
        button.click()
        button.click()
    except TimeoutException as ex:
        driver.close()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Пожары пропали"+str(ex.msg))
    time.sleep(1)
    element.screenshot(firepng.name)
    file_fire = open(firepng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, file_fire,
                           caption='Пожары')
    file_fire.close()
    driver.close()
