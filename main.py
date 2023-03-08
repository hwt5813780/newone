import openai
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = "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" # 将 YOUR_API_KEY 替换为您的实际 API 密钥

# 创建一个 FastAPI「实例」，名字为app
app = FastAPI()

# 设置允许跨域请求，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def chat(prompt):  #定义一个函数

    try:
        response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[{"role": "user", "content": prompt} ]
                )

        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as exc:
        #print(exc)  #需要打印出故障
        return "broken"

# 设置API请求的URL和参数
@app.post("/api/your-endpoint", status_code=200)
async def handle_request(prompt: str):
    # 创建一个事件循环
    loop = asyncio.get_running_loop()
    print('创建事件循环成功')
    # 创建一个协程，用于处理当前请求
    coroutine = chat(prompt)
    print('创建协程成功')
    # 并行处理当前请求
    result = await asyncio.gather(coroutine, return_exceptions=True)
    print('并行处理当前请求成功')
    print(result)
    return result[0]

# 启动创建的实例app，设置启动ip和端口号
uvicorn.run(app, host="0.0.0.0", port=8000)