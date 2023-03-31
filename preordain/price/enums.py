from enum import Enum


class GrowthDirections(str, Enum):
    asc = "asc"
    desc = "desc"


class GrowthCurrency(str, Enum):
    usd = "usd"
    euro = "euro"
    tix = "tix"
    # USD, Euro, TIX
