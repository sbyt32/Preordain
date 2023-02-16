from fastapi.testclient import TestClient
import pytest

def test_search_single(client: TestClient):
    data = {
        "resp": "search_query",
        "status": 200,
        "data": [
            {
                "name": "Thalia, Guardian of Thraben",
                "set": "vow",
                "set_full": "Innistrad: Crimson Vow",
                "id": "38",
                "last_updated": "2023-01-05",
                "prices": {
                    "usd": 0.92,
                    "usd_foil": 3.05,
                    "euro": 0.87,
                    "euro_foil": 2.95,
                    "tix": 0.17,
                },
            }
        ],
    }

    response = client.get("/search/thalia")
    assert response.status_code == 200
    assert response.json() == data

def test_over_50_char(client: TestClient):
    search_query = 'A' * 51
    print(type(search_query))
    with pytest.raises(Exception):
        client.get(f"/search/{search_query}")


# def test_under_50_char(client: TestClient):
#     search_query = ''
#     response = client.get("/search/thalia")
