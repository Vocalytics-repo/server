# 인사이트 API 빠른 참조표

## API 엔드포인트 요약

| API | 메서드 | 엔드포인트 | 파라미터 | 주요 응답 필드 |
|-----|--------|------------|----------|----------------|
| **성별별 성과 분석** | GET | `/api/insights/gender-performance` | `level?`, `nationality?` | `male`, `female`, `comparison` |
| **국적별 분석 (전체)** | GET | `/api/insights/nationality-analysis` | 없음 | `nationality_stats`, `ranking` |
| **국적별 분석 (특정)** | GET | `/api/insights/nationality-analysis/{nationality}` | `nationality` (경로) | `nationality`, `count`, `common_errors` |
| **레벨별 성과 (전체)** | GET | `/api/insights/level-performance` | 없음 | `level_stats`, `progression_analysis` |
| **레벨별 성과 (특정)** | GET | `/api/insights/level-performance/{level}` | `level` (경로) | `level`, `count`, `csid_distribution` |
| **CSID 패턴 분석** | GET | `/api/insights/csid-patterns` | `sex?`, `nationality?`, `level?` | `csid_counts`, `csid_ratios`, `accuracy_rate` |
| **타입별 성과 분석** | GET | `/api/insights/type-performance` | 없음 | `string_analysis`, `word_analysis`, `comparison` |
| **텍스트 난이도 분석** | GET | `/api/insights/text-difficulty` | `limit?` (1-100) | `hardest_texts`, `easiest_texts`, `difficulty_distribution` |
| **발음 오류 분석** | GET | `/api/insights/pronunciation-errors` | `ref_text`, `limit?` (1-200) | `pronunciation_samples`, `error_analysis`, `insights` |
| **전체 지표 개요** | GET | `/api/insights/overview` | 없음 | `summary`, `csid_overview`, `top_error_patterns`, `key_insights` |
| **서비스 상태 확인** | GET | `/api/insights/health` | 없음 | `success`, `elasticsearch_connected` |

## 공통 파라미터 값

### 필터 파라미터
- **sex**: `"M"` (남성), `"F"` (여성)
- **nationality**: `"Chinese"`, `"Japanese"` 등
- **level**: `"A"`, `"B"`, `"C"` 등
- **type**: `"S"` (String), `"W"` (Word)

### 응답 데이터 타입
- **오류율 (error_rate)**: `number` (0.0 ~ 1.0)
- **개수 (count)**: `number` (정수)
- **CSID 값**: `number` (정수)
- **상관관계**: `number` (-1.0 ~ 1.0)

## 주요 응답 필드 설명

### CSID 분포 (`csid_distribution`)
```json
{
  "C": 1200,  // Correct (정확)
  "S": 80,    // Substitution (대체)
  "I": 20,    // Insertion (삽입)
  "D": 15     // Deletion (삭제)
}
```

### 통계 필드
- `avg_error_rate`: 평균 오류율
- `median_error_rate`: 중간값 오류율
- `std_error_rate`: 표준편차
- `sample_count`: 샘플 개수

## 빠른 시작 코드

### JavaScript/TypeScript
```javascript
const BASE_URL = 'http://localhost:8000/api/insights';

// 1. 성별별 성과 비교
const genderData = await fetch(`${BASE_URL}/gender-performance`).then(r => r.json());
console.log('남성 평균 오류율:', genderData.data.male.avg_error_rate);

// 2. 중국인 B레벨 CSID 패턴
const csidData = await fetch(`${BASE_URL}/csid-patterns?nationality=Chinese&level=B`).then(r => r.json());
console.log('정확도:', csidData.data.accuracy_rate);

// 3. 전체 지표 개요
const overviewData = await fetch(`${BASE_URL}/overview`).then(r => r.json());
console.log('전체 평균 오류율:', overviewData.data.summary.overall_avg_error_rate);
console.log('핵심 인사이트:', overviewData.data.key_insights);

// 4. 발음 오류 분석
const pronunciationData = await fetch(`${BASE_URL}/pronunciation-errors?ref_text=시계&limit=20`).then(r => r.json());
console.log('찾은 문서 수:', pronunciationData.data.found_documents);
console.log('첫 번째 샘플:', pronunciationData.data.pronunciation_samples[0]);
```

### Python
```python
import requests

BASE_URL = 'http://localhost:8000/api/insights'

# 1. 국적별 성과 랭킹
response = requests.get(f'{BASE_URL}/nationality-analysis')
ranking = response.json()['data']['ranking']
print('최고 성과 국적:', ranking['best_performance'][0][0])

# 2. 전체 지표 개요
response = requests.get(f'{BASE_URL}/overview')
overview = response.json()['data']
print('전체 정확도:', overview['summary']['overall_accuracy'])
print('핵심 인사이트:', overview['key_insights'])

# 3. 발음 오류 분석
response = requests.get(f'{BASE_URL}/pronunciation-errors', params={'ref_text': '시계', 'limit': 15})
pronunciation_data = response.json()['data']
print('검색 텍스트:', pronunciation_data['search_text'])
print('발음 샘플 수:', len(pronunciation_data['pronunciation_samples']))
```

### cURL
```bash
# 서비스 상태 확인
curl http://localhost:8000/api/insights/health

# 성별별 성과 (중국인 B레벨)
curl "http://localhost:8000/api/insights/gender-performance?level=B&nationality=Chinese"

# 전체 지표 개요
curl http://localhost:8000/api/insights/overview

# 발음 오류 분석 (시계)
curl "http://localhost:8000/api/insights/pronunciation-errors?ref_text=시계&limit=20"
```

## 사용 사례별 API 조합

### 대시보드 구성
```javascript
// 메인 대시보드 데이터 로드
async function loadDashboardData() {
  const [overview, gender, nationality, csid] = await Promise.all([
    fetch(`${BASE_URL}/overview`).then(r => r.json()),
    fetch(`${BASE_URL}/gender-performance`).then(r => r.json()),
    fetch(`${BASE_URL}/nationality-analysis`).then(r => r.json()),
    fetch(`${BASE_URL}/csid-patterns`).then(r => r.json())
  ]);
  
  return { overview, gender, nationality, csid };
}
```

### 개인 맞춤 분석
```javascript
// 특정 사용자 그룹 분석
async function analyzeUserGroup(sex, nationality, level) {
  const [csid, comparison] = await Promise.all([
    fetch(`${BASE_URL}/csid-patterns?sex=${sex}&nationality=${nationality}&level=${level}`).then(r => r.json()),
    fetch(`${BASE_URL}/gender-performance?nationality=${nationality}&level=${level}`).then(r => r.json())
  ]);
  
  return { csid, comparison };
}
```

### 학습 콘텐츠 추천
```javascript
// 난이도별 텍스트 추천
async function getRecommendedTexts(difficulty = 'easy') {
  const response = await fetch(`${BASE_URL}/text-difficulty?limit=50`);
  const data = await response.json();
  
  return difficulty === 'easy' ? data.data.easiest_texts : data.data.hardest_texts;
}
```

### 특정 단어/문장 발음 분석
```javascript
// 특정 텍스트의 발음 오류 패턴 분석
async function analyzePronunciationErrors(text, limit = 30) {
  const response = await fetch(`${BASE_URL}/pronunciation-errors?ref_text=${encodeURIComponent(text)}&limit=${limit}`);
  const data = await response.json();
  
  if (data.success && data.data.found_documents > 0) {
    return {
      samples: data.data.pronunciation_samples,
      errorPatterns: data.data.error_analysis.top_error_patterns,
      insights: data.data.insights
    };
  }
  
  return null;
}

// 사용 예시
const clockAnalysis = await analyzePronunciationErrors('시계');
console.log('시계 발음 인사이트:', clockAnalysis?.insights);
```

## 주의사항

1. **필터 조합**: 너무 세부적인 필터는 데이터 부족으로 빈 결과를 반환할 수 있음
2. **응답 시간**: 대용량 데이터 분석 시 응답 시간이 길어질 수 있음 (최대 30초)
3. **캐싱**: 동일한 요청은 클라이언트에서 캐싱 권장
4. **오류 처리**: 항상 `success` 필드를 확인하고 `message`로 오류 내용 파악

## 성능 최적화 팁

1. **병렬 요청**: 독립적인 API는 `Promise.all()`로 병렬 처리
2. **필요한 데이터만**: `limit` 파라미터로 데이터 양 조절
3. **조건부 요청**: 필터 조건이 있을 때만 API 호출
4. **상태 확인**: 주기적으로 `/health` 엔드포인트로 서비스 상태 모니터링 