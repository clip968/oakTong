# taste_profile.py
from typing import List

class TasteProfile:
    """
    위스키의 맛 프로필을 나타내는 클래스입니다.
    """
    def __init__(self, sweetness: int = 0, smoky: int = 0, fruity: int = 0, spicy: int = 0):
        """
        TasteProfile 초기화

        Args:
            sweetness (int): 단맛 정도 (예: 0-5)
            smoky (int): 스모키함 정도 (예: 0-5)
            fruity (int): 과일향 정도 (예: 0-5)
            spicy (int): 스파이시함 정도 (예: 0-5)
        """
        self.sweetness = sweetness
        self.smoky = smoky
        self.fruity = fruity
        self.spicy = spicy
        # print(f"TasteProfile created: Sweet={sweetness}, Smoky={smoky}, Fruity={fruity}, Spicy={spicy}") # Debug

    def get_vector(self) -> List[int]:
        """맛 프로필을 정수 리스트(벡터) 형태로 반환합니다."""
        return [self.sweetness, self.smoky, self.fruity, self.spicy]

    def __str__(self) -> str:
        """TasteProfile 객체를 문자열로 표현합니다."""
        return f"Sweet: {self.sweetness}, Smoky: {self.smoky}, Fruity: {self.fruity}, Spicy: {self.spicy}"