"""Sample test suite."""

import logging

# pylint:disable=redefined-outer-name,protected-access
import pytest
from fastapi.testclient import TestClient

from main import create_app

# from models import db

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Spotifiuba - 2022"
