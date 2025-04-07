from enum import Enum

class WhiskeyType(Enum):
    SINGLE_MALT = "Single Malt"
    BLENDED = "Blended"
    BOURBON = "Bourbon" 
    RYE = "Rye"
    IRISH = "Irish"
    JAPANESE = "Japanese"
    OTHER = "Other"
    
    def __str__(self):
        return self.value