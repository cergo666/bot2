import tempfile
import urllib.request

from data.config import *
from data.token import *
from PIL import Image
from telegram.chataction import ChatAction


def get_sun(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    imjpg = tempfile.NamedTemporaryFile(suffix='.jpg')
    urllib.request.urlretrieve(
        "https://tesis.xras.ru/upload_test/files/flares_R4LB.png", impng.name)
    im = Image.open(impng.name)
    fill_color = (0, 0, 0)
    im = im.convert("RGBA")
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background
    im.convert("RGB").save(imjpg.name)
    file1 = open(imjpg.name, 'rb')
    updater.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    updater.bot.send_photo(update.effective_chat.id, file1,
                           caption='Вспышки на солнце за 2 дня')
    file1.close()


def get_m(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    imjpg = tempfile.NamedTemporaryFile(suffix='.jpg')
    urllib.request.urlretrieve(
        "https://tesis.xras.ru/upload_test/files/kp_R4LB.png", impng.name)
    im = Image.open(impng.name)
    fill_color = (0, 0, 0)
    im = im.convert("RGBA")
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background
    im.convert("RGB").save(imjpg.name)
    file = open(imjpg.name, 'rb')
    updater.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    updater.bot.send_photo(update.effective_chat.id, file,
                           caption='Магнитные бури за 3 дня')
    file.close()
