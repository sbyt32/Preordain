from fastapi.testclient import TestClient


def test_search_single(client: TestClient):
    data = {"resp": "search_query"}

    response = client.get("/api/search/thalia")
    assert response.status_code == 200
    assert response.json()["resp"] == data["resp"]


def test_over_50_char(client: TestClient):
    from preordain.search.exceptions import InvalidSearchQuery

    search_query = "A" * 51
    response = client.get(f"/api/search/{search_query}")

    assert response.status_code == InvalidSearchQuery.status_code
    response = response.json()
    assert response["info"] == InvalidSearchQuery.info
    assert response["resp"] == InvalidSearchQuery.resp


def test_no_results(client: TestClient):
    search_query = "THIS WILL NEVER BE A MAGIC CARD NAME"
    response = client.get(f"/api/search/{search_query}")

    assert response.status_code == 404
    assert response.json()["resp"] == "no_results"
