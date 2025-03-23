from fastapi import APIRouter
from sdk.api.health_api.health_check import HealthCheck, HealthCheckResult, HealthResponse, HealthStatus
from fastapi import APIRouter
from typing import List
import asyncio


def create_health_router(health_checks: List[HealthCheck]) -> APIRouter:
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse, tags=["Monitoring"])
    async def health():
        available = True
        results = await asyncio.gather(*(hc.run() for hc in health_checks))
        healthy = all(r.status == HealthStatus.SUCCESS for r in results)
        return HealthResponse(available=available, healthy=healthy, healthChecks=results)

    return router

