import telebot
import config
import random
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
 
@bot.message_handler(commands=['start'])
def welcome(message):
 sti = open('фото/Hi.webp', 'rb')
 bot.send_sticker(message.chat.id , sti)

 #keyboard_клава_тоесть
 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
 item1 = types.KeyboardButton("🎲 Рандомное число")
 item2 = types.KeyboardButton("😊 Как дела?")
 item3 = types.KeyboardButton("Расскажи о себе?")
 markup.add(item1, item2, item3)


 bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
 parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id , str(random.randint(0,100)))
        elif message.text == '😊 Как дела?':
            bot.send_message(message.chat.id, 'отлично, сам как?')
        elif message.text == 'Расскажи о себе?':
            bot.send_message(message.chat.id, 'я бот созданый криворуким програмистом')
        else:
            bot.send_message(message.chat.id, 'я не понимаю тебя')
        

@bot.message_handler(content_types=['text'])
def foto(message):
    if message.chat.type == 'private':
        if message.text == 'Скинь фото':
            bot.send_sticker(message.chat.id , sti)
            

    
# RUN
bot.polling(none_stop=True)
