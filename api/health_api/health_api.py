from fastapi import APIRouter
from sdk.api.health_api.health_check import HealthCheck, HealthCheckResult, HealthResponse, HealthStatus
from fastapi import APIRouter
from typing import List, Optional
import asyncio


def create_health_router(health_checks: Optional[List[HealthCheck]] = None) -> APIRouter:
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse, tags=["Monitoring"])
    async def health():
        available = True
        healthy = False
        results = None

        if (health_checks == None or len(health_checks) == 0):
            healthy = True
        else:
            results = await asyncio.gather(*(hc.run() for hc in health_checks))
            healthy = all(r.status == HealthStatus.SUCCESS for r in results)

        return HealthResponse(available=available, healthy=healthy, healthChecks=results)

    return router

