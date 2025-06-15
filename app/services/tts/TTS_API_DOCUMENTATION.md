# TTS (Text-to-Speech) API 문서

## 개요

Vocalytics TTS API는 텍스트를 자연스러운 한국어 음성으로 변환하는 서비스입니다. Google Cloud Text-to-Speech API를 기반으로 하여 고품질의 음성 합성을 제공합니다.

---

## 기본 정보

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Content-Type**: `application/json`
- **Response Type**: `audio/mpeg` (MP3)

---

## 엔드포인트

### POST /api/tts

텍스트를 한국어 음성으로 변환합니다.

#### 요청

**URL**: `POST /api/tts`

**Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "text": "안녕하세요. 반갑습니다.",
  "gender": "female"
}
```

#### 요청 파라미터

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| `text` | string | ✅ | - | 음성으로 변환할 텍스트 |
| `gender` | string | ❌ | `"female"` | 음성 성별 (`"male"` 또는 `"female"`) |

#### 지원 음성

| 성별 | 음성 코드 | 설명 |
|------|-----------|------|
| 여성 | `ko-KR-Standard-A` | 기본 여자 목소리 1 |
| 여성 | `ko-KR-Standard-B` | 기본 여자 목소리 2 |
| 남성 | `ko-KR-Standard-C` | 기본 남자 목소리 1 |
| 남성 | `ko-KR-Standard-D` | 기본 남자 목소리 2 |

> **참고**: 같은 성별 내에서 음성은 랜덤으로 선택됩니다.

#### 응답

**성공 응답 (200 OK)**:
```http
HTTP/1.1 200 OK
Content-Type: audio/mpeg
Content-Disposition: inline; filename=output.mp3
Content-Length: [파일크기]
X-Content-Type-Options: nosniff

[MP3 오디오 데이터]
```

**에러 응답**:

| 상태 코드 | 설명 | 응답 예시 |
|-----------|------|-----------|
| 400 | 잘못된 요청 | `{"detail": "Text is required."}` |
| 500 | 서버 오류 | `{"detail": "TTS 호출 실패: [오류메시지]"}` |

---

## 사용 예시

### cURL

```bash
# 기본 여성 음성으로 변환
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "안녕하세요. 오늘 날씨가 좋네요."}' \
  --output output.mp3

# 남성 음성으로 변환
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "반갑습니다. 한국어를 배워보세요.", "gender": "male"}' \
  --output output_male.mp3
```

### JavaScript (Fetch API)

```javascript
// 기본 사용법
async function textToSpeech(text, gender = 'female') {
  try {
    const response = await fetch('/api/tts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        gender: gender
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    
    // 오디오 재생
    const audio = new Audio(audioUrl);
    audio.play();
    
    return audioUrl;
  } catch (error) {
    console.error('TTS 요청 실패:', error);
    throw error;
  }
}

// 사용 예시
textToSpeech('안녕하세요. 한국어 학습을 시작해보세요!', 'female');
textToSpeech('오늘도 좋은 하루 되세요.', 'male');
```

### Python (requests)

```python
import requests

def text_to_speech(text, gender='female', output_file='output.mp3'):
    url = 'http://localhost:8000/api/tts'
    
    payload = {
        'text': text,
        'gender': gender
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f'음성 파일이 {output_file}에 저장되었습니다.')
        return output_file
        
    except requests.exceptions.RequestException as e:
        print(f'TTS 요청 실패: {e}')
        return None

# 사용 예시
text_to_speech('안녕하세요. 반갑습니다.', 'female', 'greeting_female.mp3')
text_to_speech('한국어 공부 화이팅!', 'male', 'encouragement_male.mp3')
```

### React 컴포넌트

```jsx
import React, { useState } from 'react';

const TTSComponent = () => {
  const [text, setText] = useState('');
  const [gender, setGender] = useState('female');
  const [isLoading, setIsLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleTTS = async () => {
    if (!text.trim()) {
      alert('텍스트를 입력해주세요.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/tts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, gender })
      });

      if (!response.ok) {
        throw new Error('TTS 요청 실패');
      }

      const audioBlob = await response.blob();
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (error) {
      console.error('TTS 오류:', error);
      alert('음성 변환에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="음성으로 변환할 텍스트를 입력하세요..."
        rows={4}
        cols={50}
      />
      <br />
      <select value={gender} onChange={(e) => setGender(e.target.value)}>
        <option value="female">여성</option>
        <option value="male">남성</option>
      </select>
      <br />
      <button onClick={handleTTS} disabled={isLoading}>
        {isLoading ? '변환 중...' : '음성 변환'}
      </button>
      
      {audioUrl && (
        <div>
          <audio controls src={audioUrl}>
            브라우저가 오디오를 지원하지 않습니다.
          </audio>
        </div>
      )}
    </div>
  );
};

export default TTSComponent;
```

---

## 에러 처리

### 일반적인 에러 상황

1. **텍스트 누락 (400)**
   ```json
   {
     "detail": "Text is required."
   }
   ```

2. **Google TTS API 오류 (500)**
   ```json
   {
     "detail": "TTS 호출 실패: [구체적인 오류 메시지]"
   }
   ```

3. **오디오 생성 실패 (500)**
   ```json
   {
     "detail": "TTS 결과 오디오 길이가 0입니다."
   }
   ```

### 에러 처리 권장사항

```javascript
async function safeTTS(text, gender = 'female') {
  try {
    const response = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, gender })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return await response.blob();
  } catch (error) {
    console.error('TTS 에러:', error.message);
    
    // 사용자에게 친화적인 에러 메시지 표시
    if (error.message.includes('Text is required')) {
      alert('텍스트를 입력해주세요.');
    } else if (error.message.includes('TTS 호출 실패')) {
      alert('음성 변환 서비스에 일시적인 문제가 있습니다. 잠시 후 다시 시도해주세요.');
    } else {
      alert('알 수 없는 오류가 발생했습니다.');
    }
    
    throw error;
  }
}
```

---

## 제한사항 및 주의사항

### 텍스트 제한
- **최대 길이**: Google TTS API 제한에 따름 (일반적으로 5,000자)
- **지원 언어**: 한국어 (`ko-KR`)
- **특수 문자**: 대부분의 한국어 특수 문자 지원

### 성능 고려사항
- **응답 시간**: 텍스트 길이에 따라 1-10초
- **파일 크기**: 텍스트 길이에 비례하여 증가
- **동시 요청**: 서버 리소스에 따라 제한될 수 있음

### 보안 고려사항
- **API 키**: Google Cloud 서비스 계정 키 필요
- **CORS**: 모든 도메인에서 접근 가능하도록 설정됨
- **인증**: 현재 별도 인증 없이 사용 가능

---

## 기술 스택

- **Backend**: FastAPI
- **TTS Engine**: Google Cloud Text-to-Speech API
- **Audio Format**: MP3
- **Streaming**: FastAPI StreamingResponse
- **Language**: Python 3.x

---

## 문제 해결

### 자주 발생하는 문제

1. **음성이 재생되지 않음**
   - 브라우저의 오디오 정책 확인
   - 사용자 상호작용 후 재생 시도

2. **응답이 느림**
   - 텍스트 길이 확인 (짧게 분할 권장)
   - 네트워크 연결 상태 확인

3. **특정 텍스트에서 오류**
   - 특수 문자나 기호 제거 후 재시도
   - 텍스트 인코딩 확인 (UTF-8)

### 디버깅 팁

```javascript
// 응답 헤더 확인
fetch('/api/tts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: '테스트' })
})
.then(response => {
  console.log('Status:', response.status);
  console.log('Headers:', response.headers);
  console.log('Content-Type:', response.headers.get('content-type'));
  return response.blob();
})
.then(blob => {
  console.log('Blob size:', blob.size);
  console.log('Blob type:', blob.type);
});
```

---

## 업데이트 로그

### v1.0.0 (현재)
- 기본 TTS 기능 구현
- 성별별 음성 선택 지원
- MP3 스트리밍 응답
- 에러 처리 구현

### 향후 계획
- 음성 속도 조절 기능
- 감정/톤 조절 옵션
- 배치 처리 지원
- 캐싱 시스템 도입
- 사용자별 음성 선호도 저장

---

## 지원 및 문의

기술적 문의나 버그 리포트는 개발팀에 문의해주세요.

**API 상태 확인**: `GET /` 엔드포인트로 서버 상태 확인 가능 