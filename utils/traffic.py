import tempfile
import time

from data.config import *
from data.token import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram.chataction import ChatAction


def get_traffic(update, context):
    trafpng = tempfile.NamedTemporaryFile(suffix='.png')
    driver=driver_init()
    driver.set_window_size(1600, 900)
    driver.get(traffic_url)
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ymaps3x0--map")))
    except TimeoutException as ex:
        driver.close()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Яндекс пропал"+str(ex.msg))
    try:
        traffic_base = driver.find_element(
            By.CLASS_NAME, "traffic-panel-view__dropdown-title").text
    except NoSuchElementException:
        traffic_base = ""
    time.sleep(2)
    element.screenshot(trafpng.name)
    file_traf = open(trafpng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, file_traf,
                           caption=traffic_base)
    file_traf.close()
    driver.close()
