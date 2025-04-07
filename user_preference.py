class User_Preference:
    # 사용자의 위스키 취향
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.body_preference = 3  # 기본값 3으로 시작
        self.richness_preference = 3
        self.smoke_preference= 3
        self.sweetness_preference = 3
        self.preferred_price_range = (None, None)  # (최소, 최대)
    
    def update_preference(self, preference_type, value):
        # 맛 선호도 업데이트
        value = max(0, min(5, int(value)))  # 0-5 범위 강제
        
        if preference_type == 'body':
            self.body_preference = value
        elif preference_type == 'richness':
            self.richness_preference = value
        elif preference_type == 'smoke':
            self.smoke_preference= value
        elif preference_type == 'sweetness':
            self.sweetness_preference = value
    
    # 가격 범위 업데이트
    def update_price_range(self, min_price, max_price):
        min_p = int(min_price) if min_price is not None else None
        max_p = int(max_price) if max_price is not None else None
        
        # 값 유효성 검사
        if min_p is not None and max_p is not None and min_p > max_p:
            min_p, max_p = max_p, min_p  # 값 교환
        
        self.preferred_price_range = (min_p, max_p)
    
    def get_price_range(self):
        # 선호 가격 범위 반환
        return self.preferred_price_range
    
    def get_preference_vector(self):
        # 선호 벡터 반환
        return [self.body_preference, self.richness_preference, 
                self.smoke_preference, self.sweetness_preference]