from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import websockets
import subprocess
import json
import asyncio

app = FastAPI()
room = 660141628661
danmu = []

subprocess.Popen(
    [
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--proxy-server=127.0.0.1:8827",
        f"https://live.douyin.com/{room}",
    ]
)


async def go_listen():
    global danmu
    async with websockets.connect("ws://127.0.0.1:8888/", ping_interval=None) as ws:
        await ws.send("token")
        close = True
        while close is True:
            result = await ws.recv()
            message = json.loads(result)
            if message["Type"] == 1:
                try:
                    data = json.loads(message["Data"])
                    nick = data["User"]["Id"]
                    content = data["Content"]
                    uid = data["User"]["Nickname"]
                except:
                    pass
                info = {"user": uid, "uid": nick, "content": content}
                danmu.append(info)
                print(info)
        await ws.close()


asyncio.create_task(go_listen())


@app.get("/api/danmu")
async def move():
    global danmu
    res = danmu[::]
    danmu = []
    return res


@app.get("/")
def index():
    return FileResponse("views/dist/index.html")


static_app = FastAPI()
static_app.mount("/", StaticFiles(directory="views/dist"), name="index")

app.mount("/", static_app, name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
