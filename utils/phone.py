import csv
import os
import re

from data.config import *
from data.token import *


def get_phone(update, context):
    msg = ''.join(context.args)
    print(msg)
    search = re.search(r"(7[0-9]{10})", msg)
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
