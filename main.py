import openai
import requests
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

openai.api_key = "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" # 将 YOUR_API_KEY 替换为您的实际 API 密钥

# 设置API请求的URL和参数
url = "https://api.openai.com/v1/chat/completions"


headers={"authority": "api.openai.com",
         "Content-Type": "application/json",
         "Authorization": f"Bearer {openai.api_key}"
}

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

# 定义请求体数据类型：text
class Document(BaseModel):
    prompt: str



def chat(prompt):  #定义一个函数

    try:
        data = {"model": "gpt-3.5-turbo",
                "temperature": 0,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
        }
        # 发送HTTP请求
        response = requests.post(url, headers=headers,json=data)

        # 解析响应并输出结果
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip()
            answer = json.loads(answer)
        else:
            raise Exception(f"Request failed with status code {response.status_code}")        
        return answer
    
    except Exception as exc:
        #print(exc)  #需要打印出故障
        return "broken"

# 设置API请求的URL和参数
@app.post("/v1/textCorrect/", status_code=200)
async def handle_request(document: Document):
    # 创建一个事件循环
    loop = asyncio.get_running_loop()
    print('创建事件循环成功')
    # 创建一个协程，用于处理当前请求
    coroutine = chat(document.prompt)
    print('创建协程成功')
    # 并行处理当前请求
    result = await asyncio.gather(coroutine, return_exceptions=True)
    print('并行处理当前请求成功')
    print(result)
    return result[0]

# 启动创建的实例app，设置启动ip和端口号
uvicorn.run(app, host="127.0.0.1", port=8000)