# from pydantic import BaseModel
from preordain.v1.models import BaseResponse

RESP_STRING = "internal_routes"

# # I'm not sure if this sort of thing should be easily accessible.
# class DatabaseInfo(BaseModel):
#     project: str = "Preordain"
#     database: str
#     testing: bool


class InternalResponse(BaseResponse):
    resp = RESP_STRING


class UpdateInfo(InternalResponse):
    resp = "update_info"
    info = {"message": "Updated the card information table!"}


class UpdateSets(InternalResponse):
    resp = "update_sets"
    info = {"message": "Updated the set information table!"}
