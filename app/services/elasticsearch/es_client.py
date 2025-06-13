from elasticsearch import Elasticsearch
from collections import Counter

es = Elasticsearch("http://es:9200")

def store_error_pattern(stt_text: str, enhanced_text: str):
    errors = []
    stt_words = stt_text.strip().split()
    enhanced_words = enhanced_text.strip().split()

    # 단순 단어 비교를 통해 오류 단어 추출
    for stt_word, enhanced_word in zip(stt_words, enhanced_words):
        if stt_word != enhanced_word:
            errors.append((stt_word, "발음 오류"))

    error_count = len(errors)
    error_term_counter = Counter([term for term, _ in errors])

    # Elasticsearch에 저장
    for term, count in error_term_counter.items():
        doc = {
            "term": term,
            "term_text": term,
            "error_count": count,
            "category_distribution": [
                {
                    "category": "발음 오류",
                    "count": count
                }
            ],
            "sample_sentences": [stt_text]
        }

        try:
            es.index(index="pronunciation_insights_aggregated", document=doc)
        except Exception as e:
            print(f"[Elasticsearch 저장 실패 - 단어: {term}]: {e}")