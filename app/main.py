# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from event import router  # APIRouter를 불러옴

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Vocalytics STT Server is running."}