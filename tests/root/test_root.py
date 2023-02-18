from fastapi.testclient import TestClient


def test_root(client: TestClient):
    from preordain.exceptions import RootException

    response = client.get("/")
    assert response.status_code == 400
    response = response.json()
    assert response["resp"] == RootException.resp
