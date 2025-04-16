# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import socketio
from event import register_sockets
from fastapi.responses import HTMLResponse

sio = socketio.AsyncServer(async_mode='asgi')
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
    return """
    <html>
      <head>
        <title>Vocalytics STT Server</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            color: #333;
            text-align: center;
            padding-top: 100px;
          }
          h1 {
            font-size: 2.5em;
            color: #4CAF50;
          }
          p {
            font-size: 1.2em;
          }
        </style>
      </head>
      <body>
        <h1>Welcome to Vocalytics's Server</h1>
        <p>STT Web Service Coming Soon</p>
        <p>Powered by Nginx + Ubuntu</p>
      </body>
    </html>
    """

register_sockets(sio)

app = socketio.ASGIApp(sio, fastapi_app)