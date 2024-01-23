import telebot
from telebot import types
from data_manager import TOKEN
from openai import OpenAI

client = OpenAI(api_key='')

bot = telebot.TeleBot(TOKEN)
gpt_chat_enabled = False


@bot.message_handler(commands=['start'])
def welcome(message):
    hi = open('image/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, hi)
    bot.send_message(message.chat.id, 'Привет, я ChatGPT s telegram.', reply_markup=start_menu(), )


# Функция для включения режима GPT чата
@bot.message_handler(commands=['gpt_chat'])
def enable_gpt_chat(message):
    global gpt_chat_enabled
    # Отправка приветственного сообщения
    bot.send_message(message.chat.id, "Режим GPT чата включен.")
    gpt_chat_enabled = True


# Функция для отключения режима GPT чата
@bot.message_handler(commands=['back', 'stop'])
def disable_gpt_chat(message):
    global gpt_chat_enabled
    # Отправка сообщения об отключении режима GPT чата
    bot.send_message(message.chat.id, "Режим GPT чата отключен.")
    gpt_chat_enabled = False


# Функция для обработки входящих сообщений
@bot.message_handler(func=lambda message: True)
def gpt(message):
    global gpt_chat_enabled

    if gpt_chat_enabled:
        # получаем вопрос от пользователя
        prompt = message.text
        msg = bot.send_message(message.chat.id, 'Сообщение принято. Ждем ответа..')
        # prompt = str(input())  водим ответ в консоле
        # gpt-4, gpt-4 turbo попробовать новую модель позже
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Ты русский, научный помощник"},
                {"role": "user", "content": prompt}
            ]
        )
        # gpt_text=str(response)
        gpt_text2 = response.choices[0].message.content
        tokens = response.usage.total_tokens
        # удаление сообщение
        # bot.edit_message_text("...", chat_id=message.chat.id, message_id=msg.message_id)
        bot.delete_message(message.chat.id, msg.message_id)
        #  ответ пишет пользователю
        bot.send_message(message.chat.id, gpt_text2)
        bot.send_message(message.chat.id, f"потрачено следующее количество токенов: {tokens}")
        # ответ в консоле
        print('\nвопрос:', prompt)
        print('\nответ:', gpt_text2)
        print('потрачено токенов:', tokens)
    else:
        bot.reply_to(message, "режим gpt отключен" )


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_chat_gpt = types.KeyboardButton("/gpt_chat")
    item2 = types.KeyboardButton("/start")
    item3 = types.KeyboardButton("расскажи анекдот про программиста")
    item4 = types.KeyboardButton("🎭 текущая роль")
    item5 = types.KeyboardButton("/stop")
    item6 = types.KeyboardButton("🎭 задать роль")
    markup.add(item_chat_gpt, item2, item3, item4, item5, item6)
    return markup


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)
