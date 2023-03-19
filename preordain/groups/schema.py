from pydantic import BaseModel
from preordain.models import BaseResponse, RespStrings


class GroupInfoTable(BaseModel):
    group_name: str
    description: str
