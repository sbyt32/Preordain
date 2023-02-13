from preordain.models import BaseModel
from preordain.groups.models import CardGroupInformation
from fastapi.testclient import TestClient


def test_connect(client: TestClient):
    response = client.get("/groups/?use=true")

    assert response.status_code == 200
    # ! This will eventually change, consider fixing this
