import os

import pytest
from fastapi.testclient import TestClient

from api.config import reset_settings_cache
from api.main import app


@pytest.fixture(autouse=True)
def test_env():
    os.environ["PLATFORM_API_KEYS"] = "test-api-key"
    os.environ["USE_INMEMORY_STORE"] = "true"
    os.environ["ENFORCE_TENANT_JWT"] = "false"
    reset_settings_cache()
    yield
    reset_settings_cache()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-api-key"}
