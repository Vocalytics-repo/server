import tempfile
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.stt.stt_service import transcribe_and_correct

router = APIRouter()

@router.post("/api/stt")
async def process_stt(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio.read())
            result = transcribe_and_correct(tmp.name)
            return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})