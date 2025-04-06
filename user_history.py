# user_history.py
import datetime
from collections import deque # 큐(Queue) 자료구조 사용
from typing import List, Tuple, Optional # TYPE_CHECKING 불필요

class User_History:
    """
    사용자의 활동 기록 (조회한 위스키, 컬렉션에 추가한 위스키 등)을 관리하는 클래스입니다.
    """
    # 최근 조회 기록 최대 개수 설정
    MAX_VIEWED_ITEMS = 20

    def __init__(self, user_id: str):
        """
        User_History 초기화

        Args:
            user_id (str): 이 기록의 사용자 ID
        """
        self.user_id: str = user_id
        # 최근 조회한 위스키 목록 (위스키 ID, 조회 시각) - deque는 양쪽 끝에서 추가/삭제가 빠름
        self.viewed_whiskeys: deque[Tuple[str, datetime.datetime]] = deque(maxlen=self.MAX_VIEWED_ITEMS)
        # 사용자가 컬렉션(마셔봤거나 소유한 목록 등)에 추가한 위스키 ID 목록
        self.added_whiskeys: List[str] = []
        # print(f"User_History initialized for user {self.user_id}") # Debug

    def add_viewed_whiskey(self, whiskey_id: str):
        """
        최근 조회한 위스키 목록에 추가합니다. 가장 오래된 항목은 자동으로 제거될 수 있습니다(deque의 maxlen).

        Args:
            whiskey_id (str): 조회한 위스키의 ID
        """
        now = datetime.datetime.now()
        # 중복 조회 시, 최신 시간으로 업데이트하며 맨 앞으로 이동시키기 (선택적 구현)
        # 현재 구현은 단순히 맨 뒤에 추가
        self.viewed_whiskeys.append((whiskey_id, now))
        # print(f"Whiskey {whiskey_id} added to viewed history for user {self.user_id}") # Debug

    def add_to_collection(self, whiskey_id: str):
        """
        사용자 컬렉션에 위스키를 추가합니다 (이미 있다면 추가 안 함).

        Args:
            whiskey_id (str): 컬렉션에 추가할 위스키 ID
        """
        if whiskey_id not in self.added_whiskeys:
            self.added_whiskeys.append(whiskey_id)
            # print(f"Whiskey {whiskey_id} added to collection for user {self.user_id}") # Debug
        # else:
            # print(f"Whiskey {whiskey_id} is already in the collection for user {self.user_id}") # Debug

    def remove_from_collection(self, whiskey_id: str):
        """
        사용자 컬렉션에서 위스키를 제거합니다.

        Args:
            whiskey_id (str): 컬렉션에서 제거할 위스키 ID
        """
        if whiskey_id in self.added_whiskeys:
            self.added_whiskeys.remove(whiskey_id)
            # print(f"Whiskey {whiskey_id} removed from collection for user {self.user_id}") # Debug
        # else:
            # print(f"Whiskey {whiskey_id} not found in the collection for user {self.user_id}") # Debug

    def get_recently_viewed(self, count: Optional[int] = None) -> List[Tuple[str, datetime.datetime]]:
        """
        최근에 조회한 위스키 목록을 반환합니다 (최신순).

        Args:
            count (Optional[int]): 반환할 최대 개수 (None이면 저장된 전체 반환)

        Returns:
            List[Tuple[str, datetime.datetime]]: (위스키 ID, 조회 시각) 튜플의 리스트 (최신 항목이 맨 앞에 오도록)
        """
        # deque는 추가된 순서대로 저장되므로, 최신 항목이 오른쪽에 있음. reversed() 사용.
        items = list(reversed(self.viewed_whiskeys))
        if count is not None and count > 0:
            return items[:count]
        return items

    def get_collection(self) -> List[str]:
        """사용자 컬렉션에 있는 모든 위스키 ID 목록을 반환합니다."""
        return self.added_whiskeys[:] # 복사본 반환

    def is_in_collection(self, whiskey_id: str) -> bool:
        """주어진 위스키 ID가 컬렉션에 있는지 확인합니다."""
        return whiskey_id in self.added_whiskeys

    def clear_history(self, clear_viewed: bool = True, clear_collection: bool = False):
        """
        사용자 활동 기록을 삭제합니다.

        Args:
            clear_viewed (bool): 조회 기록 삭제 여부 (기본값 True)
            clear_collection (bool): 컬렉션 목록 삭제 여부 (기본값 False)
        """
        if clear_viewed:
            self.viewed_whiskeys.clear()
            # print(f"Viewed history cleared for user {self.user_id}") # Debug
        if clear_collection:
            self.added_whiskeys.clear()
            # print(f"Collection cleared for user {self.user_id}") # Debug

    # 데이터를 파일/DB에 저장하고 불러오는 메서드 추가 가능 (save/load)
    # 이 역시 System 클래스나 데이터 관리 모듈에서 통합 관리하는 것이 좋을 수 있음
    