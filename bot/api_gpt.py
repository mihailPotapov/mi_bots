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
    client = OpenAI(api_key='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')
    # prompt = str(input())#  водим ответ в консоле
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Ты русский полезный помощник"},
            {"role": "user", "content": prompt}
        ]
    )

    # print('Вопрос:', prompt)# пишет повторно вопрос
    print('\nОтвет:',prompt)
    gpt_text=str(response)
    gpt_text2=response.choices[0].message.content
    # ответ в консоле
    print(gpt_text2)
    #  ответ пишет пользователю
    bot.send_message(message.chat.id, gpt_text2)


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃 gpt_chat")
    item2 = types.KeyboardButton("🖼 медия")
    markup.add(item1, item2)
    return markup


bot.polling(none_stop=True)