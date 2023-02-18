from fastapi.testclient import TestClient


def test_inventory_root(client: TestClient):
    from starlette.config import environ

    data = {"resp": "retrieve_inventory"}

    response = client.get(f'/inventory/?access={str(environ["SEC_TOKEN"])}')
    assert response.status_code == 200
    assert response.json()["resp"] == data["resp"]


def test_inventory_root_fail(client: TestClient):
    response = client.get(f"/inventory/")
    assert response.status_code == 422


def test_inventory_root_bad_token(client: TestClient):
    from preordain.exceptions import InvalidToken

    token = "access"
    token_value = "HELLO_BAD_TOKEN"
    invalid_example = InvalidToken(token)

    response = client.get(f"/inventory/?{token}={token_value}")
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
