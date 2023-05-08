from preordain.models import RespStrings
from fastapi.testclient import TestClient


def test_info_single(client: TestClient):
    from preordain.information.models import RESP_STRING

    response = client.get("/api/card/vow/38/")

    assert response.status_code == 200
    response = response.json()

    assert response["resp"] == RESP_STRING
    assert response["status"] == 200


# def test_get_image(client: TestClient):
#     response
