from elasticsearch import Elasticsearch
from collections import Counter
import os
import traceback

es = Elasticsearch("http://es:9200", basic_auth=("elastic", os.getenv("ES_PASSWORD")))


INDEX_NAME = "pronunciation_insights_aggregated"
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
