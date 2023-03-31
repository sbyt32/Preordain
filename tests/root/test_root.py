from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get("/api/")
    assert response.status_code == 200


def test_send_request():
    from preordain.utils.connections import send_response

    assert type(send_response("GET", "https://httpbin.org/get")) == list or dict
