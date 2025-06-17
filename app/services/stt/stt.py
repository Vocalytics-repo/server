import tempfile
from shutil import copyfileobj
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.stt.stt_service import transcribe_and_correct

router = APIRouter()

@router.post("/api/stt")
async def process_stt(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            copyfileobj(audio.file, tmp)
            tmp.flush()
            tmp_path = tmp.name

        print(f"[DEBUG] 임시 저장 경로: {tmp_path}")

        result = transcribe_and_correct(tmp.name)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
