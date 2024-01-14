import openai
openai.api_key = ""
engine="text-davinci-003"
# Запрос
prompt = "Назови лучшую Python библиотеку по машинному обучению"

# Модель
completion = openai.Completion.create(engine=engine,
                                      prompt=prompt,
                                      temperature=0.5,
                                      max_tokens=1000)

print(completion)