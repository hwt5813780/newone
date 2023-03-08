import os
import openai

openai.api_key = "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"
print("if you want to stop the conversation, please input 'quit'") #提示想终止聊天时输入"quit"


response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[{"role": "user", "content": "hello"} ]
                )

answer = response.choices[0].message.content.strip()
print(answer)