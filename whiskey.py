class Whiskey:
    # 위스키 기본 정보(이거는 나중가서 바꿀 수도 있음)
    def __init__(self, whiskey_id, name, taste_profile, origin, price, 
                 alcohol_percentage, whiskey_type, image_path=None, age_years=None):

        self.id = whiskey_id #위스키 id
        self.name = name # 위스키 이름
        self.taste_profile = taste_profile # 맛 정보
        self.origin = origin # 원산지
        self.price = price # 가격
        self.alcohol_percentage = alcohol_percentage # 도수
        self.type = whiskey_type #위스키 종류
        self.image_path = image_path # 이미지 경로
        self.age_years = age_years # 년도
        self.user_review_ids = [] # 리뷰 ID 목록
    
    def get_taste_vector(self):
        # 맛 프로필 벡터로 변환
        return self.taste_profile.get_vector()
    
    def get_basic_info(self):
        # 기본 정보 호출
        return {
            "id": self.id,
            "name": self.name,
            "type": str(self.type),
            "origin": self.origin
        }
    
    def get_full_details(self):
        # 모든 상세 정보 반환
        return {
            "id": self.id,
            "name": self.name,
            "taste_profile": str(self.taste_profile),
            "origin": self.origin,
            "price": self.price,
            "alcohol_percentage": self.alcohol_percentage,
            "type": str(self.type),
            "image_path": self.image_path,
            "age_years": self.age_years
        }
    
    def add_review_id(self, review_id):
        # 리뷰 id 추가
        if review_id not in self.user_review_ids:
            self.user_review_ids.append(review_id)
    
    def __str__(self):
        return f"{self.name} ({str(self.type)})"