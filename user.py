# user.py
from typing import List, Optional, TYPE_CHECKING

# 순환 참조 방지를 위해 TYPE_CHECKING 사용
if TYPE_CHECKING:
    from user_preference import User_Preference
    from user_history import User_History
    from user_review import User_Review

# 실제로는 User_Review 객체 대신 ID 목록만 가질 수도 있음. UML 기반으로 객체 리스트 유지.
# 단, 메모리 사용량 및 객체 관리 복잡성 고려 필요. 여기서는 ID 목록으로 가정.
class User:
    """
    애플리케이션 사용자의 정보를 관리하는 클래스입니다.
    선호도, 활동 기록, 작성한 리뷰 등의 정보를 포함합니다.
    """
    def __init__(self, user_id: str, user_name: str, user_age: Optional[int] = None, user_sex: Optional[bool] = None):
        """
        User 객체 초기화

        Args:
            user_id (str): 사용자 고유 ID (로그인 등에 사용)
            user_name (str): 사용자 이름
            user_age (Optional[int]): 사용자 나이 (선택 사항)
            user_sex (Optional[bool]): 사용자 성별 (True: 남성, False: 여성, None: 미지정) (선택 사항)
        """
        self.user_id: str = user_id
        self.user_name: str = user_name
        self.user_age: Optional[int] = user_age
        self.user_sex: Optional[bool] = user_sex # True: Male, False: Female, None: Undisclosed

        # 사용자의 선호도, 기록, 리뷰 객체를 User 객체가 직접 소유하도록 구성
        # System 클래스에서 User 생성 시 이 객체들도 함께 생성하거나 로드해서 연결해줘야 함
        self.user_preference: Optional['User_Preference'] = None
        self.user_history: Optional['User_History'] = None
        self.user_review_ids: List[str] = [] # 사용자가 작성한 리뷰의 ID 목록
        # print(f"User created: ID={self.user_id}, Name={self.user_name}") # Debug

    def set_preference(self, preference: 'User_Preference'):
        """사용자의 선호도 객체를 설정합니다."""
        self.user_preference = preference
        # print(f"Preference object set for user {self.user_id}") # Debug

    def set_history(self, history: 'User_History'):
        """사용자의 활동 기록 객체를 설정합니다."""
        self.user_history = history
        # print(f"History object set for user {self.user_id}") # Debug

    def get_user_default_information(self) -> dict:
        """사용자의 기본 정보(ID, 이름, 나이, 성별)를 딕셔너리로 반환합니다."""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_age": self.user_age,
            "user_sex": self.user_sex
        }

    def update_user_information(self, user_info: dict):
        """
        사용자 정보를 업데이트합니다. (이름, 나이, 성별 등)

        Args:
            user_info (dict): 업데이트할 정보 딕셔너리 (예: {'user_name': 'New Name', 'user_age': 35})
        """
        print(f"Updating user information for {self.user_id} with data: {user_info}") # Debug
        if 'user_name' in user_info:
            self.user_name = user_info['user_name']
        if 'user_age' in user_info:
            try:
                self.user_age = int(user_info['user_age']) if user_info['user_age'] is not None else None
            except ValueError:
                print("Error: Invalid age format.")
        if 'user_sex' in user_info:
            self.user_sex = user_info['user_sex'] # bool 또는 None 기대
        # 필요한 다른 정보 업데이트 로직 추가

    def get_preference(self) -> Optional['User_Preference']:
        """사용자의 선호도 객체를 반환합니다."""
        return self.user_preference

    def get_history(self) -> Optional['User_History']:
        """사용자의 활동 기록 객체를 반환합니다."""
        return self.user_history

    def add_review_id(self, review_id: str):
        """사용자가 작성한 리뷰의 ID를 추가합니다."""
        if review_id not in self.user_review_ids:
            self.user_review_ids.append(review_id)
            # print(f"Review ID {review_id} added to User {self.user_id}") # Debug

    def remove_review_id(self, review_id: str):
        """사용자 리뷰 목록에서 특정 리뷰 ID를 제거합니다."""
        if review_id in self.user_review_ids:
            self.user_review_ids.remove(review_id)
            # print(f"Review ID {review_id} removed from User {self.user_id}") # Debug

    def get_review_ids(self) -> List[str]:
        """사용자가 작성한 모든 리뷰의 ID 목록을 반환합니다."""
        return self.user_review_ids[:] # 복사본 반환

    def __str__(self) -> str:
        """User 객체를 ID와 이름으로 간단히 표현합니다."""
        return f"User(ID: {self.user_id}, Name: {self.user_name})"