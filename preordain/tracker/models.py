from preordain.models import BaseResponse
from preordain.tracker.schema import CardInfoModel

RESP_STRING: str = "tracker_update"


class SuccessfulRequest(BaseResponse):
    resp = RESP_STRING
    data: CardInfoModel
