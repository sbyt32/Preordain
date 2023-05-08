# from preordain.groups.models import CardGroupInformation
from fastapi.testclient import TestClient


def test_connect(client: TestClient):
    from preordain.groups.models import RESP_STRING

    response = client.get("/api/groups/?in_use=true")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RESP_STRING


def test_inventory_all_groups(client: TestClient):
    from preordain.groups.models import RESP_STRING

    response = client.get("/api/groups/?in_use=false")

    assert response.status_code == 200
    response = response.json()
    assert response["resp"] == RESP_STRING


def test_insert_and_removal(client: TestClient):
    from preordain.groups.models import RESP_STRING
    from preordain.groups.schema import GroupInfoTable

    test_group_name = "TEST_GROUP_NAME"
    test_group_desc = "TEST_GROUP_DESC"
    test_body = GroupInfoTable(
        group_name=test_group_name, description=test_group_desc, banner_uri=""
    )
    new_resp = client.post("/api/groups/new/", json=test_body.dict())
    assert new_resp.status_code == 201
    new_resp_json = new_resp.json()
    assert new_resp_json["resp"] == RESP_STRING
    assert new_resp_json["info"] == {"message": f"Added group: {test_group_name}"}
    assert new_resp_json["data"] == test_body.dict()

    delete_resp = client.delete(f"/api/groups/delete/{test_group_name}")
    assert delete_resp.status_code == 204
    assert client.get(f"/api/card/{test_group_name}").status_code == 404


def test_info_groups(client: TestClient):
    from preordain.groups.models import RESP_STRING

    response = client.get("/api/groups/dnt")

    assert response.status_code == 200
    response = response.json()

    assert response["resp"] == RESP_STRING
    assert response["status"] == 200
