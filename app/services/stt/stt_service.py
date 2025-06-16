# app/services/stt_service.py
import requests
from services.elasticsearch.es_client import store_error_pattern

STT_API_URL = "http://voice-stt-container:8081/api/v1/stt"

def transcribe_with_external_stt(file_path: str) -> str:
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "audio/wav")}
        try:
            response = requests.post(STT_API_URL, files=files, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("text", "")
        except Exception as e:
            print(f"[STT 서버 오류]: {e}")
            return ""

def transcribe_and_correct(file_path: str) -> dict:
    # Whisper로 텍스트 변환
    transcription = transcribe_with_external_stt(file_path)
    
    try:
        from services.correction.gemini import PromptRequest, chat_with_gemini
        
        request = PromptRequest(prompt=transcription)
        
        gemini_response = chat_with_gemini(request)
        
        reply = gemini_response.get("reply", "")
        
        if "- [" in reply and "]" in reply:
            correction = reply.split("- [")[1].split("]")[0]
        else:
            correction = reply.strip()

        
        try:
            store_error_pattern(
                stt_text=transcription,
                enhanced_text=correction
            )
        except Exception as es_err:
            print(f"[Elasticsearch 저장 실패]: {es_err}")

            
    except Exception as e:
        print(f"Gemini API 호출 실패: {e}")
        correction = transcription 
    
    return {
        "transcription": transcription,
        "correction": correction
    }