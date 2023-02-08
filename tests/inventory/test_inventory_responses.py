from fastapi.testclient import TestClient

def test_inventory_root(client:TestClient):
    from starlette.config import environ
    data = {
        "resp": "retrieve_inventory",
        "status": 200,
        "data": [
            {
                "name": "Thalia, Guardian of Thraben",
                "set": "Innistrad: Crimson Vow",
                "quantity": 2,
                "condition": "NM",
                "variant": "Normal",
                "avg_cost": 2
            }
        ]
    }

    response = client.get(f'/inventory/?access={str(environ["SEC_TOKEN"])}')
    assert response.status_code == 200
    assert response.json() == data
    
def test_inventory_root_fail(client:TestClient):
    response = client.get(f'/inventory/')
    assert response.status_code == 422
    
def test_inventory_root_bad_token(client:TestClient):
    response = client.get(f'/inventory/?access=HELLO_BAD_TOKEN')
    assert response.status_code == 403
    assert response.json() == {
        "resp": "error",
        "status": 403,
        "message": "access_token was not given or was incorrect. This error has been logged."
    }

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
            "avg_cost": 2.00
    }
    with pytest.raises(ValidationError):
        InventoryData(**incorrect_variant_data)