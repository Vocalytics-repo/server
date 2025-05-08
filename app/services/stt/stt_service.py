# app/services/stt_service.py
import whisper

model = whisper.load_model("small")

def transcribe_with_whisper(file_path: str) -> str:
    result = model.transcribe(file_path, language="ko")
    return result["text"]