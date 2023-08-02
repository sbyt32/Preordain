from pydantic import BaseModel


class GroupInfoGroupName(BaseModel):
    group_name: str


class GroupInfoTable(GroupInfoGroupName):
    description: str
    banner_uri: str
