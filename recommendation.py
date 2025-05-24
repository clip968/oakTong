class Recommendation:
    # 추천 시스템 기본 클래스
    
    def __init__(self, user_reference, whiskeys_reference):
        self.user_reference = user_reference
        self.whiskeys_reference = whiskeys_reference
    
    def get_recommendations(self, count):
        # 위스키 추천 목록 반환
        return []