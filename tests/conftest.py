import punq
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.infrastructure.di import init_container
from src.main import web_app_factory
from tests.fixtures import mock_test_container


@pytest.fixture
def sample_data():
    return {
        "2024-01-01": [
            {"cargo_type": "type1", "rate": 100.0},
            {"cargo_type": "type2", "rate": 200.0},
        ]
    }


@pytest.fixture(scope="function")
def container() -> punq.Container:
    return mock_test_container()


@pytest.fixture
def app() -> FastAPI:
    app = web_app_factory()
    app.dependency_overrides[init_container] = mock_test_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
