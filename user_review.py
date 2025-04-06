# user_review.py
import datetime
from typing import Optional # TYPE_CHECKING 불필요

class User_Review:
    """
    사용자가 특정 위스키에 대해 작성한 리뷰 정보를 담는 클래스입니다.
    """
    def __init__(self, review_id: str, user_id: str, whiskey_id: str, rating: int, review_text: str = ""):
        """
        User_Review 객체 초기화

        Args:
            review_id (str): 리뷰 고유 ID
            user_id (str): 리뷰를 작성한 사용자 ID
            whiskey_id (str): 리뷰 대상 위스키 ID
            rating (int): 평점 (예: 1-5 또는 1-10)
            review_text (str): 리뷰 텍스트 (선택 사항)
        """
        self.review_id: str = review_id
        self.user_id: str = user_id
        self.whiskey_id: str = whiskey_id
        # 평점 범위 검증 추가 가능
        self.rating: int = rating
        self.review_text: str = review_text
        self.review_date: datetime.datetime = datetime.datetime.now() # 리뷰 작성 시점 기록
        # print(f"User_Review created: ID={self.review_id} for Whiskey={self.whiskey_id} by User={self.user_id}") # Debug

    def update_review(self, new_rating: Optional[int] = None, new_text: Optional[str] = None):
        """
        리뷰 내용을 업데이트합니다 (평점 또는 텍스트).

        Args:
            new_rating (Optional[int]): 새로운 평점 (None이면 변경 안 함)
            new_text (Optional[str]): 새로운 리뷰 텍스트 (None이면 변경 안 함)
        """
        if new_rating is not None:
            # 평점 범위 검증 추가 가능
            self.rating = new_rating
            # print(f"Review {self.review_id} rating updated to {new_rating}") # Debug
        if new_text is not None:
            self.review_text = new_text
            # print(f"Review {self.review_id} text updated.") # Debug
        # self.review_date = datetime.datetime.now() # 수정 시각 업데이트? 선택 사항

    def get_review_details(self) -> dict:
        """리뷰 상세 정보를 딕셔너리로 반환합니다."""
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "whiskey_id": self.whiskey_id,
            "rating": self.rating,
            "review_text": self.review_text,
            "review_date": self.review_date.isoformat() # 날짜/시간은 ISO 형식 문자열로
        }

    def __str__(self) -> str:
        """User_Review 객체를 간단한 문자열로 표현합니다."""
        return f"Review(ID:{self.review_id}, User:{self.user_id}, Whiskey:{self.whiskey_id}, Rating:{self.rating})"

# User 클래스 내에서 리뷰 '생성/삭제' 로직이 있을 수 있음 (UML 상 User가 Review를 생성)
# 또는 System/UI 레벨에서 User와 Whiskey 정보를 받아 Review 객체 생성 후 User에게 연결