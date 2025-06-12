from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

def store_error_pattern(user_id: str, stt_text: str, enhanced_text: str):
    errors = []
    stt_words = stt_text.strip().split()
    enhanced_words = enhanced_text.strip().split()

    # 아주 단순한 오류 추출
    for i, (stt_word, enhanced_word) in enumerate(zip(stt_words, enhanced_words)):
        if stt_word != enhanced_word:
            errors.append({
                "error_type": "vocabulary",
                "original": stt_word,
                "corrected": enhanced_word,
                "category": "어휘",
                "position": i
            })

    error_count = len(errors)
    error_rate = error_count / len(stt_words) if stt_words else 0.0
    error_words = [e["original"] for e in errors]
    error_sentences = [stt_text]
    doc = {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "stt_text": stt_text,
        "enhanced_text": enhanced_text,
        "error_count": error_count,
        "error_rate": error_rate,
        "errors": errors,
        "error_words": error_words,
        "error_sentences": error_sentences
    }

    es.index(index="error_patterns", document=doc)