# Vocalytics API Server

**Vocalytics**는 다양한 언어 학습 도구를 제공하는 통합 API 서버입니다.  
음성 인식(STT), 텍스트 음성 변환(TTS), 문법 교정, YouTube 교육 영상 검색 기능을 제공합니다.

## 주요 기능

- **🎧 음성 인식 (STT)**: OpenAI Whisper를 활용한 실시간 음성-텍스트 변환
- **🔊 텍스트 음성 변환 (TTS)**: Google Cloud TTS를 활용한 고품질 음성 합성
- **✏️ 문법 교정**: Gemini AI를 활용한 텍스트 문법 및 표현 교정
- **📺 YouTube 검색**: YouTube Data API v3를 활용한 교육 영상 검색

---

## ⚙️ 기술 스택

- **Framework**: FastAPI
- **Real-time**: Python-SocketIO (ASGI)
- **Speech Recognition**: OpenAI Whisper
- **Text-to-Speech**: Google Cloud TTS
- **AI Correction**: Google Gemini
- **YouTube Integration**: YouTube Data API v3
- **Audio Handling**: NumPy, wave, tempfile
- **Containerization**: Docker, docker-compose

## API 엔드포인트

### YouTube 검색 API
- `GET /youtube/search` - YouTube 영상 검색
- `POST /youtube/search` - YouTube 영상 검색 (상세 옵션)
- `GET /youtube/video/{video_id}` - 특정 영상 상세 정보
- `GET /youtube/health` - YouTube 서비스 상태 확인

### 사용 예시
```bash
# "한국어 초급자를 위한 교육 영상" 검색
curl "http://localhost:8000/youtube/search?query=한국어 초급자를 위한 교육 영상&max_results=10"
```

## 🔧 환경 설정

1. `env.example` 파일을 `.env`로 복사
2. Google API Key 설정:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.
