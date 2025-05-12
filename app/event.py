from fastapi import APIRouter
from services.stt.stt import router as stt_router
from services.tts.google_tts import router as tts_router
from services.correction.gemini import router as corr_router

router = APIRouter()

router.include_router(stt_router)
router.include_router(tts_router)
router.include_router(corr_router)