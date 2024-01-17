# import telebot
# from telebot import types
# from data_manager import TOKEN
# TOKEN = "5676606819:AAFmECqYhffaGAaJOD4SThzOcICSQNNEF0I"
import telebot
import openai
from data_manager import TOKEN, OPENAI_API_KEY
from openai import OpenAI


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я ChatGPT s telegram.')


@bot.message_handler(content_types=['text'])
def gpt(message):
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
    # print(completion.choices[0].message)# пишет ответ в консоле
    # gpt_text=str(response)
    gpt_text=response.choices[0].message.content
    print(gpt_text)
    bot.send_message(message.chat.id, gpt_text)


bot.polling(none_stop=True)