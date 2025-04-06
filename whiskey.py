# whiskey.py
from typing import List, Optional # 순환참조 회피용 TYPE_CHECKING 제거 (User_Review ID만 저장)
from taste_profile import TasteProfile
from whiskey_type import WhiskeyType

class Whiskey:
    """
    개별 위스키의 정보를 담는 클래스입니다.
    """
    def __init__(self,
                 whiskey_id: str,
                 name: str,
                 taste_profile: TasteProfile,
                 origin: str,
                 price: float,
                 alcohol_percentage: float,
                 whiskey_type: WhiskeyType,
                 image_path: Optional[str] = None,
                 age_years: Optional[int] = None):
        """
        Whiskey 객체 초기화

        Args:
            whiskey_id (str): 위스키 고유 ID
            name (str): 위스키 이름
            taste_profile (TasteProfile): 맛 프로필 객체
            origin (str): 생산 국가/지역
            price (float): 가격
            alcohol_percentage (float): 알코올 도수
            whiskey_type (WhiskeyType): 위스키 타입 (Enum 값)
            image_path (Optional[str]): 이미지 파일 경로 (선택 사항)
            age_years (Optional[int]): 숙성 연수 (선택 사항)
        """
        self.id: str = whiskey_id
        self.name: str = name
        self.taste_profile: TasteProfile = taste_profile
        self.origin: str = origin
        self.price: float = price
        self.alcohol_percentage: float = alcohol_percentage
        self.type: WhiskeyType = whiskey_type
        self.image_path: Optional[str] = image_path
        self.age_years: Optional[int] = age_years
        self.user_review_ids: List[str] = [] # 이 위스키에 대한 사용자 리뷰 ID 목록
        # print(f"Whiskey created: ID={self.id}, Name={self.name}") # Debug

    def get_taste_vector(self) -> List[int]:
        """위스키의 맛 프로필 벡터를 반환합니다."""
        return self.taste_profile.get_vector()

    def get_full_details(self) -> dict:
        """위스키의 모든 상세 정보를 딕셔너리 형태로 반환합니다."""
        return {
            "id": self.id,
            "name": self.name,
            "taste_profile": str(self.taste_profile), # 문자열로 변환
            "origin": self.origin,
            "price": self.price,
            "alcohol_percentage": self.alcohol_percentage,
            "type": str(self.type), # Enum 값을 문자열로
            "image_path": self.image_path,
            "age_years": self.age_years,
            "user_review_ids": self.user_review_ids
        }

    def get_basic_info(self) -> dict:
        """위스키의 기본적인 정보(ID, 이름, 타입, 원산지)를 딕셔너리로 반환합니다."""
        return {
            "id": self.id,
            "name": self.name,
            "type": str(self.type),
            "origin": self.origin
        }

    def add_review_id(self, review_id: str):
        """이 위스키에 작성된 리뷰의 ID를 추가합니다."""
        if review_id not in self.user_review_ids:
            self.user_review_ids.append(review_id)
            # print(f"Review ID {review_id} added to Whiskey {self.id}") # Debug

    def remove_review_id(self, review_id: str):
        """이 위스키에서 특정 리뷰 ID를 제거합니다."""
        if review_id in self.user_review_ids:
            self.user_review_ids.remove(review_id)
            # print(f"Review ID {review_id} removed from Whiskey {self.id}") # Debug

    def __str__(self) -> str:
        """Whiskey 객체를 이름과 타입으로 간단히 표현합니다."""
        return f"{self.name} ({str(self.type)})"