from preordain.models import BaseResponse, RespStrings
from preordain.trackers.schema import CardInfoModel


class SuccessfulRequest(BaseResponse):
    resp = RespStrings.card_info
    info = {"message": "Successful update!"}
    data: CardInfoModel
