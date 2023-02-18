from pydantic import BaseModel
from preordain.models import BaseResponse, RespStrings

# * https://fastapi.tiangolo.com/tutorial/body/#__tabbed_2_1

# This one is for request format.
class CardInGroupInfo(BaseModel):
    set: str
    id: str
    group: str

class GroupInformation(BaseModel):
    group: str
    description: str
    cards_in_group: int

class GroupResponse(BaseResponse):
    resp = RespStrings.group_info
    data: list[dict[str,int]] = GroupInformation

    class Config:
        schema_extra = {
            "example": {
                "resp": 'group_info',
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