from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 불러오기
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")

router = APIRouter()

# 데이터 모델 정의
class PromptRequest(BaseModel):
    prompt: str

# 엔드포인트 생성
@router.post("/corr")
def chat_with_gemini(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        # 개선된 사전 프롬프트
        full_prompt = (
            "안녕, 너는 곧 내가 제시하게 될 문장을 교정해야 해. 해당 문장들은 대부분 한국어 발음 및 발화에 익숙하지 않은 외국인의 발음을 STT 모델로 옮긴 결과물이 될 거야. "
            "오타 발생 여부와 앞뒤 문맥 구조를 파악하여야 하고, 오탈자 및 틀린 발음이 있다면 발생한 부분의 발음과 맞춤법을 올바르게 교정해 제시해야 해. "
            "문맥에 맞는 이야기를 하는지에 대해서도, 검사한 결과에 따라 올바르게 수정해줘. \"알겠습니다\" 같은 반응으로 시작하지 말고, 바로 교정된 텍스트만 올려 줘. \n\n"
            "결과를 아래 형식으로 제공해 줘:\n"
            "- [교정된 텍스트]\n\n"
            "이제 아래 문장을 분석하여 교정한 결과를 제시해 주세요."
            f"{request.prompt}"
        )

        body = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        data = response.json()

        # 응답에서 텍스트 추출
        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return {"reply": reply}
    
    except Exception as e:
        print(f"TTS 호출 실패: {e}")  # 로그에 출력되도록
        raise HTTPException(status_code=500, detail=f"Gemini API 호출 실패: {e}")
