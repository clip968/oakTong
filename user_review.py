# user_review.py - 간소화 버전
import datetime

class User_Review:
    """사용자 위스키 리뷰"""
    
    def __init__(self, review_id, user_id, whiskey_id, rating, review_text=""):
        """리뷰 초기화"""
        self.review_id = review_id
        self.user_id = user_id
        self.whiskey_id = whiskey_id
        self.rating = rating  # 평점 (1-5)
        self.review_text = review_text
        self.review_date = datetime.datetime.now()
    
    def update_review(self, new_rating=None, new_text=None):
        """리뷰 내용 업데이트"""
        if new_rating is not None:
            self.rating = new_rating
        if new_text is not None:
            self.review_text = new_text
    
    def get_review_details(self):
        """리뷰 상세 정보 반환"""
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "whiskey_id": self.whiskey_id,
            "rating": self.rating,
            "review_text": self.review_text,
            "review_date": self.review_date.isoformat()
        }
    
    def __str__(self):
        return f"리뷰(ID:{self.review_id}, 평점:{self.rating})"