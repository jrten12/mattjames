from uuid import uuid4

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


def error_json(status_code: int, code: str, message: str, request_id: str | None = None) -> JSONResponse:
    rid = request_id or f"req_{uuid4().hex[:24]}"
    body = ErrorResponse(error=ErrorDetail(code=code, message=message, request_id=rid))
    return JSONResponse(status_code=status_code, content=body.model_dump())
