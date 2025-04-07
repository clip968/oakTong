import datetime
from collections import deque

class User_History:
    # 위스키 기록
    
    MAX_VIEWED_ITEMS = 20  # 최근 조회 최대 개수
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.viewed_whiskeys = deque(maxlen=self.MAX_VIEWED_ITEMS)  # (위스키ID, 조회시각)
        self.added_whiskeys = []  # 컬렉션에 추가한 위스키 ID
    
    # 조회한 위스키 ID 추가
    def add_viewed_whiskey(self, whiskey_id):
        now = datetime.datetime.now()
        self.viewed_whiskeys.append((whiskey_id, now))
    
    # 컬렉션에 위스키 id 추가
    def add_to_collection(self, whiskey_id):
        if whiskey_id not in self.added_whiskeys:
            self.added_whiskeys.append(whiskey_id)
    
    # 컬렉션에서 제거
    def remove_from_collection(self, whiskey_id):
        if whiskey_id in self.added_whiskeys:
            self.added_whiskeys.remove(whiskey_id)
    
    # 최근 조회한 위스키 목록 반환
    def get_recently_viewed(self, count=None):
        items = list(reversed(self.viewed_whiskeys))
        if count:
            return items[:count]
        return items
    
    # 컬렉션 목록 반환
    def get_collection(self):
        return self.added_whiskeys[:]
    
    # 컬렉션에 있는지 확인
    def is_in_collection(self, whiskey_id):
        return whiskey_id in self.added_whiskeys