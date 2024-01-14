# "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"
# from openai import OpenAI
# client = OpenAI(
#     api_key="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",
# )
#
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
#
# print(chat_completion.choices[0].message)
import openai
openai.api_key ="ak-cedd8139570246509b46ed003996a42a"
engine="text-davinci-003"

# Модель
# пишешь запрос в консоле и в консоле получаешь ответ
prompt = str(input())
completion = openai.Completion.create(engine=engine,
                                      prompt=prompt,
                                      temperature=0.5,
                                      max_tokens=1000)
print('\nОтвет:')
print( completion.choices[0]['text'] )
