from enum import Enum


class CardConditions(str, Enum):
    NM = "NM"
    LP = "LP"
    MP = "MP"
    HP = "HP"
    DMG = "DMG"


class CardVariants(str, Enum):
    Normal = "Normal"
    Foil = "Foil"
    Etched = "Etched"


class CardFormatLegalities(str, Enum):
    legal = "legal"
    not_legal = "not_legal"
    banned = "banned"
    restricted = "restricted"


class CardRarity(str, Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    special = "special"
    mythic = "mythic"
    bonus = "bonus"
