class Whiskys:
    def __init__(self):
        self.whiskey_catalog = {}  # 위스키 ID -> Whiskey 객체
    
    # 위스키 추가
    def add_whiskey(self, whiskey):
        if whiskey.id not in self.whiskey_catalog:
            self.whiskey_catalog[whiskey.id] = whiskey
            print(f"위스키 추가됨: {whiskey.name}")
        else:
            print(f"경고: 위스키 ID {whiskey.id}가 이미 존재합니다.")
    
    def get_whiskey_details(self, whiskey_id):
        """ID로 위스키 정보 조회"""
        return self.whiskey_catalog.get(whiskey_id)
    
    def get_all_whiskeys(self):
        """모든 위스키 목록 반환"""
        return self.whiskey_catalog.copy()
    
    def search_whiskeys(self, search_term):
        """위스키 이름 검색"""
        results = []
        if not search_term:  # 검색어 없으면 전체 반환
            return list(self.whiskey_catalog.values())
        
        term_lower = search_term.lower()
        for whiskey in self.whiskey_catalog.values():
            if term_lower in whiskey.name.lower():
                results.append(whiskey)
        
        print(f"'{search_term}' 검색 결과: {len(results)}개")
        return results
    
    def sort_whiskeys(self, whiskey_list, sort_criteria, reverse=False):
        #위스키 정렬
        sorted_list = whiskey_list[:]  # 복사본 생성
        
        if sort_criteria == 'name':
            sorted_list.sort(key=lambda w: w.name.lower(), reverse=reverse)
        elif sort_criteria == 'price':
            # None 값 처리
            sorted_list.sort(key=lambda w: (w.price is None, w.price or 0), reverse=reverse)
        elif sort_criteria == 'alcohol_percentage':
            sorted_list.sort(key=lambda w: (w.alcohol_percentage is None, w.alcohol_percentage or 0), reverse=reverse)
        else:
            print(f"경고: 알 수 없는 정렬 기준 '{sort_criteria}'")
        
        return sorted_list