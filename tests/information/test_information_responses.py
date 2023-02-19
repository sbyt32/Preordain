from preordain.models import RespStrings
from fastapi.testclient import TestClient


# ? I removed the data within and chose not to test that.
# Reason being is that Pydantic already validates that data input
# As well, it makes it much harder to accurately test.
def test_info_root(client: TestClient):
    response = client.get("/api/card/")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RespStrings.card_info


# def test_info_root_fail(client:TestClient):


def test_info_groups(client: TestClient):
    response = client.get("/api/card/dnt")

    assert response.status_code == 200
    response = response.json()

    assert response["resp"] == RespStrings.card_info


def test_info_single(client: TestClient):
    response = client.get("/api/card/vow/38/")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RespStrings.card_info
    assert response["status"] == 200
