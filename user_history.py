# user_history.py - 간소화 버전
import datetime
from collections import deque

class User_History:
    """사용자 활동 기록 관리"""
    
    MAX_VIEWED_ITEMS = 20  # 최근 조회 최대 개수
    
    def __init__(self, user_id):
        """활동 기록 초기화"""
        self.user_id = user_id
        self.viewed_whiskeys = deque(maxlen=self.MAX_VIEWED_ITEMS)  # (위스키ID, 조회시각)
        self.added_whiskeys = []  # 컬렉션에 추가한 위스키 ID
    
    def add_viewed_whiskey(self, whiskey_id):
        """조회 기록 추가"""
        now = datetime.datetime.now()
        self.viewed_whiskeys.append((whiskey_id, now))
    
    def add_to_collection(self, whiskey_id):
        """컬렉션에 위스키 추가"""
        if whiskey_id not in self.added_whiskeys:
            self.added_whiskeys.append(whiskey_id)
    
    def remove_from_collection(self, whiskey_id):
        """컬렉션에서 위스키 제거"""
        if whiskey_id in self.added_whiskeys:
            self.added_whiskeys.remove(whiskey_id)
    
    def get_recently_viewed(self, count=None):
        """최근 조회 목록 반환"""
        items = list(reversed(self.viewed_whiskeys))
        if count:
            return items[:count]
        return items
    
    def get_collection(self):
        """컬렉션 목록 반환"""
        return self.added_whiskeys[:]
    
    def is_in_collection(self, whiskey_id):
        """컬렉션 포함 여부 확인"""
        return whiskey_id in self.added_whiskeys