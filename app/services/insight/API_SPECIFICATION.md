# 한국어 학습 인사이트 API 명세서

클라이언트 개발자를 위한 상세한 API 파라미터 및 응답 필드 명세서입니다.

## Base URL
```
http://localhost:8000
```

## 공통 응답 형식

모든 API는 다음과 같은 공통 응답 구조를 가집니다:

```typescript
interface CommonResponse<T> {
  success: boolean;
  data: T;
  message: string;
}
```

---

## 1. 성별별 발음 성과 분석 API

### **요청**
```http
GET /api/insights/gender-performance
```

### **요청 파라미터**
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|----|------|------|
| `level` | string | X  | 레벨 필터 | `"A"`, `"B"`, `"C"` |
| `nationality` | string | X  | 국적 필터 | `"Chinese"`, `"Japanese"` |

### **응답 필드**
```typescript
interface GenderPerformanceResponse {
  male: {
    count: number;                    // 남성 샘플 수
    avg_error_rate: number;           // 평균 오류율 (0.0-1.0)
    median_error_rate: number;        // 중간값 오류율
    std_error_rate: number;           // 표준편차
    csid_distribution: {              // CSID 분포
      C: number;                      // Correct 개수
      S: number;                      // Substitution 개수
      I: number;                      // Insertion 개수
      D: number;                      // Deletion 개수
    };
    level_distribution: {             // 레벨별 분포
      [level: string]: number;        // 레벨: 개수
    };
  };
  female: {
    // male과 동일한 구조
  };
  comparison: {
    error_rate_difference: number;    // 남성 - 여성 오류율 차이
    total_samples: number;            // 전체 샘플 수
  };
}
```

### **사용 예시**
```javascript
// 전체 성별 비교
const response = await fetch('/api/insights/gender-performance');

// 중국인 B레벨만 필터링
const filteredResponse = await fetch('/api/insights/gender-performance?level=B&nationality=Chinese');
```

---

## 2. 국적별 발음 특성 분석 API

### **요청 (전체 국적 비교)**
```http
GET /api/insights/nationality-analysis
```

### **요청 파라미터**
없음

### **응답 필드**
```typescript
interface NationalityAnalysisResponse {
  nationality_stats: {
    [nationality: string]: {
      count: number;                  // 해당 국적 샘플 수
      avg_error_rate: number;         // 평균 오류율
      csid_distribution: {
        C: number;
        S: number;
        I: number;
        D: number;
      };
    };
  };
  ranking: {
    best_performance: Array<[string, NationalityStats]>;    // 성과 좋은 순
    worst_performance: Array<[string, NationalityStats]>;   // 성과 나쁜 순
  };
}
```

### **요청 (특정 국적 분석)**
```http
GET /api/insights/nationality-analysis/{nationality}
```

### **경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| `nationality` | string | ✅ | 분석할 국적 | `"Chinese"`, `"Japanese"` |

### **응답 필드**
```typescript
interface SpecificNationalityResponse {
  nationality: string;                // 분석 대상 국적
  count: number;                      // 샘플 수
  avg_error_rate: number;             // 평균 오류율
  median_error_rate: number;          // 중간값 오류율
  csid_distribution: {
    C: number;
    S: number;
    I: number;
    D: number;
  };
  level_distribution: {
    [level: string]: number;          // 레벨별 분포
  };
  common_errors: {
    [error: string]: number;          // 공통 오류 패턴 TOP 10
  };
}
```

---

## 3. 레벨별 성과 분석 API

### **요청 (전체 레벨 비교)**
```http
GET /api/insights/level-performance
```

### **응답 필드**
```typescript
interface LevelPerformanceResponse {
  level_stats: {
    [level: string]: {
      count: number;
      avg_error_rate: number;
      median_error_rate: number;
      csid_distribution: {
        C: number;
        S: number;
        I: number;
        D: number;
      };
    };
  };
  progression_analysis: {
    levels: string[];                 // 레벨 순서
    error_rate_trend: number[];       // 레벨별 오류율 트렌드
    improvement_rate: number;         // 전체 개선율
  };
}
```

### **요청 (특정 레벨 분석)**
```http
GET /api/insights/level-performance/{level}
```

### **경로 파라미터**
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| `level` | string | ✅ | 분석할 레벨 | `"A"`, `"B"`, `"C"` |

### **응답 필드**
```typescript
interface SpecificLevelResponse {
  level: string;                      // 분석 대상 레벨
  count: number;                      // 샘플 수
  avg_error_rate: number;             // 평균 오류율
  median_error_rate: number;          // 중간값 오류율
  csid_distribution: {
    C: number;
    S: number;
    I: number;
    D: number;
  };
}
```

---

## 4. CSID 오류 패턴 분석 API

### **요청**
```http
GET /api/insights/csid-patterns
```

### **요청 파라미터**
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|----|------|------|
| `sex` | string | X  | 성별 필터 | `"M"`, `"F"` |
| `nationality` | string | X  | 국적 필터 | `"Chinese"` |
| `level` | string | X  | 레벨 필터 | `"B"` |

### **응답 필드**
```typescript
interface CSIDPatternsResponse {
  sample_count: number;               // 분석 샘플 수
  csid_counts: {                      // CSID 절대 개수
    C: number;                        // Correct 개수
    S: number;                        // Substitution 개수
    I: number;                        // Insertion 개수
    D: number;                        // Deletion 개수
  };
  csid_ratios: {                      // CSID 비율 (%)
    C: number;                        // Correct 비율
    S: number;                        // Substitution 비율
    I: number;                        // Insertion 비율
    D: number;                        // Deletion 비율
  };
  error_distribution: {               // 오류 중에서의 분포 (%)
    S: number;                        // Substitution 비율
    I: number;                        // Insertion 비율
    D: number;                        // Deletion 비율
  };
  total_operations: number;           // 전체 연산 수
  total_errors: number;               // 전체 오류 수
  accuracy_rate: number;              // 정확도 (%)
}
```

---

## 5. 타입별 성과 분석 API

### **요청**
```http
GET /api/insights/type-performance
```

### **요청 파라미터**
없음

### **응답 필드**
```typescript
interface TypePerformanceResponse {
  string_analysis: {
    type: "String";
    count: number;                    // String 타입 샘플 수
    avg_error_rate: number;           // 평균 오류율
    median_error_rate: number;        // 중간값 오류율
    csid_distribution: {
      C: number;
      S: number;
      I: number;
      D: number;
    };
  };
  word_analysis: {
    type: "Word";
    count: number;                    // Word 타입 샘플 수
    avg_error_rate: number;           // 평균 오류율
    median_error_rate: number;        // 중간값 오류율
    csid_distribution: {
      C: number;
      S: number;
      I: number;
      D: number;
    };
  };
  comparison: {
    error_rate_difference: number;    // String - Word 오류율 차이
    better_performance: "String" | "Word";  // 더 좋은 성과를 보인 타입
    total_samples: number;            // 전체 샘플 수
  };
}
```

---

## 6. 참조 텍스트 난이도 분석 API

### **요청**
```http
GET /api/insights/text-difficulty
```

### **요청 파라미터**
| 파라미터 | 타입 | 필수 | 기본값 | 설명 | 범위 |
|---------|------|----|--------|------|------|
| `limit` | integer | X  | 20 | 반환할 텍스트 개수 | 1-100 |

### **응답 필드**
```typescript
interface TextDifficultyResponse {
  total_unique_texts: number;         // 전체 고유 텍스트 수
  hardest_texts: Array<{
    text: string;                     // 텍스트 내용
    sample_count: number;             // 해당 텍스트 샘플 수
    avg_error_rate: number;           // 평균 오류율
    median_error_rate: number;        // 중간값 오류율
    std_error_rate: number;           // 표준편차
    text_length: number;              // 텍스트 길이
    csid_distribution: {
      C: number;
      S: number;
      I: number;
      D: number;
    };
  }>;
  easiest_texts: Array<{
    // hardest_texts와 동일한 구조
  }>;
  difficulty_distribution: {
    very_hard: number;                // 매우 어려운 텍스트 수 (오류율 > 0.3)
    hard: number;                     // 어려운 텍스트 수 (0.2 < 오류율 <= 0.3)
    medium: number;                   // 보통 텍스트 수 (0.1 < 오류율 <= 0.2)
    easy: number;                     // 쉬운 텍스트 수 (오류율 <= 0.1)
  };
}
```

---

## 7. 발음 오류 분석 API

### **요청**
```http
GET /api/insights/pronunciation-errors
```

### **요청 파라미터**
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| `ref_text` | string | ✅ | 분석할 참조 텍스트 | `"시계"`, `"안녕하세요"` |
| `limit` | number | X | 반환할 최대 문서 수 (기본값: 50) | `20`, `100` |

### **응답 필드**
```typescript
interface PronunciationErrorsResponse {
  search_text: string;                // 검색한 텍스트
  found_documents: number;            // 찾은 문서 수
  pronunciation_samples: Array<{
    ref: string;                      // 참조 텍스트
    ans: string;                      // 정답 발음
    rec: string;                      // 모델이 인식한 발음
    error: string;                    // 오류 설명
    csid: {                          // CSID 분포
      C: number;                      // Correct 개수
      S: number;                      // Substitution 개수
      I: number;                      // Insertion 개수
      D: number;                      // Deletion 개수
    };
    metadata: {                       // 메타데이터
      sex: string;                    // 성별 (M/F)
      nationality: string;            // 국적
      level: string;                  // 레벨
      type: string;                   // 타입 (S/W)
    };
  }>;
  error_analysis: {
    top_error_patterns: {             // 상위 10개 오류 패턴
      [error_description: string]: number;
    };
    gender_performance: {             // 성별별 성과
      [gender: string]: {
        count: number;                // 샘플 수
        avg_error_rate: number;       // 평균 오류율
        median_error_rate: number;    // 중간값 오류율
      };
    };
    nationality_performance: {        // 국적별 성과 (상위 5개)
      [nationality: string]: {
        count: number;
        avg_error_rate: number;
      };
    };
    level_performance: {              // 레벨별 성과
      [level: string]: {
        count: number;
        avg_error_rate: number;
      };
    };
  };
  insights: string[];                 // 인사이트 (한국어)
}
```

### **사용 예시**
```javascript
// 시계 단어 분석
const response = await fetch('/api/insights/pronunciation-errors?ref_text=시계&limit=20');

// 안녕하세요 문장 분석
const response2 = await fetch('/api/insights/pronunciation-errors?ref_text=안녕하세요&limit=30');
```

### **Python 예시**
```python
import requests

# 발음 오류 분석 요청
response = requests.get(
    'http://localhost:8000/api/insights/pronunciation-errors',
    params={
        'ref_text': '시계',
        'limit': 25
    }
)

data = response.json()
if data['success']:
    print(f"검색 텍스트: {data['data']['search_text']}")
    print(f"찾은 문서 수: {data['data']['found_documents']}")
    
    # 발음 샘플 출력
    for sample in data['data']['pronunciation_samples'][:3]:
        print(f"정답: {sample['ans']}")
        print(f"인식: {sample['rec']}")
        print(f"오류: {sample['error']}")
        print("---")
```

### **cURL 예시**
```bash
# 시계 단어 분석
curl "http://localhost:8000/api/insights/pronunciation-errors?ref_text=시계&limit=20"

# 안녕하세요 문장 분석
curl "http://localhost:8000/api/insights/pronunciation-errors?ref_text=안녕하세요&limit=15"
```

### **특별 응답 케이스**
데이터를 찾을 수 없는 경우:
```typescript
interface NoDataResponse {
  search_text: string;
  found_documents: 0;
  message: string;                    // "'{텍스트}'와 관련된 발음 데이터를 찾을 수 없습니다."
}
```

---

## 8. 전체 지표 개요 API

### **요청**
```http
GET /api/insights/overview
```

### **요청 파라미터**
없음

### **응답 필드**
```typescript
interface OverviewResponse {
  summary: {
    total_samples: number;            // 전체 샘플 수
    overall_avg_error_rate: number;   // 전체 평균 오류율
    overall_accuracy: number;         // 전체 정확도 (%)
    data_coverage: {
      nationalities: number;          // 국적 수
      levels: number;                 // 레벨 수
      unique_texts: number;           // 고유 텍스트 수
    };
  };
  csid_overview: {
    totals: {                         // CSID 절대 개수
      C: number;
      S: number;
      I: number;
      D: number;
    };
    ratios: {                         // CSID 비율 (%)
      C: number;
      S: number;
      I: number;
      D: number;
    };
  };
  top_error_patterns: {               // 상위 3개 오류 패턴
    [error_description: string]: number;
  };
  gender_summary: {
    male: {
      count: number;
      avg_error_rate: number;
    };
    female: {
      count: number;
      avg_error_rate: number;
    };
  };
  nationality_summary: {              // 상위 5개 국적
    [nationality: string]: {
      count: number;
      avg_error_rate: number;
    };
  };
  level_summary: {
    [level: string]: {
      count: number;
      avg_error_rate: number;
    };
  };
  type_summary: {
    string: {
      count: number;
      avg_error_rate: number;
    };
    word: {
      count: number;
      avg_error_rate: number;
    };
  };
  hardest_texts: Array<{              // 가장 어려운 텍스트 TOP 3
    text: string;
    avg_error_rate: number;
    sample_count: number;
  }>;
  key_insights: string[];             // 핵심 인사이트 (한국어)
}
```

---

## 9. 서비스 상태 확인 API

### **요청**
```http
GET /api/insights/health
```

### **요청 파라미터**
없음

### **응답 필드**
```typescript
interface HealthCheckResponse {
  success: boolean;                   // 서비스 상태
  message: string;                    // 상태 메시지 (한국어)
  elasticsearch_connected: boolean;   // Elasticsearch 연결 상태
  index_name?: string;                // 사용 중인 인덱스 이름 (연결 시에만)
}
```

---

## 오류 응답

모든 API에서 오류 발생 시 다음과 같은 형식으로 응답합니다:

```typescript
interface ErrorResponse {
  success: false;
  data?: any;                         // 부분적 데이터 (있는 경우)
  message: string;                    // 오류 메시지 (한국어)
}
```

### 주요 HTTP 상태 코드
- `200`: 성공
- `400`: 잘못된 요청 (파라미터 오류)
- `404`: 데이터 없음 (특정 국적/레벨 등)
- `500`: 서버 내부 오류

---

## 클라이언트 구현 팁

### 1. TypeScript 타입 정의
```typescript
// 공통 응답 타입
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

// API 클라이언트 클래스
class InsightApiClient {
  private baseUrl = 'http://localhost:8000/api/insights';
  
  async getGenderPerformance(filters?: {
    level?: string;
    nationality?: string;
  }): Promise<ApiResponse<GenderPerformanceResponse>> {
    const params = new URLSearchParams();
    if (filters?.level) params.append('level', filters.level);
    if (filters?.nationality) params.append('nationality', filters.nationality);
    
    const response = await fetch(`${this.baseUrl}/gender-performance?${params}`);
    return response.json();
  }
}
```

### 2. 오류 처리
```javascript
try {
  const response = await fetch('/api/insights/gender-performance');
  const data = await response.json();
  
  if (!data.success) {
    console.error('API 오류:', data.message);
    return;
  }
  
  // 성공적인 응답 처리
  console.log('남성 평균 오류율:', data.data.male.avg_error_rate);
} catch (error) {
  console.error('네트워크 오류:', error);
}
```

### 3. 데이터 시각화 예시
```javascript
// Chart.js를 사용한 CSID 분포 차트
function createCSIDChart(csidData) {
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Correct', 'Substitution', 'Insertion', 'Deletion'],
      datasets: [{
        data: [
          csidData.C,
          csidData.S,
          csidData.I,
          csidData.D
        ],
        backgroundColor: ['#4CAF50', '#FF9800', '#F44336', '#9C27B0']
      }]
    }
  });
}
```

---