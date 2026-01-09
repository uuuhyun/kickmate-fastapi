# API ëª…ì„¸??- Spring Backend ??FastAPI

## ê°œìš”

Spring Backend?€ FastAPI ê°„ì˜ ?°ì´???µì‹  ê·œê²©???•ì˜?©ë‹ˆ??

**?µì‹  ë°©ì‹:**
- **?´ë§ ë°©ì‹**: HTTP Polling (Job-based async processing)
- **?¹í›… ë°©ì‹**: FastAPI ??Spring Backend (?‘ì—… ?„ë£Œ ???ë™ POST)
- ??ë°©ì‹???™ì‹œ???¬ìš© ê°€??(?˜ì´ë¸Œë¦¬??

---

## 1. ?´ì„¤ ?ì„± ?”ì²­ (Spring ??FastAPI)

### Endpoint
```
POST /api/commentary/jobs
```

### Request Body
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
    "venue": "DGB?€êµ¬ì??‰íŒŒ??,
    "competitionName": "K League 1",
    "countryName": "KR",
    "seasonName": "2024",
    "homeTeamName": "Daegu FC",
    "homeTeamNameKo": "?€êµ¬FC",
    "homeTeamNameKoShort": "?€êµ?,
    "awayTeamName": "Gimcheon Sangmu",
    "awayTeamNameKo": "ê¹€ì²??ë¬´ ?„ë¡œì¶•êµ¬??,
    "awayTeamNameKoShort": "ê¹€ì²?,
    "audienceNum": "12133",
    "temperature": "9.5Â°C",
    "weather": "ë§‘ìŒ",
    "referee": "ê¹€?€??,
    "assistantReferees": "?¤ì¬??ë°•ê· ??,
    "fourthOfficial": "?¤í˜„ì§?,
    "varReferees": "ê¹€ì¢…í˜,ìµœê·œ??,
    "tsg": "ìµœë¬¸??,
    "homeRank": "1",
    "awayRank": "1",
    "homeTeamUniform": "?˜ëŠ˜???ˆìœ ?ˆí¼",
    "awayTeamUniform": "ë¹¨ê°„???ˆìœ ?ˆí¼"
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
      "typeNameKo": "?¨ìŠ¤",
      "playerNameKo": "?´ì˜ì¤€",
      "teamNameKo": "ê¹€ì²??ë¬´ ?„ë¡œì¶•êµ¬??,
      "teamNameKoShort": "ê¹€ì²?,
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
      "typeNameKo": "?¨ìŠ¤ ë°›ìŒ",
      "playerNameKo": "?ë‘??,
      "teamNameKo": "ê¹€ì²??ë¬´ ?„ë¡œì¶•êµ¬??,
      "teamNameKoShort": "ê¹€ì²?,
      "positionName": "CDM",
      "mainPosition": "CM"
    }
  ]
}
```

### Request ?„ë“œ ?¤ëª…

| ?„ë“œ | ?€??| ?„ìˆ˜ | ?¤ëª… |
|------|------|------|------|
| gameId | string | O | ê²½ê¸° ID |
| style | string | O | ?´ì„¤ ?¤í???("CASTER", "ANALYST", "FRIEND") |
| matchInfo | object | O | ê²½ê¸° ë©”í??°ì´??(1ê°? |
| rawData | array | O | ?´ë²¤???°ì´??(50ê°? |

**Note:**
- Spring??ê²½ê¸° ?°ì´?°ë? 50ê°??¨ìœ„ë¡?ë¶„í• ?˜ì—¬ ?„ì†¡
- FastAPI??S3?ì„œ ?°ì´?°ë? ë¡œë“œ?˜ì? ?ŠìŒ

### Response (ì¦‰ì‹œ ë°˜í™˜)
```json
{
  "jobId": "job_9f2a1c",
  "status": "PENDING"
}
```

| ?„ë“œ | ?€??| ?¤ëª… | ê°€?¥í•œ ê°?|
|------|------|------|----------|
| jobId | string | ?‘ì—… ê³ ìœ  ID (6?ë¦¬ ?œë¤) | "job_9f2a1c" |
| status | string | ?‘ì—… ?íƒœ | "PENDING", "DONE" |

---

## 2. ?‘ì—… ?íƒœ ë°?ê²°ê³¼ ì¡°íšŒ (Spring ??FastAPI)

### Endpoint
```
GET /api/commentary/jobs/{jobId}
```

### Response

#### 2.1. ì²˜ë¦¬ ì¤?(PENDING)
```json
{
  "jobId": "job_9f2a1c",
  "status": "PENDING"
}
```

#### 2.2. ?„ë£Œ (DONE)
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
      "description": "?´ì˜ì¤€ ? ìˆ˜ê°€ ?¨ìŠ¤?©ë‹ˆ??
    },
    {
      "actionId": "1",
      "timeSeconds": "2.433",
      "tone": "DEFAULT",
      "description": "?ë‘??? ìˆ˜ê°€ ë°›ìŠµ?ˆë‹¤"
    },
    {
      "actionId": "2",
      "timeSeconds": "3.033",
      "tone": "EXCITED",
      "description": "?ë‘??? ìˆ˜ê°€ ?„ì§„?©ë‹ˆ??"
    }
  ]
}
```

### Response ?„ë“œ ?¤ëª…

| ?„ë“œ | ?€??| ?¤ëª… |
|------|------|------|
| jobId | string | ?‘ì—… ID |
| status | string | "PENDING" (ì²˜ë¦¬ ì¤? / "DONE" (?„ë£Œ) |
| gameId | string | ê²½ê¸° ID (statusê°€ "DONE"???Œë§Œ) |
| script | array | ?´ì„¤ ë°°ì—´ (statusê°€ "DONE"???Œë§Œ) |
| script[].actionId | string | ?¡ì…˜ ID |
| script[].timeSeconds | string | ê²½ê¸° ?œê°„ (ì´? |
| script[].tone | string | ê°ì • ??|
| script[].description | string | ?´ì„¤ ?ìŠ¤??|

---

## 3. tone ê°??•ì˜

| tone | ?¤ëª… | ?¬ìš© ?í™© |
|------|------|----------|
| DEFAULT | ?¼ë°˜ ?Œë ˆ??| ?¨ìŠ¤, ?œë¦¬ë¸?|
| EXCITED | ?¥ë¶„/?„í—˜ | ?ˆíŒ…, ê³? ê³?ê¸°íšŒ |
| ANGRY | ë¶„ë…¸/??˜ | ?Œìš¸, ë°˜ì¹™ |
| SAD | ?„ì‰¬?€ | ?¤ì±…, ?¤ì  |
| CALM | ì°¨ë¶„??| ?ˆì „ ì§€??ë¹Œë“œ??|
| QUESTION | ?˜ë¬¸ | ë¶ˆí™•?¤í•œ ?í™© |
| EMPHASIS | ê°•ì¡° | ì¤‘ìš”???œê°„ |

**Note:**
- AI ëª¨ë¸??ê°??¡ì…˜??ë§¥ë½??ë¶„ì„?˜ì—¬ tone???ë™?¼ë¡œ ?ì„±
- FastAPI??ë³„ë„??tone ê³„ì‚° ë¡œì§??êµ¬í˜„???„ìš” ?†ìŒ
- tone ??Google TTS ?Œë¼ë¯¸í„° ë§¤í•‘?€ Spring Backend?ì„œ ì²˜ë¦¬

---

## 4. styleë³??´ì„¤ ?¹ì§•

| style | ?¤í???| ë§íˆ¬ | ?ˆì‹œ ?´ì„¤ |
|-------|--------|------|----------|
| CASTER | ìºìŠ¤??| ì¡´ëŒ“ë§? ??™??| "ì¤‘ì›?ì„œ ?°ì¸¡?¼ë¡œ ? ì¹´ë¡œìš´ ?¨ìŠ¤!" |
| ANALYST | ë¶„ì„ê°€ | ì¡´ëŒ“ë§? ì°¨ë¶„ | "52ë¯¸í„° ì§€?ì—???°ì¸¡?¼ë¡œ 16ë¯¸í„° ?„ì§„ ?¨ìŠ¤ë¥??œë„?©ë‹ˆ??" |
| FRIEND | ì¹œêµ¬ | ë°˜ë§, ?¬ìš´ ?œí˜„ | "?? ?´ì˜ì¤€???†ìœ¼ë¡?ê³??˜ê¸°??" |

---

## 5. ?„ì²´ ?Œí¬?Œë¡œ??
### Spring Backend??ì²˜ë¦¬ ?ë¦„

```
1. ?¬ìš©?ê? ê²½ê¸° ? íƒ + style ? íƒ

2. Spring??DB/CSV?ì„œ matchInfo + rawData 50ê°?ë¡œë“œ

3. FastAPI??POST /api/commentary/jobs ?”ì²­
   - gameId, style, matchInfo, rawData[50ê°? ?„ì†¡

4. FastAPI ì¦‰ì‹œ ?‘ë‹µ
   - { jobId, status: "PENDING" }

5. Spring ?´ë§ ?œì‘ (2ì´ˆë§ˆ??
   - GET /api/commentary/jobs/{jobId}

6. FastAPI ë°±ê·¸?¼ìš´???‘ì—…
   - matchInfo + rawData 50ê°œë? ??ë²ˆì— RunPod LLM ?¸ì¶œ
   - 50ê°??´ì„¤ ë°°ì—´ ?ì„±

7. ?„ë£Œ ??Spring??script ë°°ì—´ ?˜ì‹ 
   - { status: "DONE", script: [50ê°? }

8. Spring??ê°?script???€??Google TTS ?¸ì¶œ
   - tone???°ë¼ pitch, speed ì¡°ì •

9. Frontendë¡?WebSocket/SSE ?¤íŠ¸ë¦¬ë°
```

### FastAPI??ì²˜ë¦¬ ë¡œì§

```python
@app.post("/api/commentary/jobs")
async def create_job(request: CommentaryJobRequest, background_tasks: BackgroundTasks):
    # 1. Job ID ?ì„± (6?ë¦¬ ?œë¤)
    job_id = "job_" + generate_random_string(6)

    # 2. Job ?íƒœ ì´ˆê¸°??    job_store[job_id] = {
        "gameId": request.gameId,
        "status": "PENDING",
        "script": []
    }

    # 3. ë°±ê·¸?¼ìš´???‘ì—… ?œì‘
    background_tasks.add_task(generate_commentary_async, job_id, request)

    return {"jobId": job_id, "status": "PENDING"}

async def generate_commentary_async(job_id: str, request: CommentaryJobRequest):
    try:
        # 4. System Prompt ?ì„± (style ë°˜ì˜)
        system_prompt = get_system_prompt(request.style)

        # 5. User Prompt ?ì„± (matchInfo + rawData 50ê°?
        user_prompt = build_user_prompt(
            match_info=request.matchInfo,
            raw_data=request.rawData  # 50ê°??¡ì…˜ ?„ì²´
        )

        # 6. RunPod LLM ?¸ì¶œ (1ë²ˆë§Œ ?¸ì¶œ)
        llm_response = await call_runpod_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        # 7. ?‘ë‹µ ?Œì‹± (50ê°??´ì„¤ ë°°ì—´)
        scripts = json.loads(llm_response)

        # 8. ê²°ê³¼ ?€??        job_store[job_id]["script"] = scripts
        job_store[job_id]["status"] = "DONE"

    except Exception as e:
        job_store[job_id]["status"] = "ERROR"
        job_store[job_id]["error"] = str(e)

@app.get("/api/commentary/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = job_store.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] == "DONE":
        return {
            "gameId": job["gameId"],
            "jobId": job_id,
            "status": "DONE",
            "script": job["script"]
        }
    else:
        return {"jobId": job_id, "status": "PENDING"}
```

---

## 6. ?ëŸ¬ ì²˜ë¦¬

### ?ëŸ¬ ?‘ë‹µ

```json
{
  "jobId": "job_9f2a1c",
  "status": "ERROR",
  "errorCode": "LLM_TIMEOUT",
  "errorMessage": "AI ëª¨ë¸ ?‘ë‹µ ?œê°„ ì´ˆê³¼"
}
```

| errorCode | ?¤ëª… | HTTP Status |
|-----------|------|-------------|
| JOB_NOT_FOUND | jobIdê°€ ì¡´ì¬?˜ì? ?ŠìŒ | 404 |
| INVALID_STYLE | style??"CASTER", "ANALYST", "FRIEND"ê°€ ?„ë‹˜ | 400 |
| INVALID_DATA | matchInfo ?ëŠ” rawData ?•ì‹ ?¤ë¥˜ | 400 |
| LLM_TIMEOUT | LLM ?‘ë‹µ ?œê°„ ì´ˆê³¼ | 500 |
| LLM_ERROR | LLM ?¸ì¶œ ?¤íŒ¨ | 500 |

---

## 7. ?ŒìŠ¤?¸ìš© cURL ëª…ë ¹??
### 7.1. Job ?ì„±
```bash
curl -X POST http://localhost:8000/api/commentary/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "gameId": "126288",
    "style": "CASTER",
    "matchInfo": {
      "gameId": "126288",
      "homeTeamNameKoShort": "?€êµ?,
      "awayTeamNameKoShort": "ê¹€ì²?
    },
    "rawData": [
      {
        "actionId": "0",
        "timeSeconds": "1.033",
        "typeNameKo": "?¨ìŠ¤",
        "playerNameKo": "?´ì˜ì¤€",
        "startX": "52.67",
        "startY": "34.92"
      }
    ]
  }'
```

### 7.2. ?íƒœ ì¡°íšŒ
```bash
curl http://localhost:8000/api/commentary/jobs/job_9f2a1c
```

---

## 8. ?°ì´???€???„ëµ

### Option A: In-memory (ê°œë°œ/?ŒìŠ¤?¸ìš©)
```python
job_store = {}  # FastAPI ?¬ì‹œ?????°ì´???Œì‹¤
```

### Option B: Redis (?´ì˜ ê¶Œì¥)
```python
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# ?€??r.set(f"job:{job_id}", json.dumps(job_data), ex=3600)  # 1?œê°„ TTL

# ì¡°íšŒ
job_data = json.loads(r.get(f"job:{job_id}"))
```

---

## 9. ?±ëŠ¥ ê³ ë ¤?¬í•­

### ì²˜ë¦¬ ?œê°„ ?ˆìƒ
- **50ê°??¡ì…˜ ì²˜ë¦¬:** ??5~10ì´?(ë°°ì¹˜ ì²˜ë¦¬, 7B ëª¨ë¸ ê¸°ì?)
- **LLM ?‘ë‹µ ?œê°„:** 5~10ì´?(50ê°???ë²ˆì— ì²˜ë¦¬)
- **Timeout:** 30ì´?ì´ˆê³¼ ??ê²½ê³ 

### ìµœì ???„ëµ
1. **ë°°ì¹˜ ì²˜ë¦¬:** 50ê°??¡ì…˜????ë²ˆì— LLM???”ì²­ (?„ì¬ ë°©ì‹)
2. **ìºì‹±:** ?™ì¼ ê²½ê¸° ?¬ìš”ì²???ê¸°ì¡´ ê²°ê³¼ ë°˜í™˜
3. **ëª¨ë¸ ìµœì ??** ?‘ë‹µ ?œê°„???ë¦¬ë©?4Bê¸?ëª¨ë¸ë¡??¤ìš´ê·¸ë ˆ?´ë“œ

### ?´ë§ ì£¼ê¸°
- **ê°œë°œ ?˜ê²½:** 5ì´?- **?´ì˜ ?˜ê²½:** 2ì´?
---

## 10. ì¤‘ìš” ?¬í•­

### Spring Backend (?€ ?€??
- [ ] POST `/api/commentary/jobs` ?”ì²­ êµ¬í˜„
- [ ] matchInfo + rawData 50ê°?ì¤€ë¹?- [ ] 2ì´?ì£¼ê¸° ?´ë§ ë¡œì§
- [ ] tone ??Google TTS ?Œë¼ë¯¸í„° ë§¤í•‘
- [ ] WebSocket/SSEë¡?Frontend ?¤íŠ¸ë¦¬ë°

### FastAPI (AI ê°œë°œ??
- [ ] POST `/api/commentary/jobs` ?”ë“œ?¬ì¸??- [ ] GET `/api/commentary/jobs/{jobId}` ?”ë“œ?¬ì¸??- [ ] BackgroundTasksë¡?ë¹„ë™ê¸?ì²˜ë¦¬
- [ ] RunPod LLM ?¸ì¶œ (tone + description ?ì„±)
- [ ] ì¢Œí‘œ ??êµ¬ì—­ ë§¤í•‘ (Zone Mapping)
- [ ] styleë³?System Prompt ?‘ì„±
- [ ] Job ?íƒœ ?€??(Redis or In-memory)

### Filler Content
- **ì²˜ë¦¬ ì£¼ì²´:** Spring Backend
- **?€???„ì¹˜:** RDS
- **AI ê°œë°œ??** ? ê²½ ???„ìš” ?†ìŒ

---

---

## 6. ?¹í›… ë°©ì‹ (? íƒ ?¬í•­)

### ê°œìš”

?´ë§ ë°©ì‹ ?€??FastAPIê°€ ?‘ì—… ?„ë£Œ ??Spring Backend???ë™?¼ë¡œ POST ?”ì²­??ë³´ëƒ…?ˆë‹¤.

**?¥ì :**
- ?¤íŠ¸?Œí¬ ?¸ë˜??ê°ì†Œ (?´ë§ ë¶ˆí•„??
- ì¦‰ê°?ì¸ ?‘ë‹µ (?´ë§ ì£¼ê¸° ?€ê¸??†ìŒ)
- ?œë²„ ë¶€??ê°ì†Œ

### ?¹í›… ?”ë“œ?¬ì¸??(Spring Backend?ì„œ êµ¬í˜„)

```
POST /api/callback/ai-result
```

### ?¹í›… ?˜ì´ë¡œë“œ (FastAPI ??Spring)

**?‘ì—… ?„ë£Œ ??**
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
      "description": "?´ì˜ì¤€ ? ìˆ˜ê°€ ?¨ìŠ¤?©ë‹ˆ??"
    },
    ...
  ]
}
```

**?‘ì—… ?¤íŒ¨ ??**
```json
{
  "jobId": "job_82f395",
  "gameId": "126283",
  "status": "ERROR",
  "errorCode": "LLM_TIMEOUT",
  "errorMessage": "Request timeout after 120 seconds"
}
```

### ?¹í›… ?¤ì • (FastAPI .env)

```bash
# ?¹í›… ?œì„±??(? íƒ ?¬í•­)
SPRING_WEBHOOK_URL=http://ë°±ì•¤??ip:8080/api/callback/ai-result
```

### ?˜ì´ë¸Œë¦¬??ë°©ì‹ (ê¶Œì¥)

?¹í›…ê³??´ë§???™ì‹œ???¬ìš©?˜ì—¬ ?ˆì •???•ë³´:
1. **?¹í›…**: ?•ìƒ ?™ì‘ ??ì¦‰ê° ?‘ë‹µ
2. **?´ë§**: ?¹í›… ?¤íŒ¨ ??ë°±ì—… (5ì´ˆë§ˆ??ìµœë? 3??

---

## ë²„ì „ ?•ë³´
- **Version:** 1.1 (?¹í›… ì§€??ì¶”ê?)
- **?µì‹  ë°©ì‹:** HTTP Polling + Webhook (? íƒ)
- **?°ì´???„ì†¡:** matchInfo 1ê°?+ rawData 50ê°?- **?‘ë‹µ ?„ë“œ:** jobId, status, script[] (tone + description)
- **?œì™¸ ?„ë“œ:** audio_url, threat_level, tts_params, highlighted_terms
- **Last Updated:** 2026-01-07
- **Based on:** API_IO_FORMAT.md
