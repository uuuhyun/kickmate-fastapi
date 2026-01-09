"""
K리그 AI 해설 FastAPI 서버
RunPod Serverless LLM과 통신하여 실시간 해설 생성

Version: 1.0
Usage: uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 환경 변수 로드
load_dotenv()

from .routers import commentary


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 생명주기 관리"""
    # 시작 시
    print("=" * 60)
    print("K리그 AI 해설 서버 시작")
    print("=" * 60)

    # RunPod 설정 확인
    runpod_key = os.getenv("RUNPOD_API_KEY", "")
    runpod_url = os.getenv("RUNPOD_ENDPOINT_URL", "")

    if runpod_key:
        print(f"RUNPOD_API_KEY: {runpod_key[:10]}...{runpod_key[-4:]}")
    else:
        print("WARNING: RUNPOD_API_KEY not set")

    if runpod_url:
        print(f"RUNPOD_ENDPOINT_URL: {runpod_url}")
    else:
        print("WARNING: RUNPOD_ENDPOINT_URL not set")

    print("=" * 60)

    yield

    # 종료 시
    print("K리그 AI 해설 서버 종료")


app = FastAPI(
    title="K리그 AI 해설 API",
    description="""
K리그 실시간 AI 해설 서비스의 FastAPI 백엔드

## 기능
- **해설 생성**: matchInfo와 rawData를 받아 AI 해설 생성
- **작업 조회**: 폴링 방식으로 작업 상태 및 결과 조회

## 스타일
- **CASTER**: 역동적, 빠른 템포
- **ANALYST**: 차분, 분석적
- **FRIEND**: 친근, 쉬운 표현

## 통신 방식
Spring Backend에서 2초마다 폴링하여 결과 수신
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(commentary.router)


@app.get("/", tags=["health"])
async def root():
    """서버 상태 확인"""
    return {
        "service": "K리그 AI 해설 API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """헬스 체크"""
    runpod_configured = bool(
        os.getenv("RUNPOD_API_KEY") and os.getenv("RUNPOD_ENDPOINT_URL")
    )

    return {
        "status": "healthy",
        "runpod_configured": runpod_configured
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
