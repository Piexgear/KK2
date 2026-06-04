def test_ai_mock(client, uploaded_data, monkeypatch):

    class FakeResult:
        answer = "Tetris är billigast"
        model = "mock"

    monkeypatch.setattr(
        "app.chain.pipeline.chain.invoke",
        lambda input: FakeResult()
    )

    response = client.post(
        "/ai/ask",
        json={"question": "Vilket är dyrast?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Tetris är billigast"