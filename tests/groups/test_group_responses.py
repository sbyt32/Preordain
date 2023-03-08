from preordain.models import RespStrings

# from preordain.groups.models import CardGroupInformation
from preordain.models import RespStrings

# from preordain.groups.models import CardGroupInformation
from fastapi.testclient import TestClient


def test_connect(client: TestClient):
    response = client.get("/api/groups/?in_use=true")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RespStrings.group_info

    # ! This will eventually change, consider fixing this


def test_inventory_all_groups(client: TestClient):
    response = client.get("/api/groups/?in_use=false")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RespStrings.group_info
