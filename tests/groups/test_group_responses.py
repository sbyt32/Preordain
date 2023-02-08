from fastapi.testclient import TestClient

def test_connect(client:TestClient):


    response = client.get('/groups/?use=true')

    assert response.status_code == 200
    # ! This will eventually change, consider fixing this
    assert response.json() == [
        {
            "group": "dnt",
            "description": "This is part of the deck \"Death and Taxes\""
        },
        {
            "group": "white",
            "description": "PLACEHOLDER"
        }
    ]