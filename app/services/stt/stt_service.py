# app/services/stt_service.py
import whisper
from services.elasticsearch.es_client import store_error_pattern

model = whisper.load_model("small")

def transcribe_with_whisper(file_path: str) -> str:
    result = model.transcribe(file_path, language="ko")
    return result["text"]

def transcribe_and_correct(file_path: str) -> dict:
    # Whisper로 텍스트 변환
    transcription = transcribe_with_whisper(file_path)
    
    try:
        from services.correction.gemini import PromptRequest, chat_with_gemini
        
        request = PromptRequest(prompt=transcription)
        
        gemini_response = chat_with_gemini(request)
        
        reply = gemini_response.get("reply", "")
        
        if "- [" in reply and "]" in reply:
            correction = reply.split("- [")[1].split("]")[0]
        else:
            correction = reply.strip()

        store_error_pattern(
            user_id="test_user",
            stt_text=transcription,
            enhanced_text=correction
        )

            
    except Exception as e:
        print(f"Gemini API 호출 실패: {e}")
        correction = transcription 
    
    return {
        "transcription": transcription,
        "correction": correction
    }