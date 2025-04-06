# recommendation_similar.py
from typing import List, Dict, TYPE_CHECKING, Optional # Optional 추가
from recommendation import Recommendation # 부모 클래스 import
import math # 코사인 유사도 등 계산 시 필요할 수 있음

if TYPE_CHECKING:
    from user import User
    from whiskys import Whiskys
    from whiskey import Whiskey

class Recommendation_Similar(Recommendation):
    """
    특정 위스키와 유사한 위스키를 추천하는 전략 클래스입니다. Recommendation 클래스를 상속받습니다.
    """
    def __init__(self, user_reference: 'User', whiskeys_reference: 'Whiskys'):
        """ Recommendation_Similar 초기화 """
        super().__init__(user_reference, whiskeys_reference)
        self.similarity_threshold: float = 0.5 # 유사도 임계값 (0~1 사이, 예시값 조정 필요)
        self.feature_weights: Dict[str, float] = {"taste": 0.7, "price": 0.3} # 특징별 가중치 (합이 1이 되도록 조정 권장)
        # print("Recommendation_Similar initialized.") # Debug

    def get_recommendations(self, count: int, base_whiskey_id: Optional[str] = None) -> List[str]:
        """
        기준 위스키와 유사한 위스키를 추천합니다. (부모 클래스 메서드 오버라이드)
        Args:
            count (int): 추천할 위스키 개수
            base_whiskey_id (Optional[str]): 유사도 비교 기준 위스키 ID. None이면 사용자의 최근 본 기록 등 활용 시도.
        Returns:
            List[str]: 추천된 위스키 ID 목록
        """
        if not base_whiskey_id:
             # 기준 ID 없으면 최근 조회 기록 사용 시도
             history = self.user_reference.get_history()
             if history:
                 recently_viewed = history.get_recently_viewed(1)
                 if recently_viewed:
                      base_whiskey_id = recently_viewed[0][0]
                      print(f"No base_whiskey_id provided, using recently viewed: {base_whiskey_id}")
             if not base_whiskey_id: # 그래도 없으면 추천 불가
                  print("Error: Cannot get similar recommendations without a base whiskey.")
                  return []
        else:
             print(f"Getting {count} recommendations similar to base whiskey ID: {base_whiskey_id}")

        return self.find_similar_whiskeys(base_whiskey_id, count)

    def find_similar_whiskeys(self, base_whiskey_id: str, count: int) -> List[str]:
        """주어진 기준 위스키와 가장 유사한 위스키들을 찾아 반환합니다."""
        print(f"Finding {count} whiskeys similar to {base_whiskey_id}")
        base_whiskey = self.whiskeys_reference.get_whiskey_details(base_whiskey_id)
        if not base_whiskey:
            print(f"Error: Base whiskey ID {base_whiskey_id} not found.")
            return []

        all_whiskeys = self.whiskeys_reference.get_all_whiskeys()
        similarities = {}
        for whiskey_id, whiskey in all_whiskeys.items():
            if whiskey_id == base_whiskey_id: continue # 자기 자신 제외
            overall_sim = self.calculate_overall_similarity(base_whiskey, whiskey)
            if overall_sim >= self.similarity_threshold: # 임계값 이상만 고려
                 similarities[whiskey_id] = overall_sim

        # 유사도 높은 순 정렬
        sorted_whiskeys = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        similar_ids = [whiskey_id for whiskey_id, score in sorted_whiskeys[:count]]
        print(f"  Found similar IDs: {similar_ids}")
        return similar_ids

    def calculate_overall_similarity(self, whiskey1: 'Whiskey', whiskey2: 'Whiskey') -> float:
        """두 위스키 간의 전체적인 유사도를 특징별 가중치를 적용하여 계산합니다."""
        taste_sim = self.calculate_taste_similarity(whiskey1, whiskey2)
        price_sim = self.calculate_price_similarity(whiskey1, whiskey2)
        # 다른 특징(origin, type, age 등) 유사도 추가 가능

        # 가중치 적용하여 최종 유사도 계산
        overall_similarity = (taste_sim * self.feature_weights.get("taste", 0.0) +
                              price_sim * self.feature_weights.get("price", 0.0))
        # 가중치 합으로 정규화 (선택적, 가중치 합이 1이면 불필요)
        total_weight = sum(self.feature_weights.values())
        if total_weight > 0:
             overall_similarity /= total_weight

        # print(f"    Overall sim for {whiskey1.name} vs {whiskey2.name}: Taste={taste_sim:.2f}, Price={price_sim:.2f} -> Overall={overall_similarity:.2f}") # Debug
        return max(0.0, min(1.0, overall_similarity)) # 0~1 범위 보장

    def calculate_taste_similarity(self, whiskey1: 'Whiskey', whiskey2: 'Whiskey') -> float:
        """두 위스키의 맛 프로필 간 유사도를 계산합니다 (예: 코사인 유사도)."""
        vec1 = whiskey1.get_taste_vector()
        vec2 = whiskey2.get_taste_vector()
        if not vec1 or not vec2 or len(vec1) != len(vec2): return 0.0

        # 코사인 유사도 계산
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0: return 0.0 # 벡터 크기가 0이면 유사도 0
        similarity = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, similarity)) # 0~1 범위 보장 (-1~1 범위를 0~1로 조정 필요시 (sim + 1) / 2 사용)

    def calculate_price_similarity(self, whiskey1: 'Whiskey', whiskey2: 'Whiskey') -> float:
        """두 위스키의 가격 간 유사도를 계산합니다 (0~1 범위)."""
        price1 = whiskey1.price
        price2 = whiskey2.price
        if price1 is None or price2 is None or price1 <= 0 or price2 <= 0: return 0.0 # 가격 정보 없거나 0이하면 0점

        # 가격 차이 비율 기반 유사도 (1에 가까울수록 유사)
        # 예: 1 - (가격차이 / 큰가격)
        try:
            similarity = 1.0 - abs(price1 - price2) / max(price1, price2)
        except ZeroDivisionError:
             similarity = 1.0 if price1 == price2 else 0.0 # 둘 다 0인 경우는 위에서 처리됨

        # print(f"      Price similarity: {similarity}") # Debug
        return max(0.0, min(1.0, similarity)) # 0~1 범위 보장