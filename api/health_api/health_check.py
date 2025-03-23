from enum import Enum
from typing import Callable, Awaitable, List
from pydantic import BaseModel
import asyncio

# Enum to represent health check status
class HealthStatus(str, Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    TIMEOUT = "Timeout"

# Response schema for each check
class HealthCheckResult(BaseModel):
    title: str
    status: HealthStatus

# Full health check response
class HealthResponse(BaseModel):
    available: bool
    healthy: bool
    healthChecks: List[HealthCheckResult]

class HealthCheck:
    def __init__(self, title: str, check_fn: Callable[[], Awaitable[bool]], timeout: float = 2.0):
        self.title = title
        self.check_fn = check_fn
        self.timeout = timeout

    async def run(self) -> HealthCheckResult:
        try:
            result = await asyncio.wait_for(self.check_fn(), timeout=self.timeout)
            return HealthCheckResult(title=self.title, status=HealthStatus.SUCCESS if result else HealthStatus.FAILED)
        except asyncio.TimeoutError:
            return HealthCheckResult(title=self.title, status=HealthStatus.TIMEOUT)
        except Exception:
            return HealthCheckResult(title=self.title, status=HealthStatus.FAILED)