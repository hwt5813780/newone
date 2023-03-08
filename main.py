import uvicorn
from fastapi import FastAPI
 
app = FastAPI()
 
@app.get("/case/{cid}")
def read_case(cid):
    return {"id": cid}

# 启动创建的实例app，设置启动ip和端口号
uvicorn.run(app, host="0.0.0.0", port=8000)