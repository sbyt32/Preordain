from pydantic import ConfigDict, BaseModel, validator
from preordain.v1.models import BaseResponse, BaseCardData, CardPrices
import datetime
from preordain.utils.find_missing import get_card_from_set_id
from typing import Optional

RESP_STRING = "group_info"


# This one is for request format.
class CardInGroupInfo(BaseModel):
    set: Optional[str] = None
    id: Optional[str] = None
    uri: Optional[str] = None
    group: str
    model_config = ConfigDict(validate_assignment=True)

    # If missing uri
    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator("uri", pre=True)
    def check_uri_or_set_id(cls, v, values):
        if not v:
            if values["set"] and values["id"]:
                return get_card_from_set_id(values["set"], values["id"])
            else:
                raise ValueError("Missing a way to Identify to the cards!")
        return v


class GroupInformation(BaseModel):
    group: str
    description: str
    cards_in_group: int


class ShowGroupResponse(BaseResponse):
    resp = RESP_STRING
    data: list[GroupInformation]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resp": "group_info",
                "status": 200,
                "data": [
                    {
                        "group": "dnt",
                        "description": 'This is part of the deck "Death and Taxes"',
                        "cards_in_group": "2",
                    }
                ],
            }
        }
    )


class SuccessfulRequest(BaseResponse):
    resp = RESP_STRING
    info = {"message": ""}
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resp": "group_info",
                "status": 201,
                "info": {"message": "Added / Removed group: string"},
                "data": {
                    "group": "dnt",
                    "description": 'This is part of the deck "Death and Taxes"',
                },
            }
        }
    )


class CardGroupsData(BaseCardData):
    uri: str
    last_updated: datetime.date
    groups: Optional[list[str]] = None
    prices: CardPrices


class SingleGroupResponse(BaseResponse):
    resp = RESP_STRING
    info = {"message": ""}
    data = list[CardGroupsData]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resp": RESP_STRING,
                "status": 200,
                "info": {
                    "group_name": "sample group",
                    "description": "sample desc",
                    "qty": 1,
                },
                "data": [
                    {
                        "name": "Aether Vial",
                        "set": "dst",
                        "set_full": "Darksteel",
                        "id": "91",
                        "last_updated": "2023-03-17",
                        "groups": ["sample group"],
                        "prices": {
                            "usd": 9.45,
                            "usd_foil": 105.05,
                            "usd_etch": None,
                            "euro": 9.93,
                            "euro_foil": 39.5,
                            "tix": 5.07,
                        },
                    }
                ],
            }
        }
    )
