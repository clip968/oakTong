# recommendation_similar.py - 간소화 버전
from recommendation import Recommendation
import math

class Recommendation_Similar(Recommendation):
    """유사 위스키 추천 클래스"""
    
    def __init__(self, user_reference, whiskeys_reference):
        """유사 추천 초기화"""
        super().__init__(user_reference, whiskeys_reference)
        self.similarity_threshold = 0.5  # 유사도 임계값
    
    def get_recommendations(self, count, base_whiskey_id=None):
        """유사 위스키 추천 목록 반환"""
        if not base_whiskey_id:
            # 기준 위스키가 없으면 최근 본 위스키 사용
            history = self.user_reference.get_history()
            if history:
                recently_viewed = history.get_recently_viewed(1)
                if recently_viewed:
                    base_whiskey_id = recently_viewed[0][0]
            
            if not base_whiskey_id:
                print("기준 위스키가 없어 추천할 수 없습니다")
                return []
        
        return self.find_similar_whiskeys(base_whiskey_id, count)
    
    def find_similar_whiskeys(self, base_whiskey_id, count):
        """유사 위스키 찾기"""
        base_whiskey = self.whiskeys_reference.get_whiskey_details(base_whiskey_id)
        if not base_whiskey:
            print(f"기준 위스키 ID {base_whiskey_id}를 찾을 수 없습니다")
            return []
        
        all_whiskeys = self.whiskeys_reference.get_all_whiskeys()
        similarities = {}
        
        for whiskey_id, whiskey in all_whiskeys.items():
            if whiskey_id == base_whiskey_id:
                continue  # 자기 자신 제외
            
            similarity = self.calculate_taste_similarity(base_whiskey, whiskey)
            if similarity >= self.similarity_threshold:
                similarities[whiskey_id] = similarity
        
        # 유사도 높은 순 정렬
        sorted_whiskeys = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        similar_ids = [whiskey_id for whiskey_id, score in sorted_whiskeys[:count]]
        
        return similar_ids
    
    def calculate_taste_similarity(self, whiskey1, whiskey2):
        """맛 프로필 간 유사도 계산 (코사인 유사도)"""
        vec1 = whiskey1.get_taste_vector()
        vec2 = whiskey2.get_taste_vector()
        
        # 코사인 유사도
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, similarity))