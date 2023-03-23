from fastapi.testclient import TestClient


def test_root(client: TestClient):
    from preordain.exceptions import RootException

    response = client.get("/api/")
    assert response.status_code == 400
    response = response.json()
    assert response["resp"] == RootException.resp


def test_send_request():
    from preordain.utils.connections import send_response

    assert type(send_response("GET", "https://httpbin.org/get")) == list or dict
