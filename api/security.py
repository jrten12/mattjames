from hashlib import sha256

from fastapi import Request

from api.config import Settings
from api.models.common import error_json


def request_content_length_too_large(request: Request, settings: Settings) -> bool:
    content_length = request.headers.get("content-length")
    if content_length is None:
        return False
    try:
        return int(content_length) > settings.max_request_bytes
    except ValueError:
        return False


def extract_api_key(request: Request) -> str | None:
    x_key = request.headers.get("x-api-key")
    if x_key:
        token = x_key.strip()
        return token or None
    bearer = request.headers.get("authorization")
    if bearer and bearer.lower().startswith("bearer "):
        token = bearer[7:].strip()
        return token or None
    return None


def api_auth_configured(settings: Settings) -> bool:
    return bool(settings.api_keys or settings.platform_api_key_hashes.strip())


def api_key_is_valid(api_key: str, settings: Settings) -> bool:
    if api_key in settings.api_keys:
        return True
    hashed = sha256(api_key.encode("utf-8")).hexdigest()
    accepted = {item.strip() for item in settings.platform_api_key_hashes.split(",") if item.strip()}
    return hashed in accepted


def api_key_fingerprint(api_key: str) -> str:
    return sha256(api_key.encode("utf-8")).hexdigest()[:12]


def request_too_large_response():
    return error_json(413, "request_too_large", "Request body exceeds configured maximum size.")


def auth_not_configured_response():
    return error_json(503, "auth_not_configured", "API authentication is not configured.")


def missing_api_key_response():
    return error_json(401, "missing_api_key", "Missing API key.")


def invalid_api_key_response():
    return error_json(403, "invalid_api_key", "Invalid API key.")
