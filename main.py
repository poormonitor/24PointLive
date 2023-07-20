import asyncio

from bilibili_api import live
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
room = 4362740
danmu = []

room = live.LiveDanmaku(room)


@room.on("DANMU_MSG")
async def on_danmaku(event):
    global danmu
    data = event["data"]["info"]
    info = {"user": data[2][1], "uid": data[2][0], "content": data[1]}
    danmu.append(info)
    print(info)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(room.connect())


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
