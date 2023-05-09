from enum import Enum


class EventFormat(str, Enum):
    Standard = "ST"
    Pioneer = "PI"
    Modern = "MO"
    Legacy = "LE"
    Vintage = "VI"
