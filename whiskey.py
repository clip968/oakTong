# whiskey.py - 간소화 버전
class Whiskey:
    """개별 위스키 정보를 담는 클래스"""
    
    def __init__(self, whiskey_id, name, taste_profile, origin, price, 
                 alcohol_percentage, whiskey_type, image_path=None, age_years=None):
        """위스키 객체 초기화"""
        self.id = whiskey_id
        self.name = name
        self.taste_profile = taste_profile
        self.origin = origin
        self.price = price
        self.alcohol_percentage = alcohol_percentage
        self.type = whiskey_type
        self.image_path = image_path
        self.age_years = age_years
        self.user_review_ids = []
    
    def get_taste_vector(self):
        """맛 프로필 벡터 반환"""
        return self.taste_profile.get_vector()
    
    def get_basic_info(self):
        """기본 정보 반환"""
        return {
            "id": self.id,
            "name": self.name,
            "type": str(self.type),
            "origin": self.origin
        }
    
    def get_full_details(self):
        """모든 상세 정보 반환"""
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
        """리뷰 ID 추가"""
        if review_id not in self.user_review_ids:
            self.user_review_ids.append(review_id)
    
    def __str__(self):
        return f"{self.name} ({str(self.type)})"