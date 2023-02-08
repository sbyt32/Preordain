from fastapi.testclient import TestClient

def test_search_single(client: TestClient):
    data = {
        "resp": "search_query",
        "status": 200,
        "data": [{
            "name": "Thalia, Guardian of Thraben",
            "set": "vow",
            "set_full": "Innistrad: Crimson Vow",
            "id": "38",
            "last_updated": "2022-09-28",
            "prices": {
                "usd": 1.55,
                "usd_foil": 1.65,
                "euro": 1.54,
                "euro_foil": 1.99,
                "tix": 0.29
            }}]
    }

    response = client.get('/search/thalia')
    assert response.status_code == 200
    assert response.json() == data

