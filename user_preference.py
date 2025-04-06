# user_preference.py
from typing import Tuple, List, Optional

class User_Preference:
    """
    사용자의 위스키 취향 정보를 관리하는 클래스입니다.
    """
    def __init__(self, user_id: str):
        """ User_Preference 초기화 """
        self.user_id: str = user_id
        self.sweetness_preference: int = 3 # 기본값 예시 (0-5)
        self.smoky_preference: int = 3
        self.fruity_preference: int = 3
        self.spicy_preference: int = 3
        self.preferred_price_range: Tuple[Optional[int], Optional[int]] = (None, None) # (최소, 최대)
        # print(f"User_Preference initialized for user {self.user_id}") # Debug

    def update_preference(self, preference_type: str, value: int):
        """ 특정 맛 선호도를 업데이트합니다. (0~5 범위 강제) """
        try: # 값 타입 변환 오류 방지
             value = int(value)
             value = max(0, min(5, value)) # 0~5 범위 강제
        except (ValueError, TypeError):
             print(f"Warning: Invalid value type for preference update: {value}")
             return

        if preference_type == 'sweetness': self.sweetness_preference = value
        elif preference_type == 'smoky': self.smoky_preference = value
        elif preference_type == 'fruity': self.fruity_preference = value
        elif preference_type == 'spicy': self.spicy_preference = value
        else: print(f"Warning: Unknown preference type '{preference_type}'")

    def update_price_range(self, min_price: Optional[int], max_price: Optional[int]):
        """ 선호하는 가격 범위를 업데이트합니다. """
        # 입력값 타입 검증 및 변환
        try:
            p_min = int(min_price) if min_price is not None else None
            p_max = int(max_price) if max_price is not None else None

            # 음수 가격 방지
            if p_min is not None and p_min < 0: p_min = 0
            if p_max is not None and p_max < 0: p_max = 0

            # 최소 <= 최대 유효성 검사
            if p_min is not None and p_max is not None and p_min > p_max:
                 print(f"Warning: Invalid price range (min={p_min} > max={p_max}). Swapping.")
                 p_min, p_max = p_max, p_min # 값 교환

            self.preferred_price_range = (p_min, p_max)
            # print(f"Pref price range updated: {self.preferred_price_range}") # Debug
        except (ValueError, TypeError):
            print(f"Warning: Invalid price range values ({min_price}, {max_price}). Not updated.")


    def get_preference_score(self, preference_type: str) -> Optional[int]:
        """ 특정 맛 선호도 점수를 반환합니다. """
        if preference_type == 'sweetness': return self.sweetness_preference
        elif preference_type == 'smoky': return self.smoky_preference
        elif preference_type == 'fruity': return self.fruity_preference
        elif preference_type == 'spicy': return self.spicy_preference
        else: return None

    def get_price_range(self) -> Tuple[Optional[int], Optional[int]]:
        """ 선호하는 가격 범위를 반환합니다. """
        return self.preferred_price_range

    def get_preference_vector(self) -> List[int]:
        """ 모든 맛 선호도를 리스트(벡터) 형태로 반환합니다. """
        return [self.sweetness_preference, self.smoky_preference, self.fruity_preference, self.spicy_preference]

    def save_to_database(self):
        """ 데이터 저장 로직은 System 클래스에서 처리합니다. """
        pass

    def load_from_database(self, user_id: str):
        """ 데이터 로딩 로직은 System 클래스에서 처리합니다. """
        pass

    def __str__(self) -> str:
        price_str = f"Price: {self.preferred_price_range[0] or 'Any'}-{self.preferred_price_range[1] or 'Any'}"
        taste_str = f"Taste(Sw{self.sweetness_preference},Sm{self.smoky_preference},Fr{self.fruity_preference},Sp{self.spicy_preference})"
        return f"User: {self.user_id}, {taste_str}, {price_str}"