# TODO: Figure out how to correctly write tests
from fastapi.testclient import TestClient
from preordain.api import app
class TestConnections:
    def test_connect(self):

        client = TestClient(app)

        response = client.get('/groups/?use=true&access=testing')

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
    
    def test_root_conn(self):

        client = TestClient(app)
        response = client.get('/')
        # TODO: Test exceptions! This will eventually be an exception.
        assert response.status_code == 200
        assert response.json() == {
            "resp": "error",
            "status": 200,
            "message": "The request failed due to being at root. If you're just testing if it works, yeah it works.",
        }