import os
import json
import datetime
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
# 클래스 임포트
from user import User
from user_preference import User_Preference
from user_history import User_History
from user_review import User_Review
from whiskys import Whiskys
from whiskey import Whiskey
from taste_profile import TasteProfile
from whiskey_type import WhiskeyType
from recommendation_preference import Recommendation_Preference
from recommendation_similar import Recommendation_Similar

# 데이터 경로
DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "user_data.json")
WHISKEY_FILE = os.path.join(DATA_DIR, "whiskey_catalog.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")

class System:
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Singleton이므로 초기화는 한 번만 수행
        if System._initialized:
            return
        
        self.current_user = None
        self.whiskey_catalog = Whiskys()
        self.all_reviews = {}
        self.recommendation_engine = None
        self.ui_reference = None
        
        # 데이터 디렉토리 생성
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        System._initialized = True
        print("시스템 초기화 완료 (Singleton)")
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def set_ui_reference(self, ui):
        
        self.ui_reference = ui
        print("UI 참조 설정 완료")
    
    def initialize(self):
        
        print("시스템 초기화 중...")
        
        # 위스키 카탈로그 로드
        if not self.load_whiskey_catalog():
            print("위스키 데이터 로드 실패")
        
        # 사용자 데이터 로드
        user_loaded = self.load_system_state()
        
        if user_loaded:
            print(f"사용자 로드 성공: {self.current_user.user_id}")
            # 추천 엔진 설정
            self.set_recommendation_engine(Recommendation_Preference)
            return True
        else:
            print("사용자 데이터 없음")
            return False
        
    # Factory Method Pattern: 사용자 및 관련 객체들 생성
    def register_new_user(self, user_info):

        user_id = user_info.get('user_id')
        user_name = user_info.get('user_name')
        
        if not user_id or not user_name:
            print("사용자 ID와 이름이 필요합니다")
            return False
        
        # 새 사용자 생성 (Factory Method)
        new_user = User(user_id, user_name)
        new_user.set_preference(User_Preference(user_id))
        new_user.set_history(User_History(user_id))
        
        self.current_user = new_user
        self.set_recommendation_engine(Recommendation_Preference)
        self.save_system_state()
        
        return True
    
    def get_current_user(self):
        return self.current_user
    
    def set_recommendation_engine(self, engine_type):
        
        try:
            self.recommendation_engine = engine_type(self.current_user, self.whiskey_catalog)
            print(f"추천 엔진 설정: {engine_type.__name__}")
        except Exception as e:
            print(f"추천 엔진 설정 오류: {e}")
            self.recommendation_engine = None
    
    def save_system_state(self):
        """시스템 상태 저장"""
        if not self.current_user:
            print("저장할 사용자 데이터가 없습니다")
            return False
        
        # 사용자 데이터 구성
        user_data = {
            "user_info": self.current_user.get_user_default_information(),
            "review_ids": self.current_user.get_review_ids(),
            "preference": None,
            "history": None
        }
        
        # 선호도 데이터
        if self.current_user.get_preference():
            pref = self.current_user.get_preference()
            user_data["preference"] = {
                "body": pref.body_preference,
                "richness": pref.richness_preference,
                "smoke": pref.smoke_preference,
                "sweetness": pref.sweetness_preference,
                "price_range": [pref.preferred_price_range[0], pref.preferred_price_range[1]]
            }
        
        # 기록 데이터
        if self.current_user.get_history():
            hist = self.current_user.get_history()
            viewed = [(wid, dt.isoformat()) for wid, dt in hist.viewed_whiskeys]
            user_data["history"] = {
                "viewed": viewed,
                "collection": hist.get_collection()
            }
        
        # 파일 저장
        try:
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            
            # 리뷰 저장
            reviews_to_save = {}
            for rid, review in self.all_reviews.items():
                reviews_to_save[rid] = review.get_review_details()
            
            with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(reviews_to_save, f, indent=4, ensure_ascii=False)
            
            print("시스템 상태 저장 완료")
            return True
        except Exception as e:
            print(f"저장 오류: {e}")
            return False
    
    def load_system_state(self):
        # 사용자 데이터 로드
        user_loaded = False
        
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                user_info = loaded_data.get("user_info")
                if user_info and 'user_id' in user_info:
                    # 사용자 생성
                    loaded_user = User(
                        user_id=user_info['user_id'],
                        user_name=user_info.get('user_name', '사용자'),
                        user_age=user_info.get('user_age'),
                        user_sex=user_info.get('user_sex')
                    )
                    
                    # 선호도 설정
                    pref_data = loaded_data.get("preference")
                    if pref_data:
                        preference = User_Preference(loaded_user.user_id)
                        preference.sweetness_preference = pref_data.get('sweetness', 3)
                        preference.smoke_preference = pref_data.get('smoke', 3)
                        preference.richness_preference = pref_data.get('richness', 3)
                        preference.body_preference = pref_data.get('body', 3)
                        
                        price_range = pref_data.get('price_range', [None, None])
                        preference.preferred_price_range = (price_range[0], price_range[1])
                        
                        loaded_user.set_preference(preference)
                    else:
                        loaded_user.set_preference(User_Preference(loaded_user.user_id))
                    
                    # 기록 설정
                    hist_data = loaded_data.get("history")
                    if hist_data:
                        history = User_History(loaded_user.user_id)
                        history.added_whiskeys = hist_data.get('collection', [])
                        
                        viewed_raw = hist_data.get('viewed', [])
                        for wid, dt_str in viewed_raw:
                            try:
                                history.viewed_whiskeys.append(
                                    (wid, datetime.datetime.fromisoformat(dt_str))
                                )
                            except:
                                print(f"날짜 변환 오류: {dt_str}")
                        
                        loaded_user.set_history(history)
                    else:
                        loaded_user.set_history(User_History(loaded_user.user_id))
                    
                    # 리뷰 ID 설정
                    loaded_user.user_review_ids = loaded_data.get("review_ids", [])
                    
                    self.current_user = loaded_user
                    user_loaded = True
                    print(f"사용자 데이터 로드 완료: {self.current_user.user_id}")
            except Exception as e:
                print(f"사용자 데이터 로드 오류: {e}")
        
        # 리뷰 데이터 로드
        if os.path.exists(REVIEWS_FILE):
            try:
                with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                    loaded_reviews = json.load(f)
                
                self.all_reviews = {}
                for review_id, review_data in loaded_reviews.items():
                    try:
                        review = User_Review(
                            review_id=review_id,
                            user_id=review_data['user_id'],
                            whiskey_id=review_data['whiskey_id'],
                            rating=review_data['rating'],
                            review_text=review_data.get('review_text', '')
                        )
                        
                        if 'review_date' in review_data:
                            review.review_date = datetime.datetime.fromisoformat(
                                review_data['review_date']
                            )
                        
                        self.all_reviews[review_id] = review
                    except Exception as e:
                        print(f"리뷰 데이터 오류 (ID {review_id}): {e}")
                
                print(f"리뷰 {len(self.all_reviews)}개 로드 완료")
            except Exception as e:
                print(f"리뷰 데이터 로드 오류: {e}")
        
        return user_loaded
    
    def load_whiskey_catalog(self):
        
        if not os.path.exists(WHISKEY_FILE):
            print(f"위스키 카탈로그 파일이 없습니다: {WHISKEY_FILE}")
            return False
        
        try:
            with open(WHISKEY_FILE, 'r', encoding='utf-8') as f:
                loaded_catalog = json.load(f)
            
            for whiskey_id, data in loaded_catalog.items():
                try:
                    # 맛 프로필 생성
                    taste_vector = data.get('taste_profile', [3, 3, 3, 3])
                    if isinstance(taste_vector, list) and len(taste_vector) == 4:
                        taste_profile = TasteProfile(*taste_vector)
                    else:
                        taste_profile = TasteProfile(3, 3, 3, 3)
                    
                    # 위스키 타입 설정
                    try:
                        type_name = data['type']
                        whiskey_type = WhiskeyType[type_name]
                    except:
                        whiskey_type = WhiskeyType.OTHER
                    
                    # 위스키 생성
                    whiskey = Whiskey(
                        whiskey_id=whiskey_id,
                        name=data['name'],
                        taste_profile=taste_profile,
                        origin=data.get('origin', '미상'),
                        price=data.get('price', 0),
                        alcohol_percentage=data.get('alcohol_percentage', 40.0),
                        whiskey_type=whiskey_type,
                        image_path=data.get('image_path'),
                        age_years=data.get('age_years')
                    )
                    
                    # 리뷰 ID 설정
                    whiskey.user_review_ids = data.get('user_review_ids', [])
                    
                    self.whiskey_catalog.add_whiskey(whiskey)
                except Exception as e:
                    print(f"위스키 데이터 오류 (ID {whiskey_id}): {e}")
            
            print(f"위스키 {len(self.whiskey_catalog.get_all_whiskeys())}개 로드 완료")
            return True
        except Exception as e:
            print(f"위스키 카탈로그 로드 오류: {e}")
            return False
    
    
    def get_whiskey_details_for_display(self, whiskey_id):
        
        whiskey = self.whiskey_catalog.get_whiskey_details(whiskey_id)
        return whiskey.get_full_details() if whiskey else None
    
    def create_and_add_review(self, whiskey_id, rating, text):
        """
        Factory Method Pattern: 리뷰 객체 생성 및 시스템 등록
        - 복잡한 리뷰 ID 생성 규칙
        - 리뷰 객체 생성과 시스템 등록을 한 번에 처리
        """
        if not self.current_user:
            return None
        
        whiskey = self.whiskey_catalog.get_whiskey_details(whiskey_id)
        if not whiskey:
            return None
        
        # Factory Method: 리뷰 ID 생성 규칙
        review_id = f"rev_{self.current_user.user_id}_{whiskey_id}_{int(datetime.datetime.now().timestamp())}"
        
        # Factory Method: 리뷰 생성 및 시스템 등록
        new_review = User_Review(review_id, self.current_user.user_id, whiskey_id, rating, text)
        
        # 시스템에 등록
        self.all_reviews[review_id] = new_review
        self.current_user.add_review_id(review_id)
        whiskey.add_review_id(review_id)
        
        # 사용자 히스토리에 리뷰 작성 위스키 추가
        history = self.current_user.get_history()
        if history:
            history.add_reviewed_whiskey(whiskey_id)
        
        print(f"리뷰 생성 완료: {review_id}")
        return new_review
    
    def save_system_state(self):
        if not self.current_user:
            print("저장할 사용자 데이터가 없습니다")
            return False
        
        # 사용자 데이터 구성
        user_data = {
            "user_info": self.current_user.get_user_default_information(),
            "review_ids": self.current_user.get_review_ids(),
            "preference": None,
            "history": None
        }
        
        # 선호도 데이터
        if self.current_user.get_preference():
            pref = self.current_user.get_preference()
            user_data["preference"] = {
                "body": pref.body_preference,
                "richness": pref.richness_preference,
                "smoke": pref.smoke_preference,
                "sweetness": pref.sweetness_preference,
                "price_range": [pref.preferred_price_range[0], pref.preferred_price_range[1]]
            }
        
        # 기록 데이터
        if self.current_user.get_history():
            hist = self.current_user.get_history()
            viewed = [(wid, dt.isoformat()) for wid, dt in hist.viewed_whiskeys]
            user_data["history"] = {
                "viewed": viewed,
                "collection": hist.get_collection(),
                "reviewed": hist.get_reviewed_whiskeys()  # 리뷰 작성한 위스키 목록 추가
            }
        
        # 파일 저장
        try:
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            
            # 리뷰 저장
            reviews_to_save = {}
            for rid, review in self.all_reviews.items():
                reviews_to_save[rid] = review.get_review_details()
            
            with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(reviews_to_save, f, indent=4, ensure_ascii=False)
            
            print("시스템 상태 저장 완료")
            return True
        except Exception as e:
            print(f"저장 오류: {e}")
            return False
    def load_system_state(self):
        # 사용자 데이터 로드
        user_loaded = False
        
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                user_info = loaded_data.get("user_info")
                if user_info and 'user_id' in user_info:
                    # 사용자 생성
                    loaded_user = User(
                        user_id=user_info['user_id'],
                        user_name=user_info.get('user_name', '사용자'),
                        user_age=user_info.get('user_age'),
                        user_sex=user_info.get('user_sex')
                    )
                    
                    # 선호도 설정
                    pref_data = loaded_data.get("preference")
                    if pref_data:
                        preference = User_Preference(loaded_user.user_id)
                        preference.sweetness_preference = pref_data.get('sweetness', 3)
                        preference.smoke_preference = pref_data.get('smoke', 3)
                        preference.richness_preference = pref_data.get('richness', 3)
                        preference.body_preference = pref_data.get('body', 3)
                        
                        price_range = pref_data.get('price_range', [None, None])
                        preference.preferred_price_range = (price_range[0], price_range[1])
                        
                        loaded_user.set_preference(preference)
                    else:
                        loaded_user.set_preference(User_Preference(loaded_user.user_id))
                    
                    # 기록 설정
                    hist_data = loaded_data.get("history")
                    if hist_data:
                        history = User_History(loaded_user.user_id)
                        history.added_whiskeys = hist_data.get('collection', [])
                        history.reviewed_whiskeys = hist_data.get('reviewed', [])  # 리뷰 작성한 위스키 목록 로드
                        
                        viewed_raw = hist_data.get('viewed', [])
                        for wid, dt_str in viewed_raw:
                            try:
                                history.viewed_whiskeys.append(
                                    (wid, datetime.datetime.fromisoformat(dt_str))
                                )
                            except:
                                print(f"날짜 변환 오류: {dt_str}")
                        
                        loaded_user.set_history(history)
                    else:
                        loaded_user.set_history(User_History(loaded_user.user_id))
                    
                    # 리뷰 ID 설정
                    loaded_user.user_review_ids = loaded_data.get("review_ids", [])
                    
                    self.current_user = loaded_user
                    user_loaded = True
                    print(f"사용자 데이터 로드 완료: {self.current_user.user_id}")
            except Exception as e:
                print(f"사용자 데이터 로드 오류: {e}")
        
        # 리뷰 데이터 로드
        if os.path.exists(REVIEWS_FILE):
            try:
                with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                    loaded_reviews = json.load(f)
                
                self.all_reviews = {}
                for review_id, review_data in loaded_reviews.items():
                    try:
                        review = User_Review(
                            review_id=review_id,
                            user_id=review_data['user_id'],
                            whiskey_id=review_data['whiskey_id'],
                            rating=review_data['rating'],
                            review_text=review_data.get('review_text', '')
                        )
                        
                        if 'review_date' in review_data:
                            review.review_date = datetime.datetime.fromisoformat(
                                review_data['review_date']
                            )
                        
                        self.all_reviews[review_id] = review
                    except Exception as e:
                        print(f"리뷰 데이터 오류 (ID {review_id}): {e}")
                
                print(f"리뷰 {len(self.all_reviews)}개 로드 완료")
            except Exception as e:
                print(f"리뷰 데이터 로드 오류: {e}")
        
        return user_loaded
    
    def get_user_reviewed_whiskeys(self):
        if not self.current_user:
            return []
        
        history = self.current_user.get_history()
        if not history:
            return []
        
        reviewed_ids = history.get_reviewed_whiskeys()
        reviewed_whiskeys = []
        
        for whiskey_id in reviewed_ids:
            whiskey = self.whiskey_catalog.get_whiskey_details(whiskey_id)
            if whiskey:
                reviewed_whiskeys.append(whiskey.get_basic_info())
        
        return reviewed_whiskeys
    
    def get_reviews_for_whiskey(self, whiskey_id):
        return [review for review in self.all_reviews.values() 
                if review.whiskey_id == whiskey_id]
    
    def get_recommendations(self, count, method_type=None, base_whiskey_id=None):
        if not self.current_user:
            print("사용자 정보 없음, 추천 불가")
            return []
        
        engine_to_use = self.recommendation_engine
        
        # 추천 방식에 따른 엔진 선택
        if method_type:
            if method_type == 'preference' and not isinstance(engine_to_use, Recommendation_Preference):
                engine_to_use = Recommendation_Preference(self.current_user, self.whiskey_catalog)
            elif method_type == 'similar' and not isinstance(engine_to_use, Recommendation_Similar):
                engine_to_use = Recommendation_Similar(self.current_user, self.whiskey_catalog)
        
        if not engine_to_use:
            print("추천 엔진 없음")
            return []
        
        # 추천 받기
        try:
            if isinstance(engine_to_use, Recommendation_Similar) and base_whiskey_id:
                recommended_ids = engine_to_use.find_similar_whiskeys(base_whiskey_id, count)
            else:
                recommended_ids = engine_to_use.get_recommendations(count)
            
            # 결과 구성
            results = []
            for rec_id in recommended_ids:
                whiskey = self.whiskey_catalog.get_whiskey_details(rec_id)
                if whiskey:
                    results.append(whiskey.get_basic_info())
            
            return results
        except Exception as e:
            print(f"추천 오류: {e}")
            return []
    
    def run(self):
        print("애플리케이션 시작...")
        
        # PyQt5 모듈 임포트
        from PyQt5.QtWidgets import QApplication, QMessageBox
        import sys
        
        # 애플리케이션 생성
        app = QApplication(sys.argv)
        
        # UI 임포트
        from ui import MainWindow
        
        # Singleton 시스템 사용
        system_instance = System.get_instance()
        
        # 메인 윈도우 생성 (Singleton 시스템 전달)
        main_window = MainWindow(system_reference=system_instance)
        
        # 초기화 확인
        initialization_successful = system_instance.initialize()
        
        # 사용자 설정 필요 시
        if not initialization_successful:
            print("사용자 설정 필요")
            if not main_window.prompt_for_user_setup():
                QMessageBox.critical(None, "오류", "사용자 설정이 필요합니다. 프로그램을 종료합니다.")
                sys.exit(1)
            else:
                main_window.load_initial_data()
        else:
            # 정상 로드 시 초기 데이터 표시
            main_window.load_initial_data()
        
        # 창 표시 (이 부분이 중요!)
        main_window.show()
        
        # 이벤트 루프 실행
        exit_code = app.exec_()
        
        # 종료 전 상태 저장
        system_instance.save_system_state()
        
        sys.exit(exit_code)

# 프로그램 실행 진입점
if __name__ == '__main__':
    system = System()
    system.run()