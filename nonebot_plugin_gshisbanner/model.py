from typing import List, Optional

from pydantic import BaseModel


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
