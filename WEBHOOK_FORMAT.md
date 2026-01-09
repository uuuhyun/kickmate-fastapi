# 웹훅 JSON 형식

FastAPI가 Spring Backend로 전송하는 웹훅 페이로드 명세입니다.

## 📍 웹훅 엔드포인트

```
POST http://백앤드-ip:8080/api/callback/ai-result
Content-Type: application/json
```

---

## ✅ 작업 완료 시 (status: "DONE")

```json
{
  "jobId": "job_82f395",
  "gameId": "126283",
  "status": "DONE",
  "script": [
    {
      "actionId": "0",
      "timeSeconds": "1.033",
      "tone": "DEFAULT",
      "description": "이영준 선수가 패스합니다."
    },
    {
      "actionId": "1",
      "timeSeconds": "2.433",
      "tone": "DEFAULT",
      "description": "원두재 선수가 받습니다."
    },
    {
      "actionId": "2",
      "timeSeconds": "3.033",
      "tone": "EXCITED",
      "description": "원두재 선수가 전방으로 강하게 패스합니다!"
    }
  ]
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `jobId` | string | 작업 ID |
| `gameId` | string | 경기 ID |
| `status` | string | "DONE" (고정값) |
| `script` | array | 해설 배열 (입력한 rawData 개수만큼 반환) |

### script 배열 항목

| 필드 | 타입 | 설명 |
|------|------|------|
| `actionId` | string | 액션 ID |
| `timeSeconds` | string | 경기 시간(초) |
| `tone` | string | 감정 톤 |
| `description` | string | 해설 텍스트 |

### tone 값 종류

| tone 값 | 의미 | 사용 상황 |
|---------|------|----------|
| `DEFAULT` | 일반 | 패스, 드리블 등 일반 플레이 |
| `EXCITED` | 흥분/위험 | 슈팅, 골, 골 기회 |
| `ANGRY` | 분노/항의 | 파울, 반칙 |
| `SAD` | 아쉬움 | 실책, 실점 |
| `CALM` | 차분함 | 안전 지역 빌드업 |
| `QUESTION` | 의문 | 불확실한 상황 |
| `EMPHASIS` | 강조 | 중요한 순간 |

---

## ❌ 작업 실패 시 (status: "ERROR")

```json
{
  "jobId": "job_82f395",
  "gameId": "126283",
  "status": "ERROR",
  "errorCode": "LLM_TIMEOUT",
  "errorMessage": "Request timeout after 120 seconds"
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `jobId` | string | 작업 ID |
| `gameId` | string | 경기 ID |
| `status` | string | "ERROR" (고정값) |
| `errorCode` | string | 에러 코드 |
| `errorMessage` | string | 에러 상세 메시지 |

### errorCode 종류

| 코드 | 의미 |
|------|------|
| `LLM_TIMEOUT` | RunPod API 타임아웃 (120초 초과) |
| `LLM_ERROR` | LLM 호출 실패 (기타 에러) |

---

## 🔧 Spring Backend DTO 예시

### WebhookPayload.java

```java
package com.example.dto;

import lombok.Getter;
import lombok.Setter;
import java.util.List;

@Getter
@Setter
public class WebhookPayload {
    private String jobId;
    private String gameId;
    private String status;  // "DONE" or "ERROR"

    // 성공 시
    private List<ScriptItem> script;

    // 실패 시
    private String errorCode;
    private String errorMessage;
}
```

### ScriptItem.java

```java
package com.example.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ScriptItem {
    private String actionId;
    private String timeSeconds;
    private String tone;
    private String description;
}
```

---

## 📝 Spring Backend 컨트롤러 예시

```java
package com.example.controller;

import com.example.dto.WebhookPayload;
import com.example.dto.ScriptItem;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/callback")
public class WebhookController {

    @PostMapping("/ai-result")
    public ResponseEntity<Void> receiveCommentary(@RequestBody WebhookPayload payload) {
        log.info("웹훅 수신: jobId={}, gameId={}, status={}",
                 payload.getJobId(), payload.getGameId(), payload.getStatus());

        if ("DONE".equals(payload.getStatus())) {
            // 성공 처리
            List<ScriptItem> scripts = payload.getScript();
            log.info("해설 생성 완료: {} 개", scripts.size());

            // 비즈니스 로직 처리
            // 예: 데이터베이스 저장, 프론트엔드로 WebSocket 전송 등
            for (ScriptItem script : scripts) {
                log.debug("actionId={}, tone={}, description={}",
                         script.getActionId(), script.getTone(), script.getDescription());
            }

        } else if ("ERROR".equals(payload.getStatus())) {
            // 에러 처리
            String errorCode = payload.getErrorCode();
            String errorMessage = payload.getErrorMessage();
            log.error("AI 해설 생성 실패: errorCode={}, message={}",
                     errorCode, errorMessage);

            // 에러 처리 로직
            // 예: 재시도, 사용자 알림 등
        }

        return ResponseEntity.ok().build();
    }
}
```

---

## 🔐 보안 고려사항

### 1. IP 화이트리스트
FastAPI 서버의 IP만 허용하도록 설정:

```java
@PostMapping("/ai-result")
public ResponseEntity<Void> receiveCommentary(
    @RequestBody WebhookPayload payload,
    HttpServletRequest request) {

    String clientIp = request.getRemoteAddr();
    if (!isAllowedIp(clientIp)) {
        log.warn("허용되지 않은 IP에서 웹훅 요청: {}", clientIp);
        return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
    }

    // ... 처리 로직
}
```

### 2. 인증 토큰 (선택 사항)
공유 시크릿 토큰으로 요청 검증:

```java
@PostMapping("/ai-result")
public ResponseEntity<Void> receiveCommentary(
    @RequestBody WebhookPayload payload,
    @RequestHeader("X-Webhook-Token") String token) {

    if (!isValidToken(token)) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
    }

    // ... 처리 로직
}
```

---

## 🧪 테스트 방법

### 1. 로컬 테스트 (FastAPI와 Spring 모두 로컬)

```bash
# .env 파일
SPRING_WEBHOOK_URL=http://localhost:8080/api/callback/ai-result
```

### 2. 실제 서버 테스트

```bash
# .env 파일
SPRING_WEBHOOK_URL=http://10.0.1.100:8080/api/callback/ai-result
```

### 3. ngrok을 이용한 로컬 테스트

```bash
# Spring Backend를 ngrok으로 외부 노출
ngrok http 8080

# .env 파일
SPRING_WEBHOOK_URL=https://abc123.ngrok.io/api/callback/ai-result
```

---

## 📊 웹훅 vs 폴링 비교

| 항목 | 폴링 방식 | 웹훅 방식 |
|------|----------|----------|
| 응답 속도 | 최대 2초 대기 | 즉시 전송 |
| 네트워크 트래픽 | 많음 (2초마다 요청) | 적음 (1회 전송) |
| 서버 부하 | 높음 | 낮음 |
| 구현 난이도 | 쉬움 | 중간 |
| 안정성 | 높음 (재시도 가능) | 중간 (네트워크 오류 시 실패) |

**권장 방식**: 웹훅 + 폴링 하이브리드
- 웹훅을 우선 사용하여 즉각 응답
- 웹훅 실패 시 폴링으로 백업 (5초 간격, 최대 3회)

---

## 🔍 디버깅

### FastAPI 로그 확인

```bash
# 웹훅 전송 성공
[WEBHOOK] 웹훅 전송 성공: job_xxx -> http://10.0.1.100:8080/api/callback/ai-result

# 웹훅 URL 미설정
[WEBHOOK] 웹훅 URL이 설정되지 않았습니다. 웹훅 전송을 건너뜁니다.

# 웹훅 전송 실패
[WEBHOOK] 웹훅 전송 실패 (Spring 서버가 꺼져있나요?): Connection refused
```

### Spring Backend 로그 확인

```bash
# 성공
웹훅 수신: jobId=job_xxx, gameId=126283, status=DONE
해설 생성 완료: 50 개

# 실패
AI 해설 생성 실패: errorCode=LLM_TIMEOUT, message=Request timeout after 120 seconds
```

---

**작성일**: 2026-01-07
**버전**: 1.0
**관련 문서**: [README.md](README.md), [API_SPEC.md](API_SPEC.md)
