import datetime
from preordain.information.models import CardInformation
from preordain.information.utils import parse_data_for_response
from preordain.models import BaseResponse, RespStrings
from tests.util import get_sample_data

from fastapi.testclient import TestClient


def test_info_root(client: TestClient):
    data = get_sample_data("information")

    response = client.get("/card/")
    assert response.status_code == 200
    assert (
        BaseResponse(
            resp=RespStrings.card_info, status=200, data=parse_data_for_response(data)
        )
        == response.json()
    )


# def test_info_root_fail(client:TestClient):


def test_info_groups(client: TestClient):
    response = client.get("/card/dnt")
    data = [
        {
            "name": "Thalia, Guardian of Thraben",
            "set": "vow",
            "set_full": "Innistrad: Crimson Vow",
            "id": "38",
            "last_updated": "2023-01-05",
            "usd": 0.92,
            "usd_foil": 3.05,
            "euro": 0.87,
            "euro_foil": 2.95,
            "tix": 0.17,
        },
        {
            "name": "Tithe",
            "set": "vis",
            "set_full": "Visions",
            "id": "23",
            "last_updated": "2023-01-05",
            "usd": 24.17,
            "usd_foil": None,
            "euro": 20,
            "euro_foil": None,
            "tix": 0.96,
        },
    ]

    assert response.status_code == 200
    assert BaseResponse[CardInformation](
        info={"group": "dnt", "info": "ye"},
        data=parse_data_for_response(data),
        resp=RespStrings.card_info,
        status=200,
    )


def test_info_single(client: TestClient):
    response = client.get("/card/vow/38/")
    data = [
        {
            "name": "Thalia, Guardian of Thraben",
            "set": "vow",
            "set_full": "Innistrad: Crimson Vow",
            "id": "38",
            "last_updated": "2023-01-05",
            "usd": 0.92,
            "usd_foil": 3.05,
            "euro": 0.87,
            "euro_foil": 2.95,
            "tix": 0.17,
        }
    ]

    assert response.status_code == 200
    assert (
        BaseResponse(
            resp=RespStrings.card_info, status=200, data=parse_data_for_response(data)
        )
        == response.json()
    )
