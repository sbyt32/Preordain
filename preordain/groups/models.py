from pydantic import BaseModel, validator
from preordain.models import BaseResponse, RespStrings
from preordain.groups.schema import GroupInfoTable
from preordain.utils.find_missing import get_card_from_set_id
from typing import Optional


# This one is for request format.
class CardInGroupInfo(BaseModel):
    set: Optional[str]
    id: Optional[str]
    uri: Optional[str]
    group: str

    class Config:
        validate_assignment = True

    # If missing uri
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
    cards_in_group: int
    description: str


class GroupResponse(BaseResponse):
    resp = RespStrings.group_info
    data: list[GroupInformation]

    class Config:
        schema_extra = {
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


class SuccessfulRequest(BaseResponse):
    resp = RespStrings.group_info
    info = {"message": ""}

    class Config:
        schema_extra = {
            "example": {
                "resp": "group_info",
                "status": 200,
                "info": {"message": "Added / Removed group: string"},
                "data": {
                    "group": "dnt",
                    "description": 'This is part of the deck "Death and Taxes"',
                },
            }
        }
