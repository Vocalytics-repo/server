from elasticsearch import Elasticsearch

es = Elasticsearch("http://es:9200")

def store_error_pattern(stt_text: str, enhanced_text: str):
    errors = []
    stt_words = stt_text.strip().split()
    enhanced_words = enhanced_text.strip().split()

    # 단순 단어 비교
    for stt_word, enhanced_word in zip(stt_words, enhanced_words):
        if stt_word != enhanced_word:
            errors.append(stt_word)

    error_count = len(errors)
    error_rate = error_count / len(stt_words) if stt_words else 0.0

    doc = {
        "stt_text": stt_text,
        "enhanced_text": enhanced_text,
        "error_count": error_count,
        "error_rate": error_rate,
        "error_words": errors,
        "error_sentences": [stt_text]  # 배열 형태
    }

    es.index(index="error_patterns", document=doc)