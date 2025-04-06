# user_preference.py - 간소화 버전
class User_Preference:
    """사용자의 위스키 취향 정보"""
    
    def __init__(self, user_id):
        """선호도 초기화"""
        self.user_id = user_id
        self.sweetness_preference = 3  # 기본값 (0-5)
        self.smoky_preference = 3
        self.fruity_preference = 3
        self.spicy_preference = 3
        self.preferred_price_range = (None, None)  # (최소, 최대)
    
    def update_preference(self, preference_type, value):
        """맛 선호도 업데이트"""
        value = max(0, min(5, int(value)))  # 0-5 범위 강제
        
        if preference_type == 'sweetness':
            self.sweetness_preference = value
        elif preference_type == 'smoky':
            self.smoky_preference = value
        elif preference_type == 'fruity':
            self.fruity_preference = value
        elif preference_type == 'spicy':
            self.spicy_preference = value
    
    def update_price_range(self, min_price, max_price):
        """가격 범위 업데이트"""
        min_p = int(min_price) if min_price is not None else None
        max_p = int(max_price) if max_price is not None else None
        
        # 값 유효성 검사
        if min_p is not None and max_p is not None and min_p > max_p:
            min_p, max_p = max_p, min_p  # 값 교환
        
        self.preferred_price_range = (min_p, max_p)
    
    def get_price_range(self):
        """선호 가격 범위 반환"""
        return self.preferred_price_range
    
    def get_preference_vector(self):
        """선호도 벡터 반환"""
        return [self.sweetness_preference, self.smoky_preference, 
                self.fruity_preference, self.spicy_preference]