"""
Pydantic 스키마 정의
Spring Backend <-> FastAPI 통신용 데이터 모델

Version: 1.2
- Dict 기반 유연한 스키마로 변경
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum


class StyleEnum(str, Enum):
    """해설 스타일"""
    CASTER = "CASTER"
    ANALYST = "ANALYST"
    FRIEND = "FRIEND"


class ToneEnum(str, Enum):
    """감정 톤"""
    DEFAULT = "DEFAULT"
    EXCITED = "EXCITED"
    ANGRY = "ANGRY"
    SAD = "SAD"
    CALM = "CALM"
    QUESTION = "QUESTION"
    EMPHASIS = "EMPHASIS"


class JobStatusEnum(str, Enum):
    """작업 상태"""
    PENDING = "PENDING"
    DONE = "DONE"
    ERROR = "ERROR"


# =============================================================================
# 요청 모델 (유연한 Dict 기반)
# =============================================================================

class CommentaryJobRequest(BaseModel):
    """해설 생성 요청 - 유연한 입력 처리"""
    gameId: str = Field(...)
    style: StyleEnum
    matchInfo: Dict[str, Any]  # 유연하게 모든 필드 허용
    rawData: List[Dict[str, Any]]  # 유연하게 모든 필드 허용

    class Config:
        extra = "allow"


# =============================================================================
# 응답 모델
# =============================================================================

class ScriptItem(BaseModel):
    """해설 스크립트 항목"""
    actionId: str
    timeSeconds: str
    tone: ToneEnum
    description: str


class JobPendingResponse(BaseModel):
    """작업 대기중 응답"""
    jobId: str
    status: JobStatusEnum = JobStatusEnum.PENDING


class JobDoneResponse(BaseModel):
    """작업 완료 응답"""
    gameId: str
    jobId: str
    status: JobStatusEnum = JobStatusEnum.DONE
    script: List[ScriptItem]


class JobErrorResponse(BaseModel):
    """작업 오류 응답"""
    jobId: str
    status: JobStatusEnum = JobStatusEnum.ERROR
    errorCode: str
    errorMessage: str


# =============================================================================
# RunPod 통신용 모델
# =============================================================================

class RunPodRequest(BaseModel):
    """RunPod Serverless 요청"""
    input: dict


class RunPodResponse(BaseModel):
    """RunPod Serverless 응답"""
    id: Optional[str] = None
    status: Optional[str] = None
    output: Optional[dict] = None
    error: Optional[str] = None
