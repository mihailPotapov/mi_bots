import telebot
from telebot import types
from data_manager import TOKEN
from openai import OpenAI
# TOKEN = "5676606819:AAFmECqYhffaGAaJOD4SThzOcICSQNNEF0I"
client = OpenAI(api_key="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")
prompt = str(input())
completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)
print('Вопрос:', prompt)
print('\nОтвет:')
print(completion.choices[0].message)