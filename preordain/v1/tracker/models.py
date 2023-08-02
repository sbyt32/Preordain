from preordain.models import BaseResponse
from preordain.v1.tracker.schema import CardInfoModel

RESP_STRING: str = "tracker_update"


class SuccessfulRequest(BaseResponse):
    resp = RESP_STRING
    data: CardInfoModel
