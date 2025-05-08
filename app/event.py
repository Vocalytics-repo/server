import tempfile
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.stt.stt_service import transcribe_with_whisper

router = APIRouter()

@router.post("/api/stt")
async def process_stt(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio.read())
            result = transcribe_with_whisper(tmp.name)
            return JSONResponse({
                "transcription": result,
                "correction": None  # 추가적인 교정 로직이 있다면 여기에 구현
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})