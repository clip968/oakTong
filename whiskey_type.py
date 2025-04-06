# whiskey_type.py
from enum import Enum, auto

class WhiskeyType(Enum):
    """
    위스키 타입을 나타내는 열거형(Enum)입니다.
    """
    SINGLE_MALT = "Single Malt"
    BLENDED = "Blended"
    BOURBON = "Bourbon"
    RYE = "Rye"
    IRISH = "Irish"
    JAPANESE = "Japanese"
    OTHER = "Other"

    def __str__(self) -> str:
        return self.value