# Vocalytics STT Backend

**Vocalytics**는 WebSocket 기반으로 음성 데이터를 받아  
OpenAI Whisper 모델을 활용해 실시간으로 텍스트로 변환(STT)하는 백엔드 서비스입니다.

> 🎧 프론트엔드에서 마이크로 수집된 PCM 오디오 데이터를 실시간으로 전송하면,  
> 이 백엔드가 Whisper로 변환하여 텍스트 결과를 응답합니다.

---

## ⚙️ 기술 스택

- **Framework**: FastAPI
- **Real-time**: Python-SocketIO (ASGI)
- **Speech Recognition**: Whisper (base model)
- **Audio Handling**: NumPy, wave, tempfile
- **Containerization**: Docker, docker-compose
