import ssl
import tempfile
import urllib.request

from data.config import *
from data.token import *
from PIL import Image
from telegram.chataction import ChatAction

ssl._create_default_https_context = ssl._create_unverified_context

def get_river(update, context):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    # imjpg = tempfile.NamedTemporaryFile(suffix='.jpg')
    urllib.request.urlretrieve(
        "https://ribalovers.ru/hi.php?q=informer/draw/v2_75319_400_300_30_ffffff_011_8_7_H_none.png", impng.name)
    im = Image.open(impng.name)
    # fill_color = (0, 0, 0)
    # im = im.convert("RGBA")
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, fill_color)
    #     background.paste(im, im.split()[-1])  # omit transparency
    #     im = background
    # im.convert("RGB").save(imjpg.name)
    file = open(impng.name, 'rb')
    updater.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    updater.bot.send_photo(update.effective_chat.id, file,
                           caption='Уровень Оки')
    file.close()
