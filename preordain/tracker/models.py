from preordain.models import BaseResponse, RespStrings
from preordain.tracker.schema import CardInfoModel


class SuccessfulRequest(BaseResponse):
    resp = RespStrings.card_info
    data: CardInfoModel
