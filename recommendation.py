# recommendation.py - 간소화 버전
class Recommendation:
    """추천 시스템 기본 클래스"""
    
    def __init__(self, user_reference, whiskeys_reference):
        """추천 엔진 초기화"""
        self.user_reference = user_reference
        self.whiskeys_reference = whiskeys_reference
    
    def get_recommendations(self, count):
        """위스키 추천 목록 반환 (하위 클래스에서 구현)"""
        print("이 메서드는 하위 클래스에서 구현해야 합니다")
        return []