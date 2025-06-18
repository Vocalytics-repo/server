# Vocalytics API Server
![ChatGPT Image 2025년 6월 15일 오후 09_01_18](https://github.com/user-attachments/assets/d9a3c938-6a85-4fcf-9a4f-e8fdb2406a2e)

**Vocalytics** is a comprehensive AI-powered API server for language learning.
It provides speech recognition (STT), text-to-speech (TTS), grammar correction, YouTube educational video search, and pronunciation learning data analysis features.

## Key Features

### Speech Recognition (STT)
- High-precision speech-to-text conversion based on **OpenAI Whisper**
- Real-time audio file upload and processing
- Integrated automatic grammar correction

### Text-to-Speech (TTS)
- High-quality speech synthesis using **Google Cloud TTS**
- Supports various languages and voice options
- Real-time voice generation and streaming

### Grammar Correction
- Intelligent text correction powered by **Google Gemini AI**
- Suggestions for grammar, spelling, and expression improvements
- Natural Korean expression transformation

### YouTube Educational Video Search
- Integrated with **YouTube Data API v3**
- Filters and searches videos for educational purposes
- Provides detailed video information and metadata

### Pronunciation Learning Insight Analysis
- Large-scale learning data analysis based on **Elasticsearch**
- Pronunciation performance analysis by gender, nationality, and proficiency level
- CSID (Correct, Substitution, Insertion, Deletion) error pattern analysis
- Personalized learning recommendations and difficulty analysis

---

## Tech Stack

### Backend Framework
- **FastAPI** – High-performance asynchronous web framework  
- **Python 3.9** – Primary development language  
- **Uvicorn** – ASGI server

### AI & Machine Learning
- **OpenAI Whisper** – Speech recognition  
- **Google Cloud TTS** – Text-to-speech synthesis  
- **Google Gemini** – Grammar correction and text analysis

### Data & Search
- **Elasticsearch 8.13** – Large-scale data search and analysis  
- **Kibana** – Data visualization and monitoring

### External APIs
- **YouTube Data API v3** – Educational video search  
- **Google API Client** – Integration with Google services

### Infrastructure
- **Docker & Docker Compose** – Containerization and orchestration  
- **CORS Middleware** – Cross-origin request support

---

## API endpoints

### Speech Recognition (STT)
```
POST /api/stt
- Upload audio files and convert text
- Includes automatic grammar corrections
```

### Text to Speech (TTS)
```
POST /api/tts
- Converting text to voice
- Support for a variety of voice options
```

### grammar correction
```
POST /api/correction
- Text Grammar and Expression Correction
- Gemini AI-based natural language processing
```

### grammar correction
```
POST /api/correction
- Text Grammar and Expression Correction
- Gemini AI-based natural language processing
```

### Pronunciation Learning Insights
```
GET /api/insights/overview                    # Overview of overall learning data  
GET /api/insights/gender-performance          # Pronunciation performance analysis by gender  
GET /api/insights/nationality-analysis        # Pronunciation characteristics by nationality  
GET /api/insights/nationality-analysis/{nationality}  # Analysis for a specific nationality  
GET /api/insights/level-performance           # Performance analysis by proficiency level  
GET /api/insights/level-performance/{level}   # Analysis for a specific level  
GET /api/insights/csid-patterns               # CSID (Correct, Substitution, Insertion, Deletion) error pattern analysis  
GET /api/insights/type-performance            # Performance analysis by type  
GET /api/insights/text-difficulty             # Text difficulty analysis  
GET /api/insights/pronunciation-errors        # Pronunciation error analysis  
GET /api/insights/health                      # Service health check
```

---

## Configuration Settings

### Required Environmental Variables
Create the '.env' file and set the following variables:

```env
# Google API Settings
GOOGLE_API_KEY=your_google_api_key_here

# Elasticsearch setting
ES_PASSWORD=your_elasticsearch_password
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_USERNAME=elastic

# Google Cloud Certification (for TTS)
GOOGLE_APPLICATION_CREDENTIALS=./your-credentials.json
```

### Set up a Google Cloud service account
1. Create a service account in Google Cloud Console
2. Text-to-Speech API Authorization
3. Download JSON key file and save it as `your-credentials.json`

---

## Installation and execution

### Local Development Environment

```bash
# Clone the repository  
git clone <repository-url>  
cd vocalytics-server

# Create and activate a virtual environment  
python -m venv venv  
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies  
pip install -r requirements.txt

# Set environment variables  
cp .env.example .env  
# Edit the .env file to add your API keys

# Run the server  
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running with Docker

```bash
# Run the full stack with Docker Compose
docker-compose up -d

# Check Logs
docker-compose logs -f backend
```

### Check Service
- **API Docs**: http://localhost:8000/docs
- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601

---

## Project Structure

```
vocalytics-server/
├── app/
│   ├── main.py                 # Entry point of the FastAPI application  
│   ├── event.py                # Router integration management  
│   ├── services/               # Core service modules  
│   │   ├── stt/                # Speech recognition service  
│   │   ├── tts/                # Text-to-speech service  
│   │   ├── correction/         # Grammar correction service  
│   │   ├── youtube/            # YouTube search service  
│   │   ├── insight/            # Learning data analysis service  
│   │   └── elasticsearch/      # Elasticsearch client  
│   ├── config/                 # Configuration files  
│   └── utils/                  # Utility functions  
├── requirements.txt            # Python dependencies  
├── docker-compose.yml          # Docker container configuration  
├── Dockerfile                  # Docker image build settings  
└── .env                        # Environment variables (needs to be created)
```

---

## Use Examples

### Speech Recognition (STT)
```bash
curl -X POST "http://localhost:8000/api/stt" \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@your_audio_file.wav"
```

### Search for YouTube videos
```bash
curl "http://localhost:8000/youtube/search?query=한국어 초급자를 위한 교육 영상&max_results=10"
```

### Analysis of pronunciation performance
```bash
# Analysis of Pronunciation Performance by Gender
curl "http://localhost:8000/api/insights/gender-performance"

# Analysis of pronunciation characteristics of a particular nationality
curl "http://localhost:8000/api/insights/nationality-analysis/Chinese"
```
