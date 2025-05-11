# Dockerfile
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

ENV PYTHONPATH=/app

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    apt-get clean

# requirements.txt 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY ./app /app

COPY unique-conquest-459504-u5-85d90285f98e.json /app/

# 실행 명령: uvicorn으로 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]