from fastapi.testclient import TestClient


def test_inventory_root(client: TestClient):
    from starlette.config import environ
    from preordain.inventory.models import RESP_STRING

    response = client.get(f'/api/inventory/?access={str(environ["SEC_TOKEN"])}')
    assert response.status_code == 200
    assert response.json()["resp"] == RESP_STRING


def test_inventory_root_fail(client: TestClient):
    response = client.get(f"/api/inventory/")
    assert response.status_code == 422


def test_inventory_root_bad_token(client: TestClient):
    from preordain.exceptions import InvalidToken

    token = "access"
    token_value = "HELLO_BAD_TOKEN"
    invalid_example = InvalidToken(token)

    response = client.get(f"/api/inventory/?{token}={token_value}")
    assert response.status_code == invalid_example.status_code
    response = response.json()
    assert response["info"] == invalid_example.info
    assert response["resp"] == invalid_example.resp


def test_inventory_bad_validation():
    from preordain.inventory.models import InventoryData
    from pydantic import ValidationError
    import pytest

    incorrect_variant_data = {
        "name": "Thalia, Guardian of Thraben",
        "set": "Innistrad: Crimson Vow",
        "quantity": 2,
        "condition": "nm",
        "variant": "non-foil",
        "avg_cost": 2.00,
    }
    with pytest.raises(ValidationError):
        InventoryData(**incorrect_variant_data)


def test_adding_deleting_from_inventory(client: TestClient):
    from preordain.inventory.models import RESP_STRING
    from starlette.config import environ

    # This actually corresponds to a real card
    sample_uri = "b2b91418-5cbd-443d-9963-7e590dd0b6fc"
    json_body = {
        "add_date": "2023-03-26",
        "uri": sample_uri,
        "qty": 1,
        "buy_price": 20,
        "card_condition": "NM",
        "card_variant": "Normal",
    }
    response = client.post(
        f"/api/inventory/add/?access={str(environ['SEC_TOKEN'])}", json=json_body
    )
    assert response.status_code == 201
    insert_json = response.json()
    assert insert_json["resp"] == RESP_STRING
    removal = client.post(
        f"/api/inventory/delete/?access={str(environ['SEC_TOKEN'])}", json=json_body
    )
    assert removal.status_code == 204
