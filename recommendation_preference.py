# recommendation_preference.py
from typing import List, Dict, TYPE_CHECKING
from recommendation import Recommendation # 부모 클래스 import

# 순환 참조 방지를 위해 TYPE_CHECKING 블록 사용
if TYPE_CHECKING:
    from user import User
    from user_preference import User_Preference
    from whiskys import Whiskys
    from whiskey import Whiskey

class Recommendation_Preference(Recommendation):
    """
    사용자 선호도 기반 추천 전략 클래스입니다. Recommendation 클래스를 상속받습니다.
    """
    def __init__(self, user_reference: 'User', whiskeys_reference: 'Whiskys'):
        """
        Recommendation_Preference 초기화
        Args:
            user_reference (User): 사용자 객체 참조
            whiskeys_reference (Whiskys): 위스키 카탈로그 객체 참조
        """
        super().__init__(user_reference, whiskeys_reference) # 부모 클래스의 __init__ 호출
        self.preference_weights: Dict[str, float] = {"sweetness": 1.0, "smoky": 1.0, "fruity": 1.0, "spicy": 1.0}
        # print("Recommendation_Preference initialized.") # Debug

    def get_recommendations(self, count: int) -> List[str]:
        """
        사용자 선호도를 기반으로 위스키를 추천합니다. (부모 클래스의 추상 메서드 구현)
        Args:
            count (int): 추천할 위스키 개수
        Returns:
            List[str]: 추천된 위스키 ID 목록
        """
        print(f"Getting {count} preference-based recommendations for user {self.user_reference.user_id}")
        user_preference = self.user_reference.get_preference()
        if not user_preference:
            print("Warning: User preference not available for recommendation.")
            return []

        all_whiskeys = self.whiskeys_reference.get_all_whiskeys()
        scores = {}
        for whiskey_id, whiskey in all_whiskeys.items():
            # 사용자가 이미 컬렉션에 추가했거나 리뷰한 위스키는 제외? (선택 사항)
            # if self.user_reference.get_history().is_in_collection(whiskey_id): continue
            # if whiskey_id in self.user_reference.get_review_whiskey_ids(): continue # 리뷰한 위스키 ID 목록 필요

            match_score = self.calculate_preference_match(user_preference, whiskey)
            scores[whiskey_id] = match_score

        # 점수 높은 순 정렬
        sorted_whiskeys = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        recommended_ids = [whiskey_id for whiskey_id, score in sorted_whiskeys[:count]] # 상위 count개 ID

        print(f"  Recommended IDs: {recommended_ids}")
        return recommended_ids

    def calculate_preference_match(self, user_preference: 'User_Preference', whiskey: 'Whiskey') -> float:
        """사용자 선호도와 위스키 특성 간의 매칭 점수를 계산합니다."""
        pref_vector = user_preference.get_preference_vector()
        taste_vector = whiskey.get_taste_vector()
        if not pref_vector or not taste_vector or len(pref_vector) != len(taste_vector): return 0.0

        # 예시: 가중치 적용 내적 점수
        score = 0.0
        weights = [self.preference_weights.get("sweetness", 1.0), self.preference_weights.get("smoky", 1.0),
                   self.preference_weights.get("fruity", 1.0), self.preference_weights.get("spicy", 1.0)]
        try: # 벡터 길이 불일치 등 예외 처리
            score = sum(p * t * w for p, t, w in zip(pref_vector, taste_vector, weights))
        except IndexError:
             score = sum(p * t for p, t in zip(pref_vector, taste_vector)) # 가중치 적용 실패 시 단순 내적

        # 가격대 필터링 (선택 사항)
        min_pref_price, max_pref_price = user_preference.get_price_range()
        if min_pref_price is not None and whiskey.price < min_pref_price: return 0.0 # 최소 가격 미달 시 제외
        if max_pref_price is not None and whiskey.price > max_pref_price: return 0.0 # 최대 가격 초과 시 제외

        # print(f"    Calculating match for {whiskey.name}: Pref={pref_vector}, Taste={taste_vector} -> Score={score}") # Debug
        return max(0.0, score) # 점수는 0 이상으로

    def update_weights_from_feedback(self, feedback_data):
        """사용자 피드백 기반 가중치 업데이트 (구현 필요)"""
        print(f"Updating preference weights based on feedback: {feedback_data}")
        pass