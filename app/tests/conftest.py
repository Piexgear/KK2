import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data import store


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    store._df = None
    yield
    store._df = None


@pytest.fixture
def uploaded_data(client):
    csv = "Name,Price\nTetris,10\nElden Ring,60\n"

    client.post(
        "/data/upload",
        files={"file": ("games.csv", csv, "text/csv")}
    )