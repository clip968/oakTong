# recommendation.py
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

# 순환 참조 방지를 위해 TYPE_CHECKING 블록 사용
if TYPE_CHECKING:
    from user import User
    from whiskys import Whiskys
    from whiskey import Whiskey

class Recommendation(ABC):
    """
    추천 시스템의 기본 추상 클래스입니다.
    다양한 추천 전략의 공통 인터페이스 역할을 합니다.
    """
    def __init__(self, user_reference: 'User', whiskeys_reference: 'Whiskys'):
        """
        Recommendation 초기화
        Args:
            user_reference (User): 사용자 객체 참조
            whiskeys_reference (Whiskys): 위스키 카탈로그 객체 참조
        """
        if not user_reference or not whiskeys_reference: # 기본 방어 코드
             raise ValueError("User reference and Whiskys reference cannot be None for Recommendation")
        self.user_reference = user_reference
        self.whiskeys_reference = whiskeys_reference
        # print(f"Recommendation initialized with User: {user_reference.user_id}, Whiskys: {whiskeys_reference}") # Debug

    @abstractmethod
    def get_recommendations(self, count: int) -> List[str]:
        """
        지정된 개수만큼 위스키 추천 목록(ID)을 반환하는 추상 메서드.
        하위 클래스에서 구체적인 로직을 구현해야 합니다.
        Args:
            count (int): 추천할 위스키 개수
        Returns:
            List[str]: 추천된 위스키 ID 목록
        """
        pass

    # 아래 메서드들은 특정 전략에 더 적합할 수 있으므로, 필요시 하위 클래스로 이동하거나 수정 가능
    def calculate_similarity(self, whiskey1_id: str, whiskey2_id: str) -> float:
        """두 위스키 간의 유사도를 계산합니다. (기본 구현 또는 Placeholder)"""
        whiskey1 = self.whiskeys_reference.get_whiskey_details(whiskey1_id)
        whiskey2 = self.whiskeys_reference.get_whiskey_details(whiskey2_id)
        if whiskey1 and whiskey2:
            # 실제 유사도 계산 로직 구현 필요
            print(f"Calculating similarity between {whiskey1.name} and {whiskey2.name}") # Debug
            # 예시: 단순 맛 벡터 유사도 (구현 필요)
            # taste_sim = self._calculate_vector_similarity(whiskey1.get_taste_vector(), whiskey2.get_taste_vector())
            return 0.5 # 임시 반환 값
        return 0.0

    def calculate_user_whiskey_score(self, user: 'User', whiskey: 'Whiskey') -> float:
        """특정 사용자와 특정 위스키 간의 예상 선호도 점수를 계산합니다. (기본 구현 또는 Placeholder)"""
        # User 객체와 Whiskey 객체를 직접 받는 것으로 변경 (ID 대신)
        if user and whiskey:
             user_pref = user.get_preference()
             if user_pref:
                  # 실제 점수 계산 로직 구현 필요
                  print(f"Calculating score for User {user.user_id} and Whiskey {whiskey.name}") # Debug
                  # 예시: 선호도 벡터와 맛 벡터 내적 (구현 필요)
                  # pref_vec = user_pref.get_preference_vector()
                  # taste_vec = whiskey.get_taste_vector()
                  # score = self._calculate_dot_product(pref_vec, taste_vec)
                  return 3.0 # 임시 반환 값
        return 0.0

    # 내부 헬퍼 메서드 예시 (필요시 추가)
    def _calculate_vector_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        # 코사인 유사도 등 구현
        return 0.5

    def _calculate_dot_product(self, vec1: List[float], vec2: List[float]) -> float:
        # 내적 계산 구현
        if len(vec1) != len(vec2): return 0.0
        return sum(x * y for x, y in zip(vec1, vec2))