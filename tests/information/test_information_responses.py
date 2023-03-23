from preordain.models import RespStrings
from fastapi.testclient import TestClient


def test_info_groups(client: TestClient):
    response = client.get("/api/card/dnt")

    assert response.status_code == 200
    response = response.json()

    assert response["status"] == 200
    assert response["resp"] == RespStrings.card_info


def test_info_single(client: TestClient):
    response = client.get("/api/card/vow/38/")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RespStrings.card_info
    assert response["status"] == 200
