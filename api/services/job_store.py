"""
Job 저장소 서비스
In-memory 기반 작업 상태 관리 (개발/테스트용)

Version: 1.0
"""

import uuid
import asyncio
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum


class JobStatus(str, Enum):
    """작업 상태"""
    PENDING = "PENDING"
    DONE = "DONE"
    ERROR = "ERROR"


class JobData:
    """작업 데이터 클래스"""

    def __init__(self, game_id: str, style: str):
        self.game_id = game_id
        self.style = style
        self.status = JobStatus.PENDING
        self.script: List[dict] = []
        self.error_code: Optional[str] = None
        self.error_message: Optional[str] = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "gameId": self.game_id,
            "style": self.style,
            "status": self.status.value,
            "script": self.script,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


class JobStore:
    """In-memory Job 저장소"""

    def __init__(self):
        self._jobs: Dict[str, JobData] = {}
        self._lock = asyncio.Lock()

    def generate_job_id(self) -> str:
        """고유 Job ID 생성"""
        return f"job_{uuid.uuid4().hex[:6]}"

    async def create_job(self, game_id: str, style: str) -> str:
        """
        새 작업 생성

        Args:
            game_id: 경기 ID
            style: 해설 스타일

        Returns:
            생성된 Job ID
        """
        async with self._lock:
            job_id = self.generate_job_id()
            self._jobs[job_id] = JobData(game_id, style)
            return job_id

    async def get_job(self, job_id: str) -> Optional[JobData]:
        """
        작업 조회

        Args:
            job_id: Job ID

        Returns:
            JobData 또는 None
        """
        return self._jobs.get(job_id)

    async def update_job_done(self, job_id: str, script: List[dict]) -> bool:
        """
        작업 완료 상태로 업데이트

        Args:
            job_id: Job ID
            script: 해설 스크립트 배열

        Returns:
            성공 여부
        """
        async with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.status = JobStatus.DONE
                job.script = script
                job.updated_at = datetime.now()
                return True
            return False

    async def update_job_error(
        self,
        job_id: str,
        error_code: str,
        error_message: str
    ) -> bool:
        """
        작업 오류 상태로 업데이트

        Args:
            job_id: Job ID
            error_code: 에러 코드
            error_message: 에러 메시지

        Returns:
            성공 여부
        """
        async with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.status = JobStatus.ERROR
                job.error_code = error_code
                job.error_message = error_message
                job.updated_at = datetime.now()
                return True
            return False

    async def delete_job(self, job_id: str) -> bool:
        """
        작업 삭제

        Args:
            job_id: Job ID

        Returns:
            성공 여부
        """
        async with self._lock:
            if job_id in self._jobs:
                del self._jobs[job_id]
                return True
            return False

    async def list_jobs(self) -> Dict[str, dict]:
        """모든 작업 목록 반환"""
        return {
            job_id: job.to_dict()
            for job_id, job in self._jobs.items()
        }

    async def cleanup_old_jobs(self, max_age_hours: int = 1) -> int:
        """
        오래된 작업 정리

        Args:
            max_age_hours: 최대 보관 시간 (시간)

        Returns:
            삭제된 작업 수
        """
        from datetime import timedelta

        async with self._lock:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            old_jobs = [
                job_id for job_id, job in self._jobs.items()
                if job.created_at < cutoff
            ]
            for job_id in old_jobs:
                del self._jobs[job_id]
            return len(old_jobs)


# 싱글톤 인스턴스
_job_store: Optional[JobStore] = None


def get_job_store() -> JobStore:
    """Job Store 인스턴스 반환"""
    global _job_store
    if _job_store is None:
        _job_store = JobStore()
    return _job_store
