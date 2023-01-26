# TODO: Figure out how to correctly write tests
from starlette.testclient import TestClient
from api import app

class TestConnections:

    def test_connect(self):

        client = TestClient(app)

        response = client.get('/groups/?use=true&access=testing')

        assert response.status_code == 200
        # ! This will eventually change, consider fixing this
        assert response.json() == [
            {
                "group_naming": "dnt",
                "description": "This is part of the deck \"Death and Taxes\""
            },
            {
                "group_naming": "white",
                "description": "PLACEHOLDER"
            }
        ]