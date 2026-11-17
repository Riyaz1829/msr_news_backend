
from typing import Any, Optional

from pydantic import BaseModel


class APIError(BaseModel):
    code: str
    message: Optional[str] = None
    retry_after_seconds: Optional[int] = None


class PaginationMeta(BaseModel):
    page: int = 1
    limit: int = 20


class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    meta: Optional[PaginationMeta] = None
    error: Optional[APIError] = None
