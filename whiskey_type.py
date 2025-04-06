# whiskey_type.py - 간소화 버전
from enum import Enum

class WhiskeyType(Enum):
    """위스키 타입을 나타내는 열거형"""
    SINGLE_MALT = "Single Malt"
    BLENDED = "Blended"
    BOURBON = "Bourbon" 
    RYE = "Rye"
    IRISH = "Irish"
    JAPANESE = "Japanese"
    OTHER = "Other"
    
    def __str__(self):
        return self.value