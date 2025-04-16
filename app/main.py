# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import socketio
from event import register_sockets

sio = socketio.AsyncServer(async_mode='asgi')
fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_sockets(sio)

app = socketio.ASGIApp(sio, fastapi_app)