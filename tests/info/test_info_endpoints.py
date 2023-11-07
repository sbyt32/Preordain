from fastapi.testclient import TestClient


def test_get_card_info(client: TestClient):
    response = client.get("/v2/info/card/c9f8b8fb-1cd8-450e-a1fe-892e7a323479")
    assert response.status_code == 200
