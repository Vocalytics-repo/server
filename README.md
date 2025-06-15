# Vocalytics API Server
**Vocalytics**는 언어 학습을 위한 종합적인 AI 기반 API 서버입니다.  
음성 인식(STT), 텍스트 음성 변환(TTS), 문법 교정, YouTube 교육 영상 검색, 그리고 발음 학습 데이터 분석 기능을 제공합니다.

## 주요 기능

### 음성 인식 (STT)
- **OpenAI Whisper** 기반 고정밀 음성-텍스트 변환
- 실시간 오디오 파일 업로드 및 처리
- 자동 문법 교정 통합

### 텍스트 음성 변환 (TTS)
- **Google Cloud TTS** 활용 고품질 음성 합성
- 다양한 언어 및 음성 옵션 지원
- 실시간 음성 생성 및 스트리밍

### 문법 교정
- **Google Gemini AI** 기반 지능형 텍스트 교정
- 문법, 맞춤법, 표현 개선 제안
- 자연스러운 한국어 표현 변환

### YouTube 교육 영상 검색
- **YouTube Data API v3** 통합
- 교육 목적 영상 필터링 및 검색
- 상세 영상 정보 및 메타데이터 제공

### 발음 학습 인사이트 분석
- **Elasticsearch** 기반 대용량 학습 데이터 분석
- 성별, 국적, 레벨별 발음 성과 분석
- CSID(Correct, Substitution, Insertion, Deletion) 오류 패턴 분석
- 개인화된 학습 추천 및 난이도 분석

---

## 기술 스택

### Backend Framework
- **FastAPI** - 고성능 비동기 웹 프레임워크
- **Python 3.9** - 메인 개발 언어
- **Uvicorn** - ASGI 서버

### AI & Machine Learning
- **OpenAI Whisper** - 음성 인식
- **Google Cloud TTS** - 텍스트 음성 변환
- **Google Gemini** - 문법 교정 및 텍스트 분석

### Data & Search
- **Elasticsearch 8.13** - 대용량 데이터 검색 및 분석
- **Kibana** - 데이터 시각화 및 모니터링

### External APIs
- **YouTube Data API v3** - 교육 영상 검색
- **Google API Client** - Google 서비스 통합

### Infrastructure
- **Docker & Docker Compose** - 컨테이너화 및 오케스트레이션
- **CORS Middleware** - 크로스 오리진 요청 지원

---

## API 엔드포인트

### 음성 인식 (STT)
```
POST /api/stt
- 오디오 파일 업로드 및 텍스트 변환
- 자동 문법 교정 포함
```

### 텍스트 음성 변환 (TTS)
```
POST /api/tts
- 텍스트를 음성으로 변환
- 다양한 음성 옵션 지원
```

### 문법 교정
```
POST /api/correction
- 텍스트 문법 및 표현 교정
- Gemini AI 기반 자연어 처리
```

### YouTube 검색
```
GET /youtube/search
POST /youtube/search
GET /youtube/video/{video_id}
GET /youtube/health
```

### 발음 학습 인사이트
```
GET /api/insights/overview                    # 전체 학습 데이터 개요
GET /api/insights/gender-performance          # 성별별 발음 성과 분석
GET /api/insights/nationality-analysis        # 국적별 발음 특성 분석
GET /api/insights/nationality-analysis/{nationality}  # 특정 국적 분석
GET /api/insights/level-performance           # 레벨별 성과 분석
GET /api/insights/level-performance/{level}   # 특정 레벨 분석
GET /api/insights/csid-patterns              # CSID 오류 패턴 분석
GET /api/insights/type-performance           # 타입별 성과 분석
GET /api/insights/text-difficulty            # 텍스트 난이도 분석
GET /api/insights/pronunciation-errors       # 발음 오류 분석
GET /api/insights/health                     # 서비스 상태 확인
```

---

## 환경 설정

### 필수 환경 변수
`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# Google API 설정
GOOGLE_API_KEY=your_google_api_key_here

# Elasticsearch 설정
ES_PASSWORD=your_elasticsearch_password
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_USERNAME=elastic

# Google Cloud 인증 (TTS용)
GOOGLE_APPLICATION_CREDENTIALS=./your-credentials.json
```

### Google Cloud 서비스 계정 설정
1. Google Cloud Console에서 서비스 계정 생성
2. Text-to-Speech API 권한 부여
3. JSON 키 파일 다운로드 후 `your-credentials.json`으로 저장

---

## 설치 및 실행

### 로컬 개발 환경

```bash
# 저장소 클론
git clone <repository-url>
cd vocalytics-server

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 API 키 설정

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker를 이용한 실행

```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f backend
```

### 서비스 확인
- **API 문서**: http://localhost:8000/docs
- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601

---

## 프로젝트 구조

```
vocalytics-server/
├── app/
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── event.py               # 라우터 통합 관리
│   ├── services/              # 핵심 서비스 모듈
│   │   ├── stt/              # 음성 인식 서비스
│   │   ├── tts/              # 텍스트 음성 변환 서비스
│   │   ├── correction/       # 문법 교정 서비스
│   │   ├── youtube/          # YouTube 검색 서비스
│   │   ├── insight/          # 학습 데이터 분석 서비스
│   │   └── elasticsearch/    # Elasticsearch 클라이언트
│   ├── config/               # 설정 파일
│   └── utils/                # 유틸리티 함수
├── requirements.txt          # Python 의존성
├── docker-compose.yml       # Docker 컨테이너 구성
├── Dockerfile              # Docker 이미지 빌드 설정
└── .env                    # 환경 변수 (생성 필요)
```

---

## 사용 예시

### 음성 인식 (STT)
```bash
curl -X POST "http://localhost:8000/api/stt" \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@your_audio_file.wav"
```

### YouTube 영상 검색
```bash
curl "http://localhost:8000/youtube/search?query=한국어 초급자를 위한 교육 영상&max_results=10"
```

### 발음 성과 분석
```bash
# 성별별 발음 성과 분석
curl "http://localhost:8000/api/insights/gender-performance"

# 특정 국적의 발음 특성 분석
curl "http://localhost:8000/api/insights/nationality-analysis/Chinese"
```

---

## 개발 및 기여

### 개발 환경 설정
1. Python 3.9+ 설치
2. FFmpeg 설치 (음성 처리용)
3. Docker 및 Docker Compose 설치

### 코드 스타일
- **Black** - 코드 포매팅
- **FastAPI** 표준 구조 준수
- **Type Hints** 사용 권장

---
