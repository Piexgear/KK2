def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_upload_invalid_file(client):
    response = client.post(
        "/data/upload",
        files={"file": ("file.txt", "hej", "text/plain")}
    )
    assert response.status_code == 400


def test_stats_without_data(client):
    response = client.get("/data/stats")
    assert response.status_code == 404


def test_ask_without_data(client):
    response = client.post(
        "/ai/ask",
        json={"question": "Vilket är dyrast?"}
    )
    assert response.status_code == 400


def test_upload_valid_file(client):
    csv = "Name,Price\nTetris,10\nElden Ring,60\n"

    response = client.post(
        "/data/upload",
        files={"file": ("games.csv", csv, "text/csv")}
    )

    assert response.status_code == 200


def test_stats_with_data(client, uploaded_data):
    response = client.get("/data/stats")
    assert response.status_code == 200


def test_ask_with_data(client, uploaded_data):
    response = client.post(
        "/ai/ask",
        json={"question": "Vilket är dyrast?"}
    )

    assert response.status_code == 200