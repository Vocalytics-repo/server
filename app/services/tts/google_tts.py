from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from google.cloud import texttospeech
from dotenv import load_dotenv
import os
import random
from io import BytesIO

# 환경변수 로드
load_dotenv()

# Google 인증 키 경로 환경변수 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/unique-conquest-459504-u5-85d90285f98e.json"

router = APIRouter()

# 요청 모델
class TTSRequest(BaseModel):
    text: str
    gender: str = "female"  # 기본값: female
    #voice_name: str = "ko-KR-Standard-A"  # 기본값은 기존 여자 목소리

#다음과 같은 목소리 세팅을 사용할 수 있음:
    #"ko-KR-Standard-A": 기본 여자 목소리 1
    #"ko-KR-Standard-B": 기본 여자 목소리 2
    #"ko-KR-Standard-C": 기본 남자 목소리 1
    #"ko-KR-Standard-D": 기본 남자 목소리 2
    # "ko-KR-Chirp3-HD-Achernar": 고급 여자 목소리 1
    # "ko-KR-Chirp3-HD-Leda": 고급 여자 목소리 2
    # "ko-KR-Chirp3-HD-Orus": 고급 남자 목소리 1
    # "ko-KR-Chirp3-HD-Algenib": 고급 남자 목소리 2

female_voices = ["ko-KR-Chirp3-HD-Achernar", "ko-KR-Chirp3-HD-Leda"]
male_voices = ["ko-KR-Chirp3-HD-Orus", "ko-KR-Chirp3-HD-Algenib"]

# TTS API 엔드포인트
@router.post("/api/tts")
def text_to_speech(request: TTSRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required.")

    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=request.text)
        
        # 성별에 따라 랜덤 목소리 선택
        if request.gender.lower() == "male":
            selected_voice = random.choice(male_voices)
        else:
            selected_voice = random.choice(female_voices)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name=selected_voice
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        audio_content = response.audio_content
        audio_length = len(audio_content)
        print(f"audio length: {audio_length}")

        if audio_length == 0:
            raise HTTPException(status_code=500, detail="TTS 결과 오디오 길이가 0입니다.")

        audio_stream = BytesIO(audio_content)
        audio_stream.seek(0)

        headers = {
            "Content-Disposition": "inline; filename=output.mp3",
            "Content-Length": str(audio_length)
        }

        return StreamingResponse(
            content=audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=output.mp3",
                "Content-Length": str(audio_length),
                "X-Content-Type-Options": "nosniff"
            }
        )

    except Exception as e:
        print(f"TTS 호출 실패: {e}")  # 로그에 출력되도록
        raise HTTPException(status_code=500, detail=f"TTS 호출 실패: {e}")