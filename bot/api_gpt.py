from openai import OpenAI

client = OpenAI(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message)