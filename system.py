# system.py
import os
import json
import datetime # datetime import 확인
from typing import Optional, Dict, List, Type, Tuple, Any # Tuple, Any 추가

# 필요한 클래스들 import
from user import User
from user_preference import User_Preference
from user_history import User_History
from user_review import User_Review
from whiskys import Whiskys
from whiskey import Whiskey, TasteProfile, WhiskeyType
from recommendation import Recommendation
from recommendation_preference import Recommendation_Preference
from recommendation_similar import Recommendation_Similar

# 데이터 저장 파일 경로 (예시)
DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "user_data.json")
WHISKEY_FILE = os.path.join(DATA_DIR, "whiskey_catalog.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")


class System:
    """
    애플리케이션 전체 시스템을 관리하고 조정하는 메인 클래스입니다.
    """
    def __init__(self):
        self.current_user: Optional[User] = None
        self.whiskey_catalog: Whiskys = Whiskys()
        self.all_reviews: Dict[str, User_Review] = {}
        self.recommendation_engine: Optional[Recommendation] = None
        self.ui_reference = None # UI 클래스에서 설정

        if not os.path.exists(DATA_DIR):
            try: # 디렉토리 생성 시 권한 문제 등 예외 처리 추가
                os.makedirs(DATA_DIR)
                print(f"Data directory created: {DATA_DIR}")
            except OSError as e:
                 print(f"Error creating data directory {DATA_DIR}: {e}")
                 # 여기서 프로그램 종료 또는 다른 경로 사용 등 처리 필요

        print("System initialized.")

    def set_ui_reference(self, ui):
        """UI 객체 참조를 설정합니다."""
        self.ui_reference = ui
        print("UI reference set in System.")

    def initialize(self) -> bool:
        """
        시스템을 초기화하고 사용자 정보 로딩 성공 여부를 반환합니다.

        Returns:
            bool: 사용자 정보 로딩 성공 여부 (True: 성공, False: 실패/없음)
        """
        print("System initializing...")
        if not self.load_whiskey_catalog(WHISKEY_FILE):
             print("Warning: Failed to load whiskey catalog.")
             # 기본 위스키 데이터 추가 로직 필요시 여기에...
             # self.add_default_whiskeys()

        user_loaded = self.load_system_state(USER_FILE, REVIEWS_FILE)

        if not user_loaded:
            print("No existing user data found or failed to load. User setup required.")
            return False # 사용자 로드 실패 -> False 반환
        else:
            print(f"System initialized successfully. Current user: {self.current_user.user_id if self.current_user else 'None'}")
            if self.current_user:
                # 기본 추천 엔진 설정 (예: 선호도 기반)
                self.set_recommendation_engine(Recommendation_Preference)
            print(f"Whiskey catalog size: {len(self.whiskey_catalog.get_all_whiskeys())}")
            print(f"Total reviews loaded: {len(self.all_reviews)}")
            return True # 사용자 로드 성공 -> True 반환

    def register_new_user(self, user_info: dict) -> bool:
        """새 사용자(초기 사용자)를 등록합니다."""
        if self.current_user:
            print(f"Cannot register new user. User {self.current_user.user_id} is already active.")
            return False
        user_id = user_info.get('user_id')
        user_name = user_info.get('user_name')
        if not user_id or not user_name:
            print("Error: New user registration requires 'user_id' and 'user_name'.")
            return False

        try: # 객체 생성 중 예외 발생 가능성 고려
            new_user = User(
                user_id=user_id, user_name=user_name,
                user_age=user_info.get('user_age'), user_sex=user_info.get('user_sex')
            )
            new_user.set_preference(User_Preference(user_id))
            new_user.set_history(User_History(user_id))

            self.current_user = new_user
            print(f"New user registered and set as current user: {user_id}")

            self.set_recommendation_engine(Recommendation_Preference) # 추천 엔진 설정
            self.save_system_state() # 새 사용자 정보 즉시 저장
            return True
        except Exception as e:
            print(f"Error registering new user: {e}")
            self.current_user = None # 실패 시 사용자 없음 상태 유지
            return False

    def get_current_user(self) -> Optional[User]:
        return self.current_user

    def set_recommendation_engine(self, engine_type: Type[Recommendation]):
        if self.current_user and self.whiskey_catalog:
            try:
                self.recommendation_engine = engine_type(self.current_user, self.whiskey_catalog)
                print(f"Recommendation engine set to: {engine_type.__name__}")
            except Exception as e:
                print(f"Error setting recommendation engine {engine_type.__name__}: {e}")
                self.recommendation_engine = None
        else:
            print("Cannot set recommendation engine: Current user or whiskey catalog not available.")
            self.recommendation_engine = None

    # --- 데이터 영속성 메서드 ---
    def save_system_state(self):
        """현재 사용자 관련 상태(정보, 선호도, 기록, 리뷰 ID) 및 전체 리뷰를 파일에 저장합니다."""
        if not self.current_user:
            print("No current user data to save.")
            return False
        print(f"Saving system state for user: {self.current_user.user_id}")

        user_data = { "user_info": {}, "preference": None, "history": None, "review_ids": [] }
        try: # 객체 접근 시 None 가능성 체크
            user_data["user_info"] = self.current_user.get_user_default_information()
            user_data["review_ids"] = self.current_user.get_review_ids()

            if self.current_user.user_preference:
                pref = self.current_user.user_preference
                user_data["preference"] = {
                    "sweetness": pref.sweetness_preference, "smoky": pref.smoky_preference,
                    "fruity": pref.fruity_preference, "spicy": pref.spicy_preference,
                    "price_range": pref.preferred_price_range
                }
            if self.current_user.user_history:
                hist = self.current_user.user_history
                viewed = [(wid, dt.isoformat()) for wid, dt in hist.viewed_whiskeys]
                user_data["history"] = { "viewed": viewed, "collection": hist.added_whiskeys }

            # 사용자 데이터 저장
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            print(f"User data saved to {USER_FILE}")

            # 전체 리뷰 데이터 저장
            reviews_to_save = {rid: review.get_review_details() for rid, review in self.all_reviews.items()}
            with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(reviews_to_save, f, indent=4, ensure_ascii=False)
            print(f"Reviews data saved to {REVIEWS_FILE}")
            return True

        except (IOError, TypeError, AttributeError) as e: # TypeError, AttributeError 추가
            print(f"Error saving system state: {e}")
            return False


    def load_system_state(self, user_file_path: str, reviews_file_path: str) -> bool:
        """파일에서 사용자 정보 및 전체 리뷰를 불러옵니다."""
        print("Loading system state...")
        user_loaded = False
        if os.path.exists(user_file_path):
            try:
                with open(user_file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                user_info = loaded_data.get("user_info")
                if user_info and 'user_id' in user_info:
                    loaded_user = User(
                        user_id=user_info['user_id'], user_name=user_info.get('user_name', 'Unknown'),
                        user_age=user_info.get('user_age'), user_sex=user_info.get('user_sex')
                    )
                    pref_data = loaded_data.get("preference")
                    if pref_data:
                        preference = User_Preference(loaded_user.user_id)
                        preference.sweetness_preference = pref_data.get('sweetness', 3)
                        preference.smoky_preference = pref_data.get('smoky', 3)
                        preference.fruity_preference = pref_data.get('fruity', 3)
                        preference.spicy_preference = pref_data.get('spicy', 3)
                        price_range_list = pref_data.get('price_range', [None, None])
                        preference.preferred_price_range = tuple(price_range_list)
                        loaded_user.set_preference(preference)
                    else: # 선호도 데이터 없으면 기본값으로 생성
                         loaded_user.set_preference(User_Preference(loaded_user.user_id))

                    hist_data = loaded_data.get("history")
                    if hist_data:
                        history = User_History(loaded_user.user_id)
                        history.added_whiskeys = hist_data.get('collection', [])
                        viewed_raw = hist_data.get('viewed', [])
                        for wid, dt_str in viewed_raw:
                            try: history.viewed_whiskeys.append((wid, datetime.datetime.fromisoformat(dt_str)))
                            except (ValueError, TypeError): print(f"Warn: Bad datetime '{dt_str}'")
                        loaded_user.set_history(history)
                    else: # 기록 데이터 없으면 기본값으로 생성
                         loaded_user.set_history(User_History(loaded_user.user_id))

                    loaded_user.user_review_ids = loaded_data.get("review_ids", [])
                    self.current_user = loaded_user
                    user_loaded = True
                    print(f"User data loaded successfully for: {self.current_user.user_id}")
                else: print("Error: Invalid user data format in file.")
            except (IOError, json.JSONDecodeError, TypeError) as e: # TypeError 추가
                print(f"Error loading user data from {user_file_path}: {e}")
                self.current_user = None
        else: print(f"User data file not found: {user_file_path}")

        # 리뷰 데이터 로드 (사용자 로드 성공 여부와 관계없이 시도)
        if os.path.exists(reviews_file_path):
            try:
                with open(reviews_file_path, 'r', encoding='utf-8') as f:
                    loaded_reviews = json.load(f)
                self.all_reviews.clear()
                for review_id, review_data in loaded_reviews.items():
                    try:
                        review_dt = datetime.datetime.fromisoformat(review_data['review_date'])
                        review = User_Review(
                            review_id=review_id, user_id=review_data['user_id'],
                            whiskey_id=review_data['whiskey_id'], rating=review_data['rating'],
                            review_text=review_data.get('review_text', '')
                        )
                        review.review_date = review_dt
                        self.all_reviews[review_id] = review
                    except (KeyError, ValueError, TypeError) as e:
                        print(f"Warn: Skipping invalid review data ID {review_id}: {e}")
                print(f"Reviews data loaded. Total: {len(self.all_reviews)}")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading reviews data from {reviews_file_path}: {e}")
        else: print(f"Reviews data file not found: {reviews_file_path}")

        return user_loaded # 최종적으로 사용자 로드 성공 여부 반환

    def save_whiskey_catalog(self, file_path: str):
        """위스키 카탈로그 정보를 파일에 저장합니다."""
        print(f"Saving whiskey catalog to {file_path}...")
        catalog_data = {}
        try: # get_all_whiskeys 호출 등에서 예외 발생 가능
            for whiskey_id, whiskey in self.whiskey_catalog.get_all_whiskeys().items():
                 details = whiskey.get_full_details()
                 # 객체는 JSON 직렬화 가능한 형태로 변환
                 details['taste_profile'] = whiskey.taste_profile.get_vector()
                 details['type'] = whiskey.type.name # Enum 이름 사용
                 # user_review_ids는 이미 리스트이므로 그대로 사용
                 catalog_data[whiskey_id] = details

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(catalog_data, f, indent=4, ensure_ascii=False)
            print("Whiskey catalog saved successfully.")
            return True
        except (IOError, TypeError, AttributeError) as e:
            print(f"Error saving whiskey catalog: {e}")
            return False

    def load_whiskey_catalog(self, file_path: str) -> bool:
        """파일에서 위스키 카탈로그 정보를 불러옵니다."""
        print(f"Loading whiskey catalog from {file_path}...")
        if not os.path.exists(file_path):
            print(f"Whiskey catalog file not found: {file_path}")
            return False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_catalog = json.load(f)
            self.whiskey_catalog = Whiskys() # 카탈로그 재생성
            for whiskey_id, data in loaded_catalog.items():
                try:
                    taste_vector = data['taste_profile']
                    taste_profile = TasteProfile(*taste_vector)
                    type_name = data['type']
                    whiskey_type = WhiskeyType[type_name]

                    whiskey = Whiskey(
                        whiskey_id=whiskey_id, name=data['name'], taste_profile=taste_profile,
                        origin=data['origin'], price=data['price'],
                        alcohol_percentage=data['alcohol_percentage'], whiskey_type=whiskey_type,
                        image_path=data.get('image_path'), age_years=data.get('age_years')
                    )
                    whiskey.user_review_ids = data.get('user_review_ids', []) # 리뷰 ID 목록 복원
                    self.whiskey_catalog.add_whiskey(whiskey)
                except (KeyError, ValueError, TypeError, AttributeError) as e:
                     print(f"Warn: Skipping invalid whiskey data ID {whiskey_id}: {e}")
            print(f"Whiskey catalog loaded. Total: {len(self.whiskey_catalog.get_all_whiskeys())}")
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading whiskey catalog from {file_path}: {e}")
            return False

    # --- UI 편의 메서드 ---
    def get_all_whiskey_list_for_display(self) -> List[dict]:
        all_whiskies = self.whiskey_catalog.get_all_whiskeys().values()
        return [w.get_basic_info() for w in all_whiskies]

    def get_whiskey_details_for_display(self, whiskey_id: str) -> Optional[dict]:
        whiskey = self.whiskey_catalog.get_whiskey_details(whiskey_id)
        return whiskey.get_full_details() if whiskey else None

    # filter_and_sort_whiskeys_for_display 제거 (UI에서 직접 search, sort 호출)

    def create_and_add_review(self, whiskey_id: str, rating: int, text: str) -> Optional[User_Review]:
        if not self.current_user: return None
        whiskey = self.whiskey_catalog.get_whiskey_details(whiskey_id)
        if not whiskey: return None
        # 간단한 리뷰 ID 생성 (더 견고한 방식 권장: uuid 사용 등)
        review_id = f"rev_{self.current_user.user_id}_{whiskey_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        try: # 객체 생성 시 예외 처리
            new_review = User_Review(review_id, self.current_user.user_id, whiskey_id, rating, text)
            self.all_reviews[review_id] = new_review
            self.current_user.add_review_id(review_id)
            whiskey.add_review_id(review_id)
            print(f"Review {review_id} created and added.")
            # self.save_system_state() # 리뷰 추가 시 즉시 저장 필요하면 호출
            return new_review
        except Exception as e:
            print(f"Error creating review: {e}")
            return None

    def get_reviews_for_whiskey(self, whiskey_id: str) -> List[User_Review]:
        return [review for review in self.all_reviews.values() if review.whiskey_id == whiskey_id]

    def get_reviews_by_user(self, user_id: str) -> List[User_Review]:
         if self.current_user and self.current_user.user_id == user_id:
             user_review_ids = self.current_user.get_review_ids()
             return [self.all_reviews[rid] for rid in user_review_ids if rid in self.all_reviews]
         else: # 현재 사용자가 아닌 경우 (필요 시 구현)
             return [review for review in self.all_reviews.values() if review.user_id == user_id]

    def get_recommendations(self, count: int, method_type: Optional[str] = None, base_whiskey_id: Optional[str] = None) -> List[dict]:
        """추천 목록을 받아 UI용 기본 정보 리스트로 반환합니다."""
        engine_to_use = self.recommendation_engine
        if not self.current_user:
             print("Error: Cannot get recommendations. No user logged in.")
             return []

        temp_engine = None # 임시 엔진 사용 플래그
        if method_type: # 특정 엔진 타입 요청 시
            target_engine_type = None
            if method_type == 'preference': target_engine_type = Recommendation_Preference
            elif method_type == 'similar': target_engine_type = Recommendation_Similar

            if target_engine_type and not isinstance(engine_to_use, target_engine_type):
                 print(f"Temporarily using {target_engine_type.__name__} for recommendation.")
                 try: # 임시 엔진 생성
                      temp_engine = target_engine_type(self.current_user, self.whiskey_catalog)
                      engine_to_use = temp_engine
                 except Exception as e:
                      print(f"Error creating temporary engine {target_engine_type.__name__}: {e}")
                      engine_to_use = self.recommendation_engine # 실패 시 기존 엔진 사용
            elif isinstance(engine_to_use, target_engine_type):
                 print(f"Current engine is already {target_engine_type.__name__}.")
            else: # method_type은 지정됐으나 해당 타입 엔진 사용 불가 시
                 print(f"Warning: Cannot switch to engine type {method_type}. Using current engine.")


        if not engine_to_use:
            print("Error: Recommendation engine is not available.")
            return []

        try:
            # 유사 추천 시 기준 ID 전달 (엔진 클래스 수정 필요 가능성)
            if isinstance(engine_to_use, Recommendation_Similar) and base_whiskey_id:
                 # Recommendation_Similar에 기준 ID를 받는 get_recommendations 구현 또는
                 # find_similar_whiskeys 를 직접 호출하도록 수정 필요.
                 # 임시: find_similar_whiskeys 직접 호출
                 print(f"Calling find_similar_whiskeys for {base_whiskey_id}")
                 recommended_ids = engine_to_use.find_similar_whiskeys(base_whiskey_id, count)
            else:
                 recommended_ids = engine_to_use.get_recommendations(count)

            results = []
            for rec_id in recommended_ids:
                whiskey = self.whiskey_catalog.get_whiskey_details(rec_id)
                if whiskey: results.append(whiskey.get_basic_info())
                else: print(f"Warn: Recommended whiskey ID {rec_id} not found.")
            return results
        except Exception as e:
            print(f"Error getting recommendations from {type(engine_to_use).__name__}: {e}")
            # traceback.print_exc() # 디버깅 시 스택 트레이스 출력
            return []

    def run(self):
        """애플리케이션 메인 실행 함수"""
        print("Application starting...")
        
        # PyQt5 관련 모듈 import (시스템 클래스 내에서도 임포트)
        from PyQt5.QtWidgets import QApplication, QMessageBox
        import sys
        
        # PyQt5 애플리케이션 인스턴스 생성
        app = QApplication(sys.argv)
        print("QApplication instance created.")
        
        # 시스템 초기화 결과 확인
        initialization_successful = self.initialize()
        print(f"System initialization attempt finished. User loaded: {initialization_successful}")
        
        # UI 모듈 import (런타임에 임포트하여 순환 참조 방지)
        from ui import MainWindow
        
        # MainWindow 인스턴스 생성
        main_window = MainWindow(system_reference=self)
        print("MainWindow instance created.")
        
        # 사용자 설정 필요 시 UI 호출
        if not initialization_successful:
            print("Requesting user setup from UI...")
            # MainWindow에 사용자 설정을 요청하는 메서드 호출
            if not main_window.prompt_for_user_setup():
                # 사용자 설정이 취소되거나 실패하면 프로그램 종료
                print("User setup cancelled or failed. Exiting.")
                QMessageBox.critical(None, "사용자 설정 오류", "초기 사용자 설정이 필요합니다. 프로그램을 종료합니다.")
                sys.exit(1)
            else:
                # 사용자 설정 성공 후 UI에 초기 데이터 다시 로드/표시
                print("User setup complete. Reloading initial data for UI.")
                main_window.load_initial_data() # UI에 데이터 표시
        
        # 메인 윈도우 표시
        main_window.show()
        print("MainWindow shown.")
        
        # PyQt5 이벤트 루프 시작
        print("Starting PyQt5 event loop...")
        exit_code = app.exec_()
        print(f"Application finished with exit code: {exit_code}")
        
        # 종료 전 상태 저장
        self.save_system_state()
        
        sys.exit(exit_code)

# 프로그램 메인 실행 지점
if __name__ == '__main__':
    system = System()
    system.run()