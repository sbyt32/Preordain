from preordain.models import RecentCardSales, BaseResponse
from preordain.inventory.models import InventoryData
from pydantic import ValidationError
import pytest

class TestModels:
    # Testing if just the models themselves work
    def test_return_inventory(self):
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
    # Testing if the full response properly validates
    def test_InventoryData(self):
        faulty_data = [
            {
                "name": "Thalia, Guardian of Thraben",
                "set": "Innistrad: Crimson Vow",
                "quantity": 2,
                "condition": "nm",
                "variant": "non-foil",
                "avg_cost": 2.00
            }
        ]

        with pytest.raises(ValueError):
            BaseResponse[InventoryData](data=faulty_data, status=200, resp='retrieve_inventory')

