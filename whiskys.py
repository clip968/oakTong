# whiskys.py
from typing import Dict, List, Optional, Callable, Any
from whiskey import Whiskey, TasteProfile, WhiskeyType # 필요한 클래스 import

class Whiskys:
    """
    전체 위스키 카탈로그를 관리하는 클래스입니다.
    위스키 데이터를 저장하고 검색, 필터링, 정렬하는 기능을 제공합니다.
    """
    def __init__(self):
        """Whiskys 카탈로그 초기화"""
        self.whiskey_catalog: Dict[str, Whiskey] = {} # 위스키 ID를 key로, Whiskey 객체를 value로 저장
        # print("Whiskys catalog initialized.") # Debug

    def add_whiskey(self, whiskey: Whiskey):
        """ 카탈로그에 새로운 위스키를 추가합니다. """
        if not isinstance(whiskey, Whiskey): # 타입 체크 추가
             print(f"Error: Invalid object type provided to add_whiskey.")
             return
        if whiskey.id not in self.whiskey_catalog:
            self.whiskey_catalog[whiskey.id] = whiskey
            # print(f"Whiskey added: {whiskey.name} (ID: {whiskey.id})") # Debug
        else:
            print(f"Warning: Whiskey ID {whiskey.id} already exists. Not added.")

    def get_whiskey_details(self, whiskey_id: str) -> Optional[Whiskey]:
        """ 주어진 ID에 해당하는 위스키 객체를 반환합니다. """
        return self.whiskey_catalog.get(whiskey_id)

    def get_all_whiskeys(self) -> Dict[str, Whiskey]:
        """ 카탈로그의 모든 위스키 객체를 딕셔너리로 반환합니다. """
        return self.whiskey_catalog.copy()

    def update_whiskey(self, whiskey_id: str, new_data: dict):
        """ 기존 위스키 정보를 업데이트합니다. """
        whiskey = self.get_whiskey_details(whiskey_id)
        if whiskey:
            print(f"Updating whiskey {whiskey_id} with data: {new_data}") # Debug
            if 'price' in new_data:
                try: whiskey.price = float(new_data['price'])
                except (ValueError, TypeError): print(f"Warn: Invalid price {new_data['price']}")
            if 'age_years' in new_data:
                 try: whiskey.age_years = int(new_data['age_years']) if new_data['age_years'] is not None else None
                 except (ValueError, TypeError): print(f"Warn: Invalid age {new_data['age_years']}")
            # 이름, 원산지, 타입, 맛 프로필 등 다른 속성 업데이트 로직 추가 가능
            if 'name' in new_data: whiskey.name = str(new_data['name'])
            # ...
        else:
            print(f"Error: Whiskey ID {whiskey_id} not found for update.")

    def delete_whiskey(self, whiskey_id: str):
        """ 카탈로그에서 특정 위스키를 삭제합니다. """
        if whiskey_id in self.whiskey_catalog:
            deleted_name = self.whiskey_catalog[whiskey_id].name
            del self.whiskey_catalog[whiskey_id]
            print(f"Whiskey deleted: {deleted_name} (ID: {whiskey_id})") # Debug
        else:
            print(f"Warning: Whiskey ID {whiskey_id} not found for deletion.")

    def search_whiskeys(self, search_term: str) -> List[Whiskey]:
        """ 위스키 이름에서 검색어와 일치하는 위스키 목록을 반환합니다. """
        results = []
        if not search_term: # 검색어 없으면 전체 반환
            return list(self.whiskey_catalog.values())
        term_lower = search_term.lower()
        for whiskey in self.whiskey_catalog.values():
            if term_lower in whiskey.name.lower():
                results.append(whiskey)
        print(f"Searching for '{search_term}', found {len(results)} results.")
        return results

    def filter_whiskeys(self, filter_criteria: Dict[str, Any]) -> List[Whiskey]:
        """ 주어진 기준에 따라 위스키 목록을 필터링합니다. (UI에서는 직접 사용되지 않음) """
        print(f"Filtering with criteria: {filter_criteria}")
        filtered_list = list(self.whiskey_catalog.values())
        # 필터링 로직 (이전 코드와 동일)
        if 'type' in filter_criteria and filter_criteria['type'] is not None:
            target_type = filter_criteria['type']
            if isinstance(target_type, WhiskeyType): # 타입 객체 비교
                 filtered_list = [w for w in filtered_list if w.type == target_type]
        # ... 다른 필터 로직 ...
        print(f"  Filter result count: {len(filtered_list)}")
        return filtered_list

    def sort_whiskeys(self, whiskey_list: List[Whiskey], sort_criteria: str, reverse: bool = False) -> List[Whiskey]:
        """ 주어진 위스키 리스트를 특정 기준에 따라 정렬합니다. """
        print(f"Sorting list ({len(whiskey_list)} items) by '{sort_criteria}', reverse={reverse}")
        key_func: Optional[Callable[[Whiskey], Any]] = None
        none_sort_value_asc = float('inf') # 오름차순 시 None 값 처리 (맨 뒤)
        none_sort_value_desc = float('-inf') # 내림차순 시 None 값 처리 (맨 뒤)

        try:
            if sort_criteria == 'name':
                key_func = lambda w: w.name.lower() # 이름 정렬 시 대소문자 무시
            elif sort_criteria == 'price':
                key_func = lambda w: w.price if w.price is not None else (none_sort_value_desc if reverse else none_sort_value_asc)
            elif sort_criteria == 'alcohol_percentage':
                key_func = lambda w: w.alcohol_percentage if w.alcohol_percentage is not None else (none_sort_value_desc if reverse else none_sort_value_asc)
            elif sort_criteria == 'age':
                key_func = lambda w: w.age_years if w.age_years is not None else (none_sort_value_desc if reverse else none_sort_value_asc)
            # 맛 프로필 기준 정렬 필요시 추가
            # elif sort_criteria == 'sweetness': key_func = lambda w: w.taste_profile.sweetness

            if key_func:
                sorted_list = sorted(whiskey_list, key=key_func, reverse=reverse)
                return sorted_list
            else:
                print(f"Warning: Unknown sort criteria '{sort_criteria}'. Returning original list.")
                return whiskey_list
        except Exception as e:
            print(f"Error during sorting by {sort_criteria}: {e}")
            return whiskey_list # 정렬 실패 시 원본 반환