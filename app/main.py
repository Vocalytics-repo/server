# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from event import router  # APIRouter를 불러옴
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="Vocalytics API Server",
    description="음성 인식, 텍스트 음성 변환, 문법 교정, YouTube 검색 서비스를 제공하는 API 서버",
    version="1.0.0"
)

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