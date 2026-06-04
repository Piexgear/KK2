from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_invalid_file():
    
    response = client.post("/data/upload", files={"file": ("csv.txt", "hej", "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files allowed"}

def test_upload_valid_file():
    
    csv = "Name,Price\nElden ring,10\nTetris,20\n"

    response = client.post("/data/upload", files={"file": ("test.csv", csv, "text/csv")})

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert data["columns"] == ["Name", "Price"]