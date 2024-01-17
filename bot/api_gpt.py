import telebot
from telebot import types
from data_manager import TOKEN, OPENAI_API_KEY
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
    client = OpenAI(api_key='')
    # prompt = str(input())#  водим ответ в консоле

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Ты русский, научный помощник"},
            {"role": "user", "content": prompt}
        ]
    )

# print('Вопрос:', prompt)# пишет повторно вопрос
    print('\nОтвет:',prompt)
    # gpt_text=str(response)
    gpt_text2=response.choices[0].message.content
# ответ в консоле
    print(gpt_text2)
    # print(gpt_text)
#  ответ пишет пользователю
    bot.send_message(message.chat.id, gpt_text2)


# @bot.message_handler(content_types=['text'])
# def gpt(message):
#     chat_id = message.chat.id
#     text = message.text.lower()
#     if message.chat.type == 'private':
#         if text == '🎭 задать роль':
#             bot.send_message(chat_id, 'Какую роль желаете? ')
#
#     elif text == '🗃 gpt_chat':
#         bot.send_message(chat_id, 'Я gpt_chat что желаете? ')
#
#     elif text == '🎭 текущая роль':
#         bot.send_message(chat_id, 'Я русский, научный помощник ')
#
#     else:


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃 gpt_chat")
    item2 = types.KeyboardButton("🎭 текущая роль")
    item3 = types.KeyboardButton("🎭 задать роль")
    item4 = types.KeyboardButton("/start")
    markup.add(item1, item2, item3,item4)
    return markup


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)