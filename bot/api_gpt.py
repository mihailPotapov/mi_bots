import telebot
from telebot import types
from pathlib import Path
from data_manager import TOKEN
from openai import OpenAI


bot = telebot.TeleBot(TOKEN)

BACK_BUTTON = "◀ назад"
WELCOME_MESSAGE = (
    "Добро пожаловать, {0.first_name}!\n"
    "Я - <b>{1.first_name}</b>, бот созданный для проверки разный функций."
)


@bot.message_handler(commands=['start'])
def welcome(message):
    hi = open('image/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, hi)
    bot.send_message(message.chat.id, 'Привет, я ChatGPT s telegram.', reply_markup=start_menu(),)


@bot.message_handler(content_types=['text'])
def gpt(message):
    # получаем вопрос от пользователя
    prompt = message.text
    msg=bot.send_message(message.chat.id, 'Сообщение принято. Ждем ответа..')
    client = OpenAI(api_key='')
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
    gpt_text2=response.choices[0].message.content
    tokens=response.usage.total_tokens
    # удаление сообщение
    # bot.edit_message_text("...", chat_id=message.chat.id, message_id=msg.message_id)
    bot.delete_message(message.chat.id, msg.message_id)
    #  ответ пишет пользователю
    bot.send_message(message.chat.id, gpt_text2)
    bot.send_message(message.chat.id, f"потрачено следующее количество токенов: {tokens}")
#     bot.delete_message(message.chat.id, message.message_id - 1)
# ответ в консоле
    print('\nвопрос:', prompt)
    print('\nответ:', gpt_text2)
    print('потрачено токенов:', tokens)


# @bot.message_handler(content_types=['text'])
# def chatting(message):
#     if message.text == 'Сообщение принято. Ждем ответа..':
#         bot.delete_message(message.chat.id, message.message_id)


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃 gpt_chat")
    item2 = types.KeyboardButton("/start")
    item3 = types.KeyboardButton("расскажи анекдот про программиста")
    item4 = types.KeyboardButton("🎭 текущая роль")
    item5 = types.KeyboardButton("🎭 задать роль")
    markup.add(item1, item2, item3,item4,item5)
    return markup


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)