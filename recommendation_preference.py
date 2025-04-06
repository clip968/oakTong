# recommendation_preference.py - 간소화 버전
from recommendation import Recommendation

class Recommendation_Preference(Recommendation):
    """사용자 선호도 기반 추천 클래스"""
    
    def __init__(self, user_reference, whiskeys_reference):
        """선호도 기반 추천 초기화"""
        super().__init__(user_reference, whiskeys_reference)
    
    def get_recommendations(self, count):
        """선호도 기반 추천 목록 반환"""
        print(f"사용자 {self.user_reference.user_id}의 선호도 기반 추천 {count}개")
        
        user_preference = self.user_reference.get_preference()
        if not user_preference:
            print("사용자 선호도 정보가 없습니다")
            return []
        
        all_whiskeys = self.whiskeys_reference.get_all_whiskeys()
        scores = {}
        
        for whiskey_id, whiskey in all_whiskeys.items():
            match_score = self.calculate_preference_match(user_preference, whiskey)
            scores[whiskey_id] = match_score
        
        # 점수 높은 순 정렬
        sorted_whiskeys = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        recommended_ids = [whiskey_id for whiskey_id, score in sorted_whiskeys[:count]]
        
        return recommended_ids
    
    def calculate_preference_match(self, user_preference, whiskey):
        """선호도와 위스키 특성 간 매칭 점수 계산"""
        pref_vector = user_preference.get_preference_vector()
        taste_vector = whiskey.get_taste_vector()
        
        # 내적 계산
        score = sum(p * t for p, t in zip(pref_vector, taste_vector))
        
        # 가격대 필터링
        min_price, max_price = user_preference.get_price_range()
        if min_price and whiskey.price < min_price:
            return 0.0
        if max_price and whiskey.price > max_price:
            return 0.0
        
        return max(0.0, score)