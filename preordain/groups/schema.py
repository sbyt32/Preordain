from pydantic import BaseModel


class GroupInfoGroupName(BaseModel):
    group_name: str


class GroupInfoTable(BaseModel):
    group_name: str
    description: str
