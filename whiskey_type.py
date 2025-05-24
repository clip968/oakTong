from enum import Enum

class WhiskeyType(Enum):
    #근데 이거 정작 쓰긴 함?
    SINGLE_MALT = "Single Malt"
    BLENDED = "Blended"
    BOURBON = "Bourbon" 
    RYE = "Rye"
    IRISH = "Irish"
    JAPANESE = "Japanese"
    OTHER = "Other"
    
    def __str__(self):
        return self.value