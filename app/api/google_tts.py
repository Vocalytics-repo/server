from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from google.cloud import texttospeech
from dotenv import load_dotenv
import os
from io import BytesIO

# 환경변수 로드
load_dotenv()

# Google 인증 키 경로 환경변수 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

app = FastAPI()

# 요청 모델
class TTSRequest(BaseModel):
    text: str

# TTS API 엔드포인트
@app.post("/api/tts")
def text_to_speech(request: TTSRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required.")

    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=request.text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Standard-A"
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
        raise HTTPException(status_code=500, detail=f"TTS 호출 실패: {e}")