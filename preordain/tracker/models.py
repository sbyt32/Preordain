from preordain.models import BaseResponse
from preordain.tracker.schema import CardInfoModel

resp_string: str = "tracker_update"


class SuccessfulRequest(BaseResponse):
    resp = resp_string
    data: CardInfoModel
