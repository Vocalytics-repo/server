from fastapi import FastAPI, HTTPException
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

app = FastAPI()

# 데이터 모델 정의
class PromptRequest(BaseModel):
    prompt: str

# 엔드포인트 생성
@app.post("/chat")
def chat_with_gemini(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        # 개선된 사전 프롬프트
        full_prompt = (
            "안녕, 너는 곧 내가 제시하게 될 문장을 분석해야 해. 해당 문장들은 대부분 한국어 발음 및 발화에 익숙하지 않은 외국인의 발음을 STT 모델로 옮긴 결과물이 될 거야. "
            "오타 발생 여부와 앞뒤 문맥 구조를 파악하여야 하고, 오탈자 및 틀린 발음이 있다면 발생한 부분의 발음을 어떻게 교정해야 하는지 제시해 줘. "
            "문맥에 맞는 이야기를 하는지에 대해서도, 검사한 결과와 함께 권장되는 수정 사항을 제시해 줘.\n\n"
            "결과를 아래 형식으로 제공해 주세요:\n"
            "- 원문: [사용자 입력 문장]\n"
            "- 오탈자 및 교정 안내:\n"
            "  - [문제 발생 부분]: [교정 제안]\n"
            "- 문맥 검토:\n"
            "  - [검토 결과 및 권장사항]\n\n"
            "이제 아래 문장을 분석해 주세요."
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
        raise HTTPException(status_code=500, detail=f"Gemini API 호출 실패: {e}")
