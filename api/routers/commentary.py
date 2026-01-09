"""
해설 생성 API 라우터
POST /ai/commentary/jobs - 해설 생성 요청
GET /ai/commentary/jobs/{jobId} - 작업 상태 조회

Version: 1.1 (웹훅 지원 추가)
"""

import os
import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Union

from ..models.schemas import (
    CommentaryJobRequest,
    JobPendingResponse,
    JobDoneResponse,
    JobErrorResponse,
    ScriptItem,
    ToneEnum,
    JobStatusEnum
)
from ..services.job_store import get_job_store, JobStatus
from ..services.runpod_service import get_runpod_service

# 웹훅 URL (환경 변수에서 로드, 선택 사항)
WEBHOOK_URL = os.getenv("SPRING_WEBHOOK_URL", "")

router = APIRouter(prefix="/ai/commentary", tags=["commentary"])


async def send_webhook(
    job_id: str,
    game_id: str,
    status: str,
    script: list = None,
    error_code: str = None,
    error_message: str = None
):
    """
    Spring Backend로 웹훅 전송

    Args:
        job_id: Job ID
        game_id: 경기 ID (문자열)
        status: "DONE" 또는 "ERROR"
        script: 생성된 해설 배열 (성공 시)
        error_code: 에러 코드 (실패 시)
        error_message: 에러 메시지 (실패 시)
    """
    if not WEBHOOK_URL:
        print(f"[WEBHOOK] 웹훅 URL이 설정되지 않았습니다. 웹훅 전송을 건너뜁니다.")
        return

    try:
        # 웹훅 페이로드 구성
        callback_data = {
            "jobId": job_id,
            "gameId": game_id,
            "status": status
        }

        if status == "DONE" and script:
            callback_data["script"] = script
        elif status == "ERROR":
            callback_data["errorCode"] = error_code
            callback_data["errorMessage"] = error_message

        # 웹훅 전송
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(WEBHOOK_URL, json=callback_data)

            if response.status_code == 200:
                print(f"[WEBHOOK] 웹훅 전송 성공: {job_id} -> {WEBHOOK_URL}")
            else:
                print(f"[WEBHOOK] 웹훅 응답 오류: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[WEBHOOK] 웹훅 전송 실패 (Spring 서버가 꺼져있나요?): {e}")


async def generate_commentary_task(
    job_id: str,
    request: CommentaryJobRequest
):
    """
    백그라운드 해설 생성 태스크

    Args:
        job_id: Job ID
        request: 해설 생성 요청
    """
    print(f"[DEBUG] Background task started for job {job_id}")
    job_store = get_job_store()
    runpod_service = get_runpod_service()

    try:
        # matchInfo와 rawData는 이미 dict 형태
        match_info_dict = request.matchInfo
        raw_data_list = request.rawData

        print(f"[DEBUG] Calling RunPod LLM for {len(raw_data_list)} actions...")

        # RunPod LLM 호출
        scripts = await runpod_service.call_llm(
            style=request.style.value,
            match_info=match_info_dict,
            raw_data=raw_data_list
        )

        print(f"[DEBUG] LLM returned {len(scripts)} scripts")

        # 작업 완료 업데이트
        await job_store.update_job_done(job_id, scripts)

        print(f"Job {job_id} completed with {len(scripts)} scripts")

        # [웹훅] Spring Backend로 완료 알림 전송
        await send_webhook(
            job_id=job_id,
            game_id=request.gameId,
            status="DONE",
            script=scripts
        )

    except Exception as e:
        # 작업 오류 업데이트
        error_message = str(e)

        print(f"[DEBUG] Error in background task: {error_message}")
        import traceback
        traceback.print_exc()

        if "timeout" in error_message.lower():
            error_code = "LLM_TIMEOUT"
        else:
            error_code = "LLM_ERROR"

        await job_store.update_job_error(job_id, error_code, error_message)
        print(f"Job {job_id} failed: {error_code} - {error_message}")

        # [웹훅] Spring Backend로 실패 알림 전송
        await send_webhook(
            job_id=job_id,
            game_id=request.gameId,
            status="ERROR",
            error_code=error_code,
            error_message=error_message
        )


@router.post(
    "/jobs",
    response_model=JobPendingResponse,
    summary="해설 생성 요청",
    description="matchInfo와 rawData를 받아 AI 해설 생성 작업을 시작합니다."
)
async def create_commentary_job(
    request: CommentaryJobRequest,
    background_tasks: BackgroundTasks
):
    """
    해설 생성 작업 생성

    - matchInfo: 경기 메타데이터 (1개)
    - rawData: 이벤트 로그 데이터 (10개)
    - style: CASTER, ANALYST, FRIEND
    """
    print(f"\n{'='*60}")
    print(f"[REQUEST] 해설 생성 요청 수신")
    print(f"[REQUEST] gameId: {request.gameId}, style: {request.style.value}")
    print(f"[REQUEST] rawData 개수: {len(request.rawData) if request.rawData else 0}개")
    print(f"{'='*60}\n")

    job_store = get_job_store()

    # 유효성 검사
    if not request.rawData:
        raise HTTPException(
            status_code=400,
            detail={
                "errorCode": "INVALID_DATA",
                "errorMessage": "rawData는 비어있을 수 없습니다."
            }
        )

    if len(request.rawData) > 20:
        raise HTTPException(
            status_code=400,
            detail={
                "errorCode": "INVALID_DATA",
                "errorMessage": "rawData는 20개를 초과할 수 없습니다."
            }
        )

    # Job 생성
    job_id = await job_store.create_job(
        game_id=request.gameId,
        style=request.style.value
    )
    print(f"[JOB] Job ID 생성 완료: {job_id}")

    # 백그라운드 태스크 시작
    background_tasks.add_task(
        generate_commentary_task,
        job_id,
        request
    )
    print(f"[JOB] 백그라운드 태스크 시작: {job_id}\n")

    return JobPendingResponse(jobId=job_id, status=JobStatusEnum.PENDING)


@router.get(
    "/jobs/{job_id}",
    response_model=Union[JobPendingResponse, JobDoneResponse, JobErrorResponse],
    summary="작업 상태 조회",
    description="Job ID로 작업 상태 및 결과를 조회합니다."
)
async def get_job_status(job_id: str):
    """
    작업 상태 조회

    - PENDING: 처리 중
    - DONE: 완료 (script 배열 포함)
    - ERROR: 오류 발생
    """
    print(f"[POLLING] Job 상태 조회: {job_id}")
    job_store = get_job_store()
    job = await job_store.get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail={
                "errorCode": "JOB_NOT_FOUND",
                "errorMessage": f"Job {job_id}를 찾을 수 없습니다."
            }
        )

    if job.status == JobStatus.PENDING:
        print(f"[POLLING] {job_id} - 상태: PENDING (처리 중)")
        return JobPendingResponse(jobId=job_id, status=JobStatusEnum.PENDING)

    elif job.status == JobStatus.DONE:
        print(f"[POLLING] {job_id} - 상태: DONE (완료, script {len(job.script)}개)")
        # script 항목을 ScriptItem으로 변환
        script_items = []
        for s in job.script:
            try:
                tone = ToneEnum(s.get("tone", "DEFAULT"))
            except ValueError:
                tone = ToneEnum.DEFAULT

            script_items.append(ScriptItem(
                actionId=str(s.get("actionId", "")),
                timeSeconds=str(s.get("timeSeconds", "")),
                tone=tone,
                description=str(s.get("description", ""))
            ))

        return JobDoneResponse(
            gameId=job.game_id,
            jobId=job_id,
            status=JobStatusEnum.DONE,
            script=script_items
        )

    else:  # ERROR
        print(f"[POLLING] {job_id} - 상태: ERROR ({job.error_code})")
        return JobErrorResponse(
            jobId=job_id,
            status=JobStatusEnum.ERROR,
            errorCode=job.error_code or "UNKNOWN_ERROR",
            errorMessage=job.error_message or "알 수 없는 오류가 발생했습니다."
        )


@router.get(
    "/jobs",
    summary="모든 작업 목록 조회",
    description="현재 저장된 모든 작업 목록을 조회합니다. (디버깅용)"
)
async def list_jobs():
    """모든 작업 목록 반환 (디버깅용)"""
    job_store = get_job_store()
    jobs = await job_store.list_jobs()
    return {"jobs": jobs, "count": len(jobs)}


@router.delete(
    "/jobs/{job_id}",
    summary="작업 삭제",
    description="Job ID로 작업을 삭제합니다."
)
async def delete_job(job_id: str):
    """작업 삭제"""
    job_store = get_job_store()
    deleted = await job_store.delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "errorCode": "JOB_NOT_FOUND",
                "errorMessage": f"Job {job_id}를 찾을 수 없습니다."
            }
        )

    return {"message": f"Job {job_id} 삭제 완료"}
