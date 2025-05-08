from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import socketio

from event import register_sockets
from api.stt_router import router as stt_router  # 📌 STT 라우터 임포트

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

fastapi_app = FastAPI()

# CORS 설정
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 포함
fastapi_app.include_router(stt_router)

@fastapi_app.get("/", response_class=HTMLResponse)
def root():
    return "Server is running."

# 소켓 이벤트 등록
register_sockets(sio)

# FastAPI + SocketIO 합치기
app = socketio.ASGIApp(sio, fastapi_app)