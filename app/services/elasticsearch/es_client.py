from elasticsearch import Elasticsearch
from collections import Counter
import os
import traceback
from dotenv import load_dotenv

# 환경변수 로드 (다른 모듈에서 import할 때를 대비)
# 현재 디렉토리와 상위 디렉토리에서 .env 파일 찾기
import pathlib
current_dir = pathlib.Path(__file__).parent
root_dir = current_dir.parent.parent.parent  # app의 상위 디렉토리 (server)
env_paths = [
    root_dir / '.env',
    current_dir / '.env',
    pathlib.Path('.env')
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break
else:
    load_dotenv()  # 기본 로드

es_url = os.getenv("ELASTICSEARCH_URL")
es_username = os.getenv("ES_USERNAME")
es_password = os.getenv("ES_PASSWORD")

# 필수 환경변수 검증
if not all([es_url, es_username, es_password]):
    missing_vars = []
    if not es_url: missing_vars.append("ELASTICSEARCH_URL")
    if not es_username: missing_vars.append("ES_USERNAME")
    if not es_password: missing_vars.append("ES_PASSWORD")
    
    raise ValueError(f"필수 환경변수가 설정되지 않았습니다: {es_url}{', '.join(missing_vars)}")

try:
    es = Elasticsearch(es_url, basic_auth=(es_username, es_password))
    # 연결 테스트
    es.ping()
except Exception as e:
    print(f"Elasticsearch 연결 실패: {e}")
    raise

INDEX_NAME = os.getenv("ELASTICSEARCH_INDEX_NAME")
if not INDEX_NAME:
    raise ValueError("ELASTICSEARCH_INDEX_NAME 환경변수가 설정되지 않았습니다.")
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

def store_error_pattern(stt_text: str, enhanced_text: str):
    errors = []
    stt_words = stt_text.strip().split()
    enhanced_words = enhanced_text.strip().split()

    for stt_word, enhanced_word in zip(stt_words, enhanced_words):
        if stt_word != enhanced_word:
            errors.append((stt_word, "발음 오류"))

    error_term_counter = Counter([term for term, _ in errors])

    for term, count in error_term_counter.items():
        doc_id = f"{term}_pronunciation_error"
        doc = {
            "term": term,
            "term_text": term,
            "error_count": count,
            "category_distribution": [
                {"category": "발음 오류", "count": count}
            ],
            "sample_sentences": [stt_text]
        }

        try:
            es.update(index=INDEX_NAME, id=doc_id, body={
                "doc_as_upsert": True,
                "doc": doc
            })
            print(f"[Elasticsearch 저장 성공 - 단어: {term}]")
        except Exception as e:
            print(f"[Elasticsearch 저장 실패 - 단어: {term}]: {e}")
            traceback.print_exc()
