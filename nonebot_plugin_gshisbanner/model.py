from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, root_validator


class GachaItem(BaseModel):
    itemId: int
    weaponType: str
    rankType: int
    imageUrl: str
    itemType: str
    name: str
    element: Optional[str]


class GsGachaItem(GachaItem):
    name_En: Optional[str]


class Gacha(BaseModel):
    version: str
    start: str
    end: str


class GsGacha(Gacha):
    items: List[GsGachaItem]


class GachaDraw(BaseModel):
    five_star: List[str]
    four_star: List[str]
    start: datetime
    end: datetime
    version: str

    @root_validator(pre=True)
    def set_five_star(cls, values):
        five_character = values.get("five_character")
        five_weapon = values.get("five_weapon")
        if five_character is not None:
            values["five_star"] = five_character
        elif five_weapon is not None:
            values["five_star"] = five_weapon
        else:
            raise ValueError("Either 'five_character' or 'five_weapon' must be set")
        return values

    @root_validator(pre=True)
    def set_four_star(cls, values):
        five_character = values.get("four_character")
        five_weapon = values.get("four_weapon")
        if five_character is not None:
            values["four_star"] = five_character
        elif five_weapon is not None:
            values["four_star"] = five_weapon
        else:
            raise ValueError("Either 'five_character' or 'five_weapon' must be set")
        return values
