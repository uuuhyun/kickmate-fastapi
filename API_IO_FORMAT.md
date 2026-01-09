# API 입출력 형식 (Spring ↔ FastAPI)

## 백엔드 → FastAPI 입력

```json
{
  "gameId": "126288",
  "style": "CASTER",
  "matchInfo": {
    "gameId": "126288",
    "seasonId": "3669",
    "competitionId": "587",
    "gameDay": "1",
    "gameDate": "2024-03-03 14:00:00",
    "homeTeamId": "4644",
    "awayTeamId": "2353",
    "homeScore": "0",
    "awayScore": "1",
    "venue": "DGB대구은행파크",
    "competitionName": "K League 1",
    "countryName": "KR",
    "seasonName": "2024",
    "homeTeamName": "Daegu FC",
    "homeTeamNameKo": "대구FC",
    "homeTeamNameKoShort": "대구",
    "awayTeamName": "Gimcheon Sangmu",
    "awayTeamNameKo": "김천 상무 프로축구단",
    "awayTeamNameKoShort": "김천",
    "audienceNum": "12133",
    "temperature": "9.5°C",
    "weather": "맑음",
    "referee": "김대용",
    "assistantReferees": "윤재열,박균용",
    "fourthOfficial": "오현진",
    "varReferees": "김종혁,최규현",
    "tsg": "최문식",
    "homeRank": "1",
    "awayRank": "1",
    "homeTeamUniform": "하늘색 홈유니폼",
    "awayTeamUniform": "빨간색 홈유니폼"
  },
  "rawData": [
    {
      "gameId": "126288",
      "actionId": "0",
      "periodId": "1",
      "timeSeconds": "1.033",
      "teamId": "2353",
      "playerId": "356625.0",
      "resultName": "Successful",
      "startX": "52.670205",
      "startY": "34.919632",
      "endX": "68.628945",
      "endY": "34.347412",
      "dx": "15.95874",
      "dy": "-0.57222",
      "typeName": "Pass",
      "typeNameKo": "패스",
      "playerNameKo": "이영준",
      "teamNameKo": "김천 상무 프로축구단",
      "teamNameKoShort": "김천",
      "positionName": "CF",
      "mainPosition": "CF"
    },
    {
      "gameId": "126288",
      "actionId": "1",
      "periodId": "1",
      "timeSeconds": "2.433",
      "teamId": "2353",
      "playerId": "356612.0",
      "resultName": "",
      "startX": "68.628945",
      "startY": "34.347412",
      "endX": "68.628945",
      "endY": "34.347412",
      "dx": "0.0",
      "dy": "0.0",
      "typeName": "Pass Received",
      "typeNameKo": "패스 받음",
      "playerNameKo": "원두재",
      "teamNameKo": "김천 상무 프로축구단",
      "teamNameKoShort": "김천",
      "positionName": "CDM",
      "mainPosition": "CM"
    },
    {
      "gameId": "126288",
      "actionId": "2",
      "periodId": "1",
      "timeSeconds": "3.033",
      "teamId": "2353",
      "playerId": "356612.0",
      "resultName": "Successful",
      "startX": "68.228055",
      "startY": "33.853256",
      "endX": "65.468865",
      "endY": "26.640292",
      "dx": "-2.75919",
      "dy": "-7.212964",
      "typeName": "Pass",
      "typeNameKo": "패스",
      "playerNameKo": "원두재",
      "teamNameKo": "김천 상무 프로축구단",
      "teamNameKoShort": "김천",
      "positionName": "CDM",
      "mainPosition": "CM"
    }
  ]
}
```

**설명:**
- `gameId`: 경기 ID
- `style`: "CASTER", "ANALYST", "FRIEND"
- `matchInfo`: 경기 메타데이터 1개 (CSV의 1행)
- `rawData`: 이벤트 데이터 50개 행 (위 예시는 3개만 표시, 실제로는 50개)
  - **주의**: Spring Backend가 `id` 필드(DB PK)를 첫 번째 필드로 추가해도 무방합니다
  - FastAPI는 LLM 전송 시 필요한 필드만 선택적으로 추출하므로 `id` 필드는 자동으로 무시됩니다

---

## AI 모델 자체 출력

FastAPI가 RunPod LLM을 **1번 호출**하여 받는 **50개 해설 배열**:

```json
[
  {
    "gameId": "126288",
    "actionId": "0",
    "timeSeconds": "1.033",
    "tone": "DEFAULT",
    "description": "이영준 선수가 패스합니다"
  },
  {
    "gameId": "126288",
    "actionId": "1",
    "timeSeconds": "2.433",
    "tone": "DEFAULT",
    "description": "원두재 선수가 받습니다"
  },
  {
    "gameId": "126288",
    "actionId": "2",
    "timeSeconds": "3.033",
    "tone": "DEFAULT",
    "description": "원두재 선수가 패스합니다"
  },
  ...47개 더...
]
```

**설명:**
- AI 모델은 **50개 액션을 한 번에 입력받아 50개 해설 배열을 반환**
- 입력: matchInfo 1개 + rawData 50개
- 출력: 50개 해설 객체 배열 (1번의 LLM 호출)

---

## FastAPI → 백엔드 응답

### 응답 필드 정의

| 필드 | 타입 | 설명 |
|------|------|------|
| jobId | string | AI 작업 식별자 (예: "job_9f2a1c") |
| status | string | "PENDING" (처리 중) / "DONE" (완료) |
| gameId | string | 경기 ID (status가 "DONE"일 때만) |
| script | array | 해설 배열 (status가 "DONE"일 때만) |

---

### FastAPI → 백엔드 (AI 답변 생성 중일 때)

```json
{
  "jobId": "job_9f2a1c",
  "status": "PENDING"
}
```

---

### FastAPI → 백엔드 (AI 답변 생성 완료 시)

```json
{
  "gameId": "126288",
  "jobId": "job_9f2a1c",
  "status": "DONE",
  "script": [
    {
      "actionId": "0",
      "timeSeconds": "1.033",
      "tone": "DEFAULT",
      "description": "이영준 선수가 패스합니다"
    },
    {
      "actionId": "1",
      "timeSeconds": "2.433",
      "tone": "DEFAULT",
      "description": "원두재 선수가 받습니다"
    },
    {
      "actionId": "2",
      "timeSeconds": "3.033",
      "tone": "ANGRY",
      "description": "원두재 선수가 패스합니다"
    },
    {
      "actionId": "3",
      "timeSeconds": "4.333",
      "tone": "DEFAULT",
      "description": "김진규 선수가 받습니다"
    },
    {
      "actionId": "4",
      "timeSeconds": "4.9",
      "tone": "DEFAULT",
      "description": "김진규 선수가 패스합니다"
    },
    {
      "actionId": "5",
      "timeSeconds": "6.3",
      "tone": "DEFAULT",
      "description": "강현묵 선수가 받습니다"
    },
    {
      "actionId": "6",
      "timeSeconds": "6.301",
      "tone": "DEFAULT",
      "description": "강현묵 선수가 드리블합니다"
    },
    {
      "actionId": "7",
      "timeSeconds": "10.114",
      "tone": "DEFAULT",
      "description": "강현묵 선수가 패스합니다"
    },
    {
      "actionId": "8",
      "timeSeconds": "11.467",
      "tone": "DEFAULT",
      "description": "원두재 선수가 받습니다"
    }
  ]
}
```

**설명:**
- `script` 배열의 길이 = 입력받은 `rawData` 배열 길이 (50개)
- 각 `actionId`는 입력 데이터의 `actionId`와 일치

---

## tone 값 종류 (AI 모델이 자동 생성)

| tone | 사용 상황 |
|------|----------|
| DEFAULT | 일반 플레이 (패스, 드리블) |
| EXCITED | 골, 슈팅, 골 기회 |
| ANGRY | 파울, 반칙, 항의 |
| SAD | 실책, 실점, 아쉬운 상황 |
| CALM | 안전 지역 빌드업 |
| QUESTION | 의문, 불확실한 상황 |
| EMPHASIS | 강조, 중요한 순간 |

**참고:**
- AI 모델이 각 액션의 맥락을 분석하여 적절한 tone을 자동으로 선택
- 별도의 tone 계산 로직은 FastAPI에서 구현할 필요 없음

---

## 전체 흐름 요약

```
1. Spring → FastAPI 요청
   POST /api/commentary/jobs
   { matchInfo(1개) + rawData(50개) + style }

2. FastAPI 즉시 응답
   { "jobId": "job_xxx", "status": "PENDING" }

3. FastAPI 백그라운드 작업
   - matchInfo + rawData 50개를 한 번에 AI 모델 호출 (1회)
   - 50개 해설 배열 생성 (gameId, actionId, timeSeconds, tone, description)

4. Spring 폴링 (2초마다)
   GET /api/commentary/jobs/job_xxx

5. 완료 후 응답
   { "status": "DONE", "script": [50개 해설 배열] }
```

---

**문서 버전:** 1.0
**작성일:** 2026-01-04
**데이터 출처:** match_info_final_with_ko_short.csv, raw_data_with_short.csv
