import os
import tempfile

from data.config import *
from telegram.chataction import ChatAction


def get_photo(update, context, cam_id):
    impng = tempfile.NamedTemporaryFile(suffix='.png')
    cmd = '%s -y -user_agent %s -headers "origin: %s" -headers "referer: %s" -i "https://cctv.on-telecom.ru:4080/hls/%s/playlist.m3u8" -ss 00:00:01 -vframes 1 -q:v 1 %s' % (
        ffmpeg, user_agent, url, url, cam_id, impng.name)
    os.system(cmd)
    file = open(impng.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(update.effective_chat.id, file,
                           caption='')
    file.close()


def get_video(update, context, cam_id):
    imp4 = tempfile.NamedTemporaryFile(suffix='.mp4')
    cmd = '%s -y -user_agent %s -headers "origin: %s" -headers "referer: %s" -i "https://cctv.on-telecom.ru:4080/hls/%s/playlist.m3u8" -t 10 -c copy  %s' % (
        ffmpeg, user_agent, url, url, cam_id, imp4.name)
    os.system(cmd)
    file = open(imp4.name, 'rb')
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
    context.bot.send_video(update.effective_chat.id, file,
                           caption='')
    file.close()
