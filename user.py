class User:
    # 사용자 기본 정보
    
    def __init__(self, user_id, user_name, user_age=None, user_sex=None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_age = user_age
        self.user_sex = user_sex  # True: 남성, False: 여성, None: 논바이너리(?)
        
        # 관련 객체들
        self.user_preference = None
        self.user_history = None
        self.user_review_ids = []
    
    def set_preference(self, preference):
        # 선호도 객체 설정
        self.user_preference = preference
    
    # 활동 기록 객체 설정
    def set_history(self, history):
        self.user_history = history
    
    def get_user_default_information(self):
        # 기본 정보 반환
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_age": self.user_age,
            "user_sex": self.user_sex
        }
    
    def get_preference(self):
        #선호도 객체 반호나
        return self.user_preference
    
    def get_history(self):
        # 활동 기록 객체 반환
        return self.user_history
    
    def add_review_id(self, review_id):
        # 리뷰 id 추가
        if review_id not in self.user_review_ids:
            self.user_review_ids.append(review_id)
    
    def get_review_ids(self):
        # 리뷰 목록 반환
        return self.user_review_ids[:]