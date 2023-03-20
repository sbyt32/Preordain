from pydantic import BaseModel
from preordain.models import BaseResponse, RespStrings
from preordain.groups.schema import GroupInfoTable

# * https://fastapi.tiangolo.com/tutorial/body/#__tabbed_2_1


# This one is for request format.
class CardInGroupInfo(BaseModel):
    uri: str
    group: str


class GroupInformation(GroupInfoTable):
    cards_in_group: int


# class


class GroupResponse(BaseResponse):
    resp = RespStrings.group_info
    data: list[dict[str, int]] = GroupInformation

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
