from pydantic import field_validator, BaseModel
from preordain.v1.models import BaseResponse
from .enums import EventFormat
from datetime import date
from typing import Union


class EventData(BaseModel):
    format: Union[EventFormat, str]
    url: str
    event_name: str
    event_date: date
    event_type: str

    @field_validator("format", mode="before")
    @classmethod
    def parse_format_data(cls, v):
        if v == EventFormat.Standard:
            v = "Standard"
        elif v == EventFormat.Pioneer:
            v = "Pioneer"
        elif v == EventFormat.Modern:
            v = "Modern"
        elif v == EventFormat.Legacy:
            v = "Legacy"
        elif v == EventFormat.Vintage:
            v = "Vintage"
        else:
            v = "Unknown"
        return v


class EventListings(BaseResponse):
    resp = "recent_events"
    data: list[EventData]
