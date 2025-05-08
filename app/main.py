# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import socketio
from event import register_sockets
from fastapi.responses import HTMLResponse

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)
fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/", response_class=HTMLResponse)
def root():
    return "Server is running."

register_sockets(sio)

app = socketio.ASGIApp(sio, fastapi_app)