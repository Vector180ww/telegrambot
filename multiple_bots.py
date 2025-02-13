import telebot
import re
import threading
from telebot import types

# Словарь для хранения админов и их ботов
BOT_ADMINS = {
    "8066552328:AAFPl1Oy4uA9wG8tmSvFVROAZldY2Is0FEk": 7684236341,  # Первый администратор
    "7814892891:AAGWCQTlXp5lC9SSFMROXV9g2DbNObpEvP0": 1784949039,  # Второй администратор
    "7837681656:AAHipoSl6eANbnHkYI1ZnVz9UdR4tIHCMAw": 7451841835,  # Третий администратор
    "7458106241:AAEXEReIeEKciV0kgkOuECWZywJIqo06ZMo": 7026509584,  # Четвертый администратор
    "7555233576:AAH4tPQ7GWHjjsFEwq0iSU16eAuxfB8CxYU": 7944399671,  # Пятый администратор
    "7914302663:AAF47zNceJTUZud-l4Izy6SMCtxOgRgAs1M": 2009068571,  # Шестой администратор
    "7400427034:AAFMhMj43Iw9PUVCdbOwEF0RH70MuoAmt_E": 6954599692,  # Седьмой администратор
    "8059443691:AAGWk3ds5bqpObAjqBOsudaDW1FazB7POEI": 6336717053,  # Восьмой администратор
    "7860853949:AAHLhBgU3L1NK1TmHULrieRM6A0nXaEMSME": 7016442984,  # Девятый администратор
    "7857018867:AAHntUcX7Tzqois1M4oSBbcmdTO34Cw3Bs4": 1854033101,  # Десятый администратор
    "7655209082:AAE5KlKEpHmQKZr-_VJI7wvtSg52sbOmk0s": 5819287947,  # Одиннадцатый администратор
    "7503578744:AAHWLbw3YqR4pzC0B_VsZl0KDRlA77R2vzQ": 1809889654,  # Двенадцатый администратор
    "7467081366:AAEHoHKivDRmu0JO3djA4fvHY5bsb9ZHDPk": 6727311571,  # Тринадцатый администратор
    "8145650633:AAG8-YKLnflVcUxtEsNbL13AftaxtrRofDM": 5176607333,  # Четырнадцатый администратор
    "7549627036:AAEVAX2BoF51PgeXbIgn_8oYPvnvyd-K9pg": 7083298669,  # Пятнадцатый администратор
    "8159602287:AAFIgKsVdQXwBTSmj3ymVbErfoQxhMphsQ4": 1685649919,  # Шестнадцатый администратор
    "7605010274:AAEZJ9fMDCqwH6CQ-YEZDgcDofDykd35MME": 5698202204,  # Семнадцатый администратор
    "7992158778:AAEezCKxgejZGkK2ACtP-wW2yycCbTxWTHM": 5683006219,  # Восемнадцатый администратор
    "8063764825:AAHVFwXyW2QV4s8kZFak_jh28R1CteVPPks": 5675386055,  # Девятнадцатый администратор
    "7551944644:AAFYXQW8atw-Yh89ZJ3xMBgMM_5uiO5ZcMg": 5961836680,  # Двадцатый администратор
    "8156011723:AAGByL3zmfJ-s70dlqzdV5EXfyDXSnLYeyY": 6104889278,  # Двадцать первый администратор
    "7975800660:AAGax9QQM7LTRzAYgDmREeQdtTd6a7M-1v4": 6133694613, # Двадцать второй администратор           
    "7567039380:AAE5DqaBDwb0AGReWRnOIbx-y_3Xh6rbNOw": 6466793262, # Двадцать третий администратор
    "7798226843:AAEx6Dy3K5xfBIYIdLhL0j-aAqZfRompJ70": 5973408575, # Двадцать четвертый администратор
    "7681320762:AAH2c1ae6cSMh86cKXfRfVGXW3AynOFdgps": 6110760577, # Двадцать пятый администратор
    "7924683602:AAFFmVUaqZONbpGafdDlysjz5JtUB8-gZcE": 6016580029, # Двадцать шестой администратор
    "7661631895:AAH_KJSX2DUdBo2L_1C-lcsGEiobTkiDnQw": 6433264848, # Двадцать седьмой администратор
    "7981404819:AAHlmtyoHHYH9aOJ2RbTqeq5pTWQe7U5b9U": 6541862294, # Двадцать восьмой администратор
    "7908519689:AAF_iz23hoPdg0x4RKX_mBezGT--LdGUjD0": 6314894743, # Двадцать девятый администратор
    "7619344997:AAFgocOSXWaHfqtVXmtLlbss9Bjl-ziU1kg": 6782047516, # Тридцатый администратор
    "7756617497:AAErPNV2nG4I8KOgVji7or8u5VVTn97r0T8": 6713356022, # Тридцать первый администратор
     "7593566290:AAGOlal76QTNez5HukWeqebMGTl0Y0qWAA8": 6536643213, # Тридцать третий администратор
    "8025893259:AAHunn9In8dk8kjUiQw_9nRo3phEVPbxNsQ": 5864426452, # Тридцать четвертый администратор
    "7639419535:AAEAVdQEhrGDDfEqq-WmXpYZ_ADrKn4e88E": 6778588621, # Тридцать пятый администратор
    "7716142231:AAEtkiM1uP50bDSX3AsTMGVbw5N8r_3kaq0": 6959767681, # Тридцать шестой администратор
    "7929059534:AAGjfUb2uxGGvHdKjXCTmU97nHcObXrk--Y": 6127305691, # Тридцать седьмой администратор
    "7654749735:AAF0hmhmiIiU8p2wwVAkU5kFkHx6-n6c7p8": 6007977586, # Тридцать восьмой администратор
    "7634505767:AAFD0HRZIvbA5UNP3CwCIrDftunlT40SuJM": 6406588546, # Тридцать девятый администратор
    "8118325456:AAEW-xBMU6HyQF8sw8EXbivNC10ofDMYs6c": 7373263247, # Сороковой администратор
    "7261310004:AAFDs_NYa1kjP2M8VK_zLTKvArNSo-WfY-w": 7302794051, # Сорок первый администратор
    "7993909365:AAFZflAZuxeTvtHt26xpqsGE2uK9FEVuHW0": 6232795423, # Сорок второй администратор
    "7862952626:AAHySC2PY4BqyiDdD3HRs1mDrge1i76eeh0": 6116638479, # Сорок третий администратор
    "7623048911:AAEroqIoNfY4kv0IQabGhZCNzFNMWkT0U4M": 6532777173, # Сорок четвертый администратор
    "7759929311:AAH7bQdaKepTRd2oWiuW-w2YSUygeZUMNxQ": 5970383838, # Сорок пятый администратор
    "7899111219:AAGJZUstusgkjTymBHioYVhvYE-E7W1SXXg": 7122943745, # Сорок шестой администратор
    "7176347169:AAGKp_ZzfzhnjGQ_XxpzkSHJBUZKxt62SS0": 6172073548, # Сорок восьмой администратор
    "7561050958:AAEOhQwhTxIA0FZnTx0FQXGSDByO9FJx4AU": 5876005113, # Сорок девятый администратор
    "7839795193:AAFk9Kl4EORZs6s-bpcGWhF1lpsmbUrl39M": 7543899484, # Пятидесятый администратор
    "7678047083:AAEFes6NLWrOTT4dVHBMCtSs1NK1mR7q7Lw": 1932100312, # Пятдесят первый администратор 
    "7472784249:AAHUR-8aySo79P6N7mRpkc9osVa560Up-CY": 7297737173, # Пятдесят второй администратор
    "7261310004:AAFDs_NYa1kjP2M8VK_zLTKvArNSo-WfY-w": 7302794051, # Пятдесят третий администратор
    "7960810331:AAFohbHSKqnbDGeZliVL0WjPmFhFpZ4XAoI": 6444351488, # Пятдесят четвертый администратор
    "7839795193:AAFk9Kl4EORZs6s-bpcGWhF1lpsmbUrl39M": 7543899484, # Пятдесят пятый администратор
    "8181156961:AAH_TZ9WjW_dNj-F6aWwr8boDcjxuIddvbY": 7720075768  # Пятдесят шестой администратор
}# Список токенов для ботов
BOT_TOKENS = list(BOT_ADMINS.keys())

# Словарь для хранения пользователей и соответствующих ботов
user_to_bot = {}

# Словарь для хранения номеров телефонов
user_contacts = {}

# Список для хранения объектов ботов
bots = []

# Функция для извлечения chat_id из текста
def extract_chat_id(text):
    match = re.search(r'\((\d+)\)', text)
    if match:
        return int(match.group(1))
    return None

# Функция для отправки медиаконтента
def send_media(bot, chat_id, media_type, media_file, caption=None):
    try:
        if media_type == 'photo':
            bot.send_photo(chat_id, media_file, caption=caption)
        elif media_type == 'video':
            bot.send_video(chat_id, media_file, caption=caption)
        elif media_type == 'audio':
            bot.send_audio(chat_id, media_file, caption=caption)
        elif media_type == 'document':
            bot.send_document(chat_id, media_file, caption=caption)
        elif media_type == 'voice':
            bot.send_voice(chat_id, media_file)
        else:
            print("Unknown Media Type.")
    except Exception as e:
        print(f"Error when sending media: {e}")

# Создаем объекты ботов
for token in BOT_TOKENS:
    bot = telebot.TeleBot(token)
    bots.append(bot)

# Функция для запуска бота
def bot_worker(bot, admin_id):
    # Обработчик команды /start
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        # Создаем кнопку для запроса номера телефона
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton("📞 Send phone number", request_contact=True)
        markup.add(button)
        bot.send_message(
            message.chat.id,
            "Hello. Write me what you want and the receptionist will make your evening unforgettable.\n"
            "Don't forget to include your phone number so we can contact you.",
            reply_markup=markup
        )

    # Обработчик номера телефона
    @bot.message_handler(content_types=['contact'])
    def handle_contact(message):
        if message.contact is not None:
            user_contacts[message.chat.id] = message.contact.phone_number
            bot.send_message(
                message.chat.id,
                f"Thank you! We got your phone number: {message.contact.phone_number}.\n"
                "You can now send a message and an administrator will get back to you.",
                reply_markup=types.ReplyKeyboardRemove()
            )

    # Обработчик сообщений от пользователей (включая медиа)
    @bot.message_handler(content_types=['photo', 'video', 'document', 'text'])
    def handle_user_message(message):
        global user_to_bot

        if message.chat.id != admin_id:
            # Сохраняем соответствие пользователя и бота
            user_to_bot[message.chat.id] = bot

            # Логируем информацию
            sanitized_text = message.text if message.text else "Media message"
            print(f"Message from {message.chat.first_name} ({message.chat.id}): {sanitized_text}")  # Логируем сообщение

            # Формируем сообщение для администратора
            forward_text = f"🔔 Сообщение от {message.chat.first_name} ({message.chat.id})\n"

            # Добавляем номер телефона, если он есть
            if message.chat.id in user_contacts:
                forward_text += f"📞 Phone: {user_contacts[message.chat.id]}\n"

            # Добавляем текст сообщения
            forward_text += f"\n{sanitized_text}\n\n🔗 Бот: @{bot.get_me().username}"

            try:
                print(f"Sending a message to the administrator {admin_id}")  # Логируем попытку отправки
                bot.send_message(admin_id, forward_text)
            except Exception as e:
                print(f"Error when sending a message to the administrator: {e}")
                bot.send_message(
                    message.chat.id,
                    "❌ Failed to send a message to the administrator. Please try again later."
                )

            # Отправка медиа (если оно есть)
            try:
                if message.photo:
                    print(f"Received photo: {message.photo[-1].file_id}")
                    send_media(bot, admin_id, 'photo', message.photo[-1].file_id)
                elif message.video:
                    print(f"Received video: {message.video.file_id}")
                    send_media(bot, admin_id, 'video', message.video.file_id)
                elif message.document:
                    print(f"Received document: {message.document.file_id}")
                    send_media(bot, admin_id, 'document', message.document.file_id)
            except Exception as e:
                print(f"Error while forwarding media: {e}")
                bot.send_message(message.chat.id, "❌ Ошибка при отправке файла.")

        else:
            # Если сообщение от администратора, пытаемся ответить пользователю
            try:
                print(f"Message from admin {admin_id}")  # Логируем сообщение от администратора
                if message.reply_to_message:
                    # Проверяем, что сообщение администратора действительно ответ на сообщение пользователя
                    if message.reply_to_message.text:
                        # Парсим chat_id пользователя из текста
                        reply_to_chat_id = extract_chat_id(message.reply_to_message.text)

                        if reply_to_chat_id is not None:
                            print(f"Reply to user with chat_id {reply_to_chat_id}")  # Логируем chat_id
                            if message.text:  # Если это текстовое сообщение
                                bot.send_message(reply_to_chat_id, message.text)  # Отправляем текст
                            elif message.photo:  # Если это фото
                                send_media(bot, reply_to_chat_id, 'photo', message.photo[-1].file_id)
                            elif message.video:  # Если это видео
                                send_media(bot, reply_to_chat_id, 'video', message.video.file_id)
                            elif message.document:  # Если это документ
                                send_media(bot, reply_to_chat_id, 'document', message.document.file_id)
                        else:
                            bot.send_message(admin_id, "❌ Unable to retrieve chat_id to send.")
                    else:
                        bot.send_message(admin_id, "❌ Reply not to a message with a chat_id.")
                else:
                    bot.send_message(admin_id, "❌ No reply to user's message.")
            except Exception as e:
                print(f"Error while processing a message from the administrator: {e}")
                bot.send_message(admin_id, f"❌ Error: {str(e)}")

    bot.polling(none_stop=True)

# Запускаем всех ботов в отдельных потоках
print("Bots are up and running. Waiting for messages...")
threads = []
for bot in bots:
    admin_id = BOT_ADMINS[bot.token]
    thread = threading.Thread(target=bot_worker, args=(bot, admin_id))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()