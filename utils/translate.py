from google_trans_new import google_translator

translator = google_translator()

def dec(text, lang):
    try:
        res = translator.translate(text, lang_src='auto', lang_tgt=lang)
        return res
    except Exception:
        return False
    
def translate(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(parse_mode='HTML', chat_id=chat_id, text='Попробую разложить')
    try:
        to_send = update.message.reply_to_message.text
        print(to_send)
    except AttributeError:
        to_send = ' '.join(context.args)

    if len(to_send) == 0:
        context.bot.send_message(parse_mode='HTML', chat_id=chat_id,
        text='Ниче не задано для раскладки. Пример /dec пропал')

    else:
        i = 0
        result = dec(to_send, 'zh-cn')
        print(result)
        if result:
            lst = []
            while True:
                result = dec(result, 'zh-cn')
                result = dec(result, 'ru')

                if result not in lst:
                    lst.append(result)

                else:
                    context.bot.send_message(parse_mode='HTML', chat_id=chat_id, text=result)
                    context.bot.send_message(parse_mode='HTML', chat_id=chat_id,
                                             text='Расклалось за {} раз'.format(i))
                    break
                if i == 10:
                    context.bot.send_message(parse_mode='HTML', chat_id=chat_id,
                                             text='Разложить не удалось')
                    context.bot.send_message(parse_mode='HTML', chat_id=chat_id, text=result)
                    break

                i += 1
        else:
            context.bot.send_message(parse_mode='HTML', chat_id=chat_id, text='Раскладка отпотела')
