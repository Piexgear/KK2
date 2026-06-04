from fastapi.testclient import TestClient
from app.main import app
from app.chain.steps import PromptBuilder
from app.schemas import PromptBuilderInput

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_invalid_file():
    
    response = client.post("/data/upload", files={"file": ("csv.txt", "hej", "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files allowed"}


def test_stats_without_data():
    response = client.get("/data/stats")
    assert response.status_code == 404
    assert response.json() == {"detail": "No dataset uploaded"}


def test_ask_without_data():
    response = client.post("/ai/ask", json={"question": "Vilket är det dyraste spelet?"})
    assert response.status_code == 400
    assert response.json() == {"detail": "No dataset uploaded"}


def test_upload_valid_file():
    
    csv = "Name,Price\nElden ring,10\nTetris,20\n"

    response = client.post("/data/upload", files={"file": ("test.csv", csv, "text/csv")})

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert data["columns"] == ["Name", "Price"]


def test_stats_with_data():
    response = client.get("/data/stats")
    assert response.status_code == 200


def test_ask_with_data():
    response = client.post("/ai/ask", json={"question": "Vilket är det dyraste spelet?"})
    assert response.status_code == 200
    data = response.json()
    assert "Tetris" in data["answer"]


def test_ask_with_data_wrong_game():
    response = client.post("/ai/ask", json={"question": "Vilket är det dyraste spelet?"})
    assert response.status_code == 200
    data = response.json()
    assert "Elden ring" not in data["answer"]


def test_prompt_builder_input():
    input = PromptBuilderInput(
        question="Vilket är det dyraste spelet?",
        stats="Name Price\nTetris 20")
    
    result = PromptBuilder().invoke(input)

    assert "Vilket är det dyraste spelet?" in result.prompt
    assert "Tetris" in result.prompt