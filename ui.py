# ui.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QLabel, QTextEdit, QPushButton, QLineEdit,
                             QSlider, QSpinBox, QComboBox, QTabWidget, QSplitter,
                             QMessageBox, QListWidgetItem, QGridLayout, QFormLayout,
                             QDialog, QDialogButtonBox, QInputDialog) # QInputDialog 확인
from PyQt5.QtCore import Qt, pyqtSlot, QObject
from PyQt5.QtGui import QIntValidator

from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from system import System
    from user_preference import User_Preference
    from user_history import User_History
    from user_review import User_Review

# UI 클래스가 메인 윈도우 역할을 하도록 QMainWindow 상속
class MainWindow(QMainWindow):
    """
    메인 애플리케이션 윈도우 클래스 (PyQt5 QMainWindow 상속)
    """
    def __init__(self, system_reference: 'System', parent=None):
        super().__init__(parent)
        self.system_reference = system_reference
        # 시스템 객체에 UI 참조 설정 요청
        if hasattr(self.system_reference, 'set_ui_reference'):
            self.system_reference.set_ui_reference(self)

        self.current_selected_whiskey_id: Optional[str] = None # 현재 선택된 위스키 ID 저장

        self.setWindowTitle("위스키 추천 시스템")
        self.setGeometry(100, 100, 1200, 700) # 창 위치와 크기 설정

        self.init_ui() # UI 요소 생성 및 배치 메서드 호출
        # 초기 데이터 로드는 main.py에서 initialize 결과 확인 후 호출

    def init_ui(self):
        """UI 요소들을 생성하고 배치합니다."""
        # --- 메인 레이아웃 설정 (좌우 분할) ---
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal) # 좌우 크기 조절 가능한 분할자
        main_layout.addWidget(splitter)

        # --- 왼쪽 패널: 위스키 목록 ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # --- 검색 및 전체보기 레이아웃 (수정됨) ---
        search_layout = QHBoxLayout() # 검색창과 전체보기 버튼을 가로로 배치
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("위스키 이름 검색...")
        self.search_input.textChanged.connect(self.on_search_changed) # 텍스트 변경 시 슬롯 연결
        search_layout.addWidget(self.search_input) # 검색창 추가

        # *** "전체 목록 보기" 버튼 추가됨 ***
        self.show_all_button = QPushButton("전체 목록")
        self.show_all_button.setToolTip("검색어를 지우고 전체 위스키 목록을 표시합니다.") # 버튼 툴팁
        self.show_all_button.clicked.connect(self.on_show_all_clicked) # 버튼 클릭 시 슬롯 연결
        search_layout.addWidget(self.show_all_button) # 버튼 추가
        # --- 검색 및 전체보기 레이아웃 끝 ---

        left_layout.addLayout(search_layout) # 검색 관련 레이아웃을 왼쪽 패널에 추가

        # 정렬 옵션
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(QLabel("정렬:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(['이름 (오름차순)', '이름 (내림차순)', '가격 (낮은순)', '가격 (높은순)', '도수 (낮은순)', '도수 (높은순)'])
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        sort_layout.addWidget(self.sort_combo)
        left_layout.addLayout(sort_layout)

        # 위스키 목록 리스트 위젯
        self.whiskey_list_widget = QListWidget()
        self.whiskey_list_widget.itemSelectionChanged.connect(self.on_whiskey_selected)
        left_layout.addWidget(self.whiskey_list_widget)

        splitter.addWidget(left_panel)

        # --- 오른쪽 패널: 탭 위젯 ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.tab_widget = QTabWidget()
        right_layout.addWidget(self.tab_widget)

        # 탭 생성
        self.init_details_tab()
        self.init_preference_tab()
        self.init_history_tab()
        self.init_recommend_tab()
        self.init_review_tab()

        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800]) # 초기 분할 비율

    def init_details_tab(self):
        """상세 정보 탭 UI 생성"""
        self.details_tab = QWidget()
        layout = QVBoxLayout(self.details_tab)
        form_layout = QFormLayout()

        self.detail_name_label = QLabel("N/A")
        self.detail_origin_label = QLabel("N/A")
        self.detail_type_label = QLabel("N/A")
        self.detail_price_label = QLabel("N/A")
        self.detail_abv_label = QLabel("N/A")
        self.detail_age_label = QLabel("N/A")
        self.detail_taste_label = QLabel("N/A")

        form_layout.addRow("이름:", self.detail_name_label)
        form_layout.addRow("원산지:", self.detail_origin_label)
        form_layout.addRow("타입:", self.detail_type_label)
        form_layout.addRow("가격:", self.detail_price_label)
        form_layout.addRow("도수:", self.detail_abv_label)
        form_layout.addRow("숙성연수:", self.detail_age_label)
        form_layout.addRow("맛 프로필:", self.detail_taste_label)
        layout.addLayout(form_layout)

        self.add_collection_button = QPushButton("내 컬렉션에 추가")
        self.add_collection_button.clicked.connect(self.on_add_to_collection_clicked)
        layout.addWidget(self.add_collection_button)
        self.add_collection_button.setEnabled(False)

        layout.addStretch(1)
        self.tab_widget.addTab(self.details_tab, "상세 정보")

    def init_preference_tab(self):
        """사용자 선호도 탭 UI 생성"""
        self.preference_tab = QWidget()
        layout = QVBoxLayout(self.preference_tab)
        grid_layout = QGridLayout()

        self.pref_sweet_slider = QSlider(Qt.Horizontal)
        self.pref_smoky_slider = QSlider(Qt.Horizontal)
        self.pref_fruity_slider = QSlider(Qt.Horizontal)
        self.pref_spicy_slider = QSlider(Qt.Horizontal)
        sliders = [self.pref_sweet_slider, self.pref_smoky_slider, self.pref_fruity_slider, self.pref_spicy_slider]
        slider_labels = ["단맛", "스모키", "과일향", "스파이시"]
        self.pref_value_labels = {}

        for i, slider in enumerate(sliders):
            slider.setRange(0, 5)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            value_label = QLabel("3")
            self.pref_value_labels[slider_labels[i]] = value_label
            slider.valueChanged.connect(lambda value, lbl=value_label: lbl.setText(str(value)))

            grid_layout.addWidget(QLabel(slider_labels[i]), i, 0)
            grid_layout.addWidget(slider, i, 1)
            grid_layout.addWidget(value_label, i, 2)
        layout.addLayout(grid_layout)

        price_layout = QHBoxLayout()
        self.pref_price_min_input = QLineEdit()
        self.pref_price_min_input.setPlaceholderText("최소 가격 (숫자만)")
        self.pref_price_min_input.setValidator(QIntValidator(0, 9999999))
        self.pref_price_max_input = QLineEdit()
        self.pref_price_max_input.setPlaceholderText("최대 가격 (숫자만)")
        self.pref_price_max_input.setValidator(QIntValidator(0, 9999999))

        price_layout.addWidget(QLabel("선호 가격대:"))
        price_layout.addWidget(self.pref_price_min_input)
        price_layout.addWidget(QLabel("~"))
        price_layout.addWidget(self.pref_price_max_input)
        layout.addLayout(price_layout)

        self.save_prefs_button = QPushButton("선호도 저장")
        self.save_prefs_button.clicked.connect(self.on_save_prefs_clicked)
        layout.addWidget(self.save_prefs_button)

        layout.addStretch(1)
        self.tab_widget.addTab(self.preference_tab, "나의 선호도")

    def init_history_tab(self):
        """활동 기록 탭 UI 생성"""
        self.history_tab = QWidget()
        layout = QHBoxLayout(self.history_tab)

        viewed_layout = QVBoxLayout()
        viewed_layout.addWidget(QLabel("최근 본 위스키"))
        self.viewed_list_widget = QListWidget()
        viewed_layout.addWidget(self.viewed_list_widget)
        layout.addLayout(viewed_layout)

        collection_layout = QVBoxLayout()
        collection_layout.addWidget(QLabel("내 컬렉션"))
        self.collection_list_widget = QListWidget()
        collection_layout.addWidget(self.collection_list_widget)
        layout.addLayout(collection_layout)

        self.tab_widget.addTab(self.history_tab, "활동 기록")

    def init_recommend_tab(self):
        """추천 탭 UI 생성"""
        self.recommend_tab = QWidget()
        layout = QVBoxLayout(self.recommend_tab)

        button_layout = QHBoxLayout()
        self.get_pref_recs_button = QPushButton("내 취향 기반 추천 받기")
        self.get_pref_recs_button.clicked.connect(self.on_get_pref_recs_clicked)
        self.get_similar_recs_button = QPushButton("현재 선택한 위스키와 유사한 것 추천 받기")
        self.get_similar_recs_button.clicked.connect(self.on_get_similar_recs_clicked)
        self.get_similar_recs_button.setEnabled(False)
        button_layout.addWidget(self.get_pref_recs_button)
        button_layout.addWidget(self.get_similar_recs_button)
        layout.addLayout(button_layout)

        layout.addWidget(QLabel("추천 결과:"))
        self.recommendation_list_widget = QListWidget()
        self.recommendation_list_widget.itemClicked.connect(self.on_recommendation_item_clicked)
        layout.addWidget(self.recommendation_list_widget)

        self.tab_widget.addTab(self.recommend_tab, "위스키 추천")

    def init_review_tab(self):
        """리뷰 탭 UI 생성"""
        self.review_tab = QWidget()
        layout = QVBoxLayout(self.review_tab)
        layout.addWidget(QLabel("리뷰 (현재 선택된 위스키)"))

        self.review_list_widget = QListWidget()
        layout.addWidget(self.review_list_widget)

        layout.addWidget(QLabel("새 리뷰 작성:"))
        new_review_layout = QHBoxLayout()
        self.new_review_rating_spinbox = QSpinBox()
        self.new_review_rating_spinbox.setRange(1, 5)
        self.new_review_rating_spinbox.setValue(3)
        self.new_review_text_input = QLineEdit()
        self.new_review_text_input.setPlaceholderText("리뷰 내용을 입력하세요...")
        self.add_review_button = QPushButton("리뷰 등록")
        self.add_review_button.clicked.connect(self.on_add_review_clicked)

        new_review_layout.addWidget(QLabel("평점:"))
        new_review_layout.addWidget(self.new_review_rating_spinbox)
        new_review_layout.addWidget(self.new_review_text_input)
        new_review_layout.addWidget(self.add_review_button)
        layout.addLayout(new_review_layout)

        self.review_tab.setEnabled(False)
        self.tab_widget.addTab(self.review_tab, "리뷰")

    def load_initial_data(self):
        """애플리케이션 시작 시 또는 사용자 설정 후 초기 데이터를 로드하고 UI에 표시합니다."""
        print("UI: Loading initial data...")
        user = self.system_reference.get_current_user()
        if not user:
             QMessageBox.critical(self, "치명적 오류", "사용자 정보를 로드할 수 없습니다. 프로그램을 종료합니다.")
             self.close()
             return

        self.update_whiskey_list()
        preference = user.get_preference()
        self.display_user_preferences(preference)
        self.update_history_display()

    def update_whiskey_list(self):
        """현재 검색어와 정렬 기준에 맞춰 위스키 목록을 업데이트합니다."""
        search_term = self.search_input.text()
        sort_option = self.sort_combo.currentText()

        sort_key_map = {
            '이름 (오름차순)': ('name', False), '이름 (내림차순)': ('name', True),
            '가격 (낮은순)': ('price', False), '가격 (높은순)': ('price', True),
            '도수 (낮은순)': ('alcohol_percentage', False), '도수 (높은순)': ('alcohol_percentage', True),
        }
        sort_by, reverse_sort = sort_key_map.get(sort_option, ('name', False))

        print(f"UI: Updating whiskey list. Search='{search_term}', Sort='{sort_by}', Reverse={reverse_sort}")
        try:
            search_results_objects = self.system_reference.whiskey_catalog.search_whiskeys(search_term)
            sorted_list_objects = self.system_reference.whiskey_catalog.sort_whiskeys(search_results_objects, sort_by, reverse_sort)
            whiskey_list_for_display = [w.get_basic_info() for w in sorted_list_objects]

            # 현재 선택된 아이템 저장 (업데이트 후 복원 시도용)
            current_selection_id = self.current_selected_whiskey_id

            self.whiskey_list_widget.clear()
            item_to_reselect = None
            if not whiskey_list_for_display:
                self.whiskey_list_widget.addItem("결과 없음")
            else:
                for whiskey_info in whiskey_list_for_display:
                    display_text = f"{whiskey_info['name']} ({whiskey_info.get('type', 'N/A')})"
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, whiskey_info['id'])
                    self.whiskey_list_widget.addItem(item)
                    if whiskey_info['id'] == current_selection_id:
                        item_to_reselect = item # 업데이트 후 다시 선택할 아이템 저장

            # 이전 선택 항목이 새 목록에도 있으면 다시 선택
            if item_to_reselect:
                # itemSelectionChanged 시그널을 잠시 막고 선택 설정 후 다시 풀기 (선택 이벤트 재호출 방지)
                self.whiskey_list_widget.blockSignals(True)
                self.whiskey_list_widget.setCurrentItem(item_to_reselect)
                self.whiskey_list_widget.blockSignals(False)
            elif current_selection_id:
                 # 이전에 선택된 것이 있었는데 새 목록에 없다면 상세 정보 초기화
                 self.display_whiskey_details(None)


        except Exception as e:
            print(f"Error updating whiskey list: {e}")
            QMessageBox.critical(self, "오류", f"위스키 목록을 불러오는 중 오류 발생:\n{e}")

    def display_whiskey_details(self, whiskey_id: Optional[str]):
        """선택된 위스키 ID에 대한 상세 정보를 오른쪽 탭에 표시합니다."""
        self.current_selected_whiskey_id = whiskey_id
        is_valid_whiskey = bool(whiskey_id)
        self.get_similar_recs_button.setEnabled(is_valid_whiskey)
        self.add_collection_button.setEnabled(is_valid_whiskey)
        self.review_tab.setEnabled(is_valid_whiskey)

        if not whiskey_id:
            self.detail_name_label.setText("N/A")
            self.detail_origin_label.setText("N/A")
            self.detail_type_label.setText("N/A")
            self.detail_price_label.setText("N/A")
            self.detail_abv_label.setText("N/A")
            self.detail_age_label.setText("N/A")
            self.detail_taste_label.setText("N/A")
            self.review_list_widget.clear()
            return

        print(f"UI: Displaying details for whiskey ID: {whiskey_id}")
        try:
            details = self.system_reference.get_whiskey_details_for_display(whiskey_id)
            if details:
                self.detail_name_label.setText(details.get('name', 'N/A'))
                self.detail_origin_label.setText(details.get('origin', 'N/A'))
                self.detail_type_label.setText(details.get('type', 'N/A'))
                price = details.get('price')
                self.detail_price_label.setText(f"${price:.2f}" if price is not None else "N/A")
                abv = details.get('alcohol_percentage')
                self.detail_abv_label.setText(f"{abv}%" if abv is not None else "N/A")
                age = details.get('age_years')
                self.detail_age_label.setText(f"{age}년" if age is not None else "N/A")
                taste = details.get('taste_profile', 'N/A')
                self.detail_taste_label.setText(str(taste))
                self.update_review_display(whiskey_id)

                user = self.system_reference.get_current_user()
                if user and user.get_history() and user.get_history().is_in_collection(whiskey_id):
                     self.add_collection_button.setText("내 컬렉션에서 제거")
                else:
                     self.add_collection_button.setText("내 컬렉션에 추가")
            else:
                QMessageBox.warning(self, "정보 없음", f"위스키 ID '{whiskey_id}'에 대한 정보를 찾을 수 없습니다.")
                self.current_selected_whiskey_id = None
                self.display_whiskey_details(None)
        except Exception as e:
             print(f"Error displaying whiskey details: {e}")
             QMessageBox.critical(self, "오류", f"위스키 상세 정보를 불러오는 중 오류 발생:\n{e}")

    def display_user_preferences(self, preference: Optional['User_Preference']):
        """사용자 선호도 객체의 데이터를 UI 위젯에 표시합니다."""
        if preference:
            # 값 변경 시그널 잠시 비활성화 (값을 설정하는 동안 슬롯 호출 방지)
            sliders = [self.pref_sweet_slider, self.pref_smoky_slider, self.pref_fruity_slider, self.pref_spicy_slider]
            inputs = [self.pref_price_min_input, self.pref_price_max_input]
            for w in sliders + inputs: w.blockSignals(True)

            print("UI: Displaying user preferences.")
            self.pref_sweet_slider.setValue(preference.sweetness_preference)
            self.pref_smoky_slider.setValue(preference.smoky_preference)
            self.pref_fruity_slider.setValue(preference.fruity_preference)
            self.pref_spicy_slider.setValue(preference.spicy_preference)
            self.pref_value_labels["단맛"].setText(str(preference.sweetness_preference))
            self.pref_value_labels["스모키"].setText(str(preference.smoky_preference))
            self.pref_value_labels["과일향"].setText(str(preference.fruity_preference))
            self.pref_value_labels["스파이시"].setText(str(preference.spicy_preference))

            min_p, max_p = preference.get_price_range()
            self.pref_price_min_input.setText(str(min_p) if min_p is not None else "")
            self.pref_price_max_input.setText(str(max_p) if max_p is not None else "")

            # 시그널 다시 활성화
            for w in sliders + inputs: w.blockSignals(False)
        else:
            print("UI: No preference data to display.")


    def update_history_display(self):
        """사용자의 활동 기록(최근 본, 컬렉션)을 UI에 업데이트합니다."""
        user = self.system_reference.get_current_user()
        history = user.get_history() if user else None

        self.viewed_list_widget.clear()
        self.collection_list_widget.clear()

        if history:
            print("UI: Updating history display.")
            recently_viewed = history.get_recently_viewed(20)
            for whiskey_id, timestamp in recently_viewed:
                 whiskey = self.system_reference.whiskey_catalog.get_whiskey_details(whiskey_id)
                 name = whiskey.name if whiskey else f"ID: {whiskey_id}"
                 time_str = timestamp.strftime("%Y-%m-%d %H:%M")
                 item = QListWidgetItem(f"{name} ({time_str})")
                 item.setData(Qt.UserRole, whiskey_id)
                 self.viewed_list_widget.addItem(item)

            collection_ids = history.get_collection()
            for whiskey_id in collection_ids:
                 whiskey = self.system_reference.whiskey_catalog.get_whiskey_details(whiskey_id)
                 name = whiskey.name if whiskey else f"ID: {whiskey_id}"
                 item = QListWidgetItem(name)
                 item.setData(Qt.UserRole, whiskey_id)
                 self.collection_list_widget.addItem(item)
        else:
             print("UI: No history data to display.")

    def update_review_display(self, whiskey_id: str):
        """특정 위스키에 대한 리뷰 목록을 업데이트합니다."""
        self.review_list_widget.clear()
        print(f"UI: Updating reviews for whiskey ID: {whiskey_id}")
        try:
            reviews = self.system_reference.get_reviews_for_whiskey(whiskey_id)
            if not reviews:
                self.review_list_widget.addItem("이 위스키에 대한 리뷰가 아직 없습니다.")
            else:
                # 최신 리뷰가 위로 오도록 정렬 (선택 사항)
                reviews.sort(key=lambda r: r.review_date, reverse=True)
                for review in reviews:
                    details = review.get_review_details()
                    rating = details.get('rating', '?')
                    text = details.get('review_text', '(내용 없음)')
                    date = details.get('review_date', '')[:10]
                    user_id = details.get('user_id', 'Unknown')
                    display_text = f"평점: {rating}/5 | 작성자: {user_id} ({date})\n{text}"
                    item = QListWidgetItem(display_text)
                    # 리뷰 텍스트가 길 경우 전체 표시 대신 툴팁 사용 고려
                    # item.setToolTip(display_text)
                    self.review_list_widget.addItem(item)
        except Exception as e:
             print(f"Error updating review display: {e}")
             QMessageBox.critical(self, "오류", f"리뷰를 불러오는 중 오류 발생:\n{e}")

    def prompt_for_user_setup(self) -> bool:
        """사용자 정보가 없을 때, 사용자 ID와 이름을 입력받는 다이얼로그를 띄웁니다."""
        user_id, ok1 = QInputDialog.getText(self, '초기 사용자 설정', '사용자 ID를 입력하세요:')
        if ok1 and user_id.strip():
            user_name, ok2 = QInputDialog.getText(self, '초기 사용자 설정', '사용자 이름을 입력하세요:')
            if ok2 and user_name.strip():
                user_info = {'user_id': user_id.strip(), 'user_name': user_name.strip()}
                print(f"UI: Attempting to register new user: {user_info}")
                success = self.system_reference.register_new_user(user_info)
                if success:
                    QMessageBox.information(self, "설정 완료", f"사용자 '{user_name}'({user_id}) 설정이 완료되었습니다.")
                    return True
                else:
                    QMessageBox.critical(self, "등록 실패", "사용자 등록에 실패했습니다.")
                    return False
            else:
                 QMessageBox.warning(self, "입력 필요", "사용자 이름이 필요합니다.")
                 return False
        else:
             QMessageBox.warning(self, "입력 필요", "사용자 ID가 필요합니다.")
             return False

    # --- PyQt5 슬롯 메서드들 ---
    @pyqtSlot()
    def on_search_changed(self):
        # 검색어가 변경될 때마다 목록 업데이트 (짧은 시간 내 연속 변경 시 부하 고려 -> QTimer 사용한 디바운싱(Debouncing) 적용 가능)
        self.update_whiskey_list()

    @pyqtSlot()
    def on_sort_changed(self):
        self.update_whiskey_list()

    @pyqtSlot()
    def on_whiskey_selected(self):
        selected_items = self.whiskey_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            whiskey_id = selected_item.data(Qt.UserRole)
            self.display_whiskey_details(whiskey_id if whiskey_id else None)
        else:
            # 목록에서 선택이 해제된 경우 (예: 빈 곳 클릭)
            self.display_whiskey_details(None)

    # *** "전체 목록 보기" 버튼 슬롯 추가됨 ***
    @pyqtSlot()
    def on_show_all_clicked(self):
        """'전체 목록' 버튼 클릭 시 호출됩니다."""
        print("UI: 'Show All' button clicked.")
        # 검색창 내용 지우기 (textChanged 시그널이 발생하여 on_search_changed 호출 기대)
        self.search_input.clear()
        # 만약 clear()가 textChanged를 발생시키지 않으면 아래 주석 해제
        # self.update_whiskey_list()

    @pyqtSlot()
    def on_save_prefs_clicked(self):
        user = self.system_reference.get_current_user()
        preference = user.get_preference() if user else None
        if not preference:
             QMessageBox.warning(self, "오류", "사용자 선호도 정보를 찾을 수 없습니다.")
             return
        print("UI: Saving preferences...")
        try:
            # UI 위젯에서 값 읽기 (기존과 동일)
            sweet = self.pref_sweet_slider.value()
            smoky = self.pref_smoky_slider.value()
            fruity = self.pref_fruity_slider.value()
            spicy = self.pref_spicy_slider.value()
            min_p_str = self.pref_price_min_input.text()
            max_p_str = self.pref_price_max_input.text()
            min_p = int(min_p_str) if min_p_str else None
            max_p = int(max_p_str) if max_p_str else None

            # User_Preference 업데이트 (기존과 동일)
            preference.update_preference('sweetness', sweet)
            preference.update_preference('smoky', smoky)
            preference.update_preference('fruity', fruity)
            preference.update_preference('spicy', spicy)
            preference.update_price_range(min_p, max_p)

            QMessageBox.information(self, "저장 완료", "선호도가 저장되었습니다.")
            self.display_user_preferences(preference) # 업데이트 확인
        except ValueError:
             QMessageBox.warning(self, "입력 오류", "가격은 숫자만 입력 가능합니다.")
        except Exception as e:
             print(f"Error saving preferences: {e}")
             QMessageBox.critical(self, "오류", f"선호도 저장 중 오류 발생:\n{e}")

    @pyqtSlot()
    def on_add_to_collection_clicked(self):
        if not self.current_selected_whiskey_id:
            QMessageBox.warning(self, "선택 필요", "먼저 위스키를 선택해주세요.")
            return
        user = self.system_reference.get_current_user()
        history = user.get_history() if user else None
        if not history:
            QMessageBox.warning(self, "오류", "사용자 활동 기록 정보를 찾을 수 없습니다.")
            return
        whiskey_id = self.current_selected_whiskey_id
        print(f"UI: Toggling collection status for {whiskey_id}")
        try:
            whiskey_name = self.detail_name_label.text()
            if history.is_in_collection(whiskey_id):
                history.remove_from_collection(whiskey_id)
                self.add_collection_button.setText("내 컬렉션에 추가")
                QMessageBox.information(self, "컬렉션", f"'{whiskey_name}'을(를) 컬렉션에서 제거했습니다.")
            else:
                history.add_to_collection(whiskey_id)
                self.add_collection_button.setText("내 컬렉션에서 제거")
                QMessageBox.information(self, "컬렉션", f"'{whiskey_name}'을(를) 컬렉션에 추가했습니다.")
            self.update_history_display()
        except Exception as e:
            print(f"Error updating collection: {e}")
            QMessageBox.critical(self, "오류", f"컬렉션 업데이트 중 오류 발생:\n{e}")

    @pyqtSlot()
    def on_get_pref_recs_clicked(self):
        print("UI: Requesting preference-based recommendations...")
        self.recommendation_list_widget.clear()
        self.recommendation_list_widget.addItem("추천 목록을 불러오는 중...")
        QApplication.processEvents()
        try:
            recommendations = self.system_reference.get_recommendations(count=10, method_type='preference')
            self.recommendation_list_widget.clear()
            if not recommendations:
                self.recommendation_list_widget.addItem("추천할 위스키를 찾지 못했습니다.")
            else:
                for rec_info in recommendations:
                    display_text = f"{rec_info['name']} ({rec_info.get('type', 'N/A')})"
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, rec_info['id'])
                    self.recommendation_list_widget.addItem(item)
        except Exception as e:
            print(f"Error getting preference recommendations: {e}")
            self.recommendation_list_widget.clear()
            self.recommendation_list_widget.addItem("추천을 가져오는 중 오류 발생.")
            QMessageBox.critical(self, "오류", f"취향 기반 추천 중 오류 발생:\n{e}")

    @pyqtSlot()
    def on_get_similar_recs_clicked(self):
        if not self.current_selected_whiskey_id:
            QMessageBox.warning(self, "선택 필요", "유사한 위스키를 찾으려면 먼저 기준 위스키를 선택해주세요.")
            return
        base_whiskey_id = self.current_selected_whiskey_id
        base_whiskey_name = self.detail_name_label.text()
        print(f"UI: Requesting recommendations similar to {base_whiskey_name} ({base_whiskey_id})...")
        self.recommendation_list_widget.clear()
        self.recommendation_list_widget.addItem(f"'{base_whiskey_name}'와(과) 유사한 위스키 검색 중...")
        QApplication.processEvents()
        try:
            # System.get_recommendations 에 기준 ID 전달 필요 (수정됨)
            recommendations = self.system_reference.get_recommendations(count=10, method_type='similar', base_whiskey_id=base_whiskey_id)

            self.recommendation_list_widget.clear()
            if not recommendations:
                self.recommendation_list_widget.addItem(f"'{base_whiskey_name}'와(과) 유사한 위스키를 찾지 못했습니다.")
            else:
                self.recommendation_list_widget.addItem(f"--- '{base_whiskey_name}'와(과) 유사한 위스키 ---")
                for rec_info in recommendations:
                    if rec_info['id'] == base_whiskey_id: continue # 자기 자신 제외
                    display_text = f"{rec_info['name']} ({rec_info.get('type', 'N/A')})"
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, rec_info['id'])
                    self.recommendation_list_widget.addItem(item)
        except Exception as e:
            print(f"Error getting similar recommendations: {e}")
            self.recommendation_list_widget.clear()
            self.recommendation_list_widget.addItem("유사 추천을 가져오는 중 오류 발생.")
            QMessageBox.critical(self, "오류", f"유사 위스키 추천 중 오류 발생:\n{e}")

    @pyqtSlot(QListWidgetItem)
    def on_recommendation_item_clicked(self, item: QListWidgetItem):
        whiskey_id = item.data(Qt.UserRole)
        if whiskey_id:
             print(f"UI: Recommendation item clicked, moving to whiskey ID: {whiskey_id}")
             found = False
             for i in range(self.whiskey_list_widget.count()):
                  list_item = self.whiskey_list_widget.item(i)
                  if list_item.data(Qt.UserRole) == whiskey_id:
                       self.whiskey_list_widget.setCurrentItem(list_item)
                       # setCurrentItem이 itemSelectionChanged 시그널을 발생시키므로,
                       # display_whiskey_details는 on_whiskey_selected 슬롯에서 처리됨
                       self.tab_widget.setCurrentWidget(self.details_tab) # 상세 탭으로 이동
                       found = True
                       break
             if not found:
                  # 추천 목록에는 있지만 현재 필터링된 메인 목록에는 없을 수 있음
                  QMessageBox.information(self, "정보", "해당 위스키는 현재 목록 필터에 맞지 않아 직접 이동할 수 없습니다. 상세 정보만 표시합니다.")
                  # 상세 정보만 표시
                  self.display_whiskey_details(whiskey_id)
                  self.tab_widget.setCurrentWidget(self.details_tab)


    @pyqtSlot()
    def on_add_review_clicked(self):
        if not self.current_selected_whiskey_id:
            QMessageBox.warning(self, "선택 필요", "리뷰를 작성할 위스키를 먼저 선택해주세요.")
            return
        whiskey_id = self.current_selected_whiskey_id
        rating = self.new_review_rating_spinbox.value()
        text = self.new_review_text_input.text().strip()

        print(f"UI: Adding review for {whiskey_id}. Rating={rating}, Text='{text}'")
        try:
            new_review = self.system_reference.create_and_add_review(whiskey_id, rating, text)
            if new_review:
                 QMessageBox.information(self, "리뷰 등록", "리뷰가 성공적으로 등록되었습니다.")
                 self.new_review_rating_spinbox.setValue(3)
                 self.new_review_text_input.clear()
                 self.update_review_display(whiskey_id)
            else:
                 QMessageBox.warning(self, "등록 실패", "리뷰를 등록하지 못했습니다. 시스템 로그를 확인하세요.")
        except Exception as e:
             print(f"Error adding review: {e}")
             QMessageBox.critical(self, "오류", f"리뷰 등록 중 오류 발생:\n{e}")

    def closeEvent(self, event):
        """메인 윈도우가 닫힐 때 호출됩니다."""
        reply = QMessageBox.question(self, '종료 확인',
                                     "애플리케이션을 종료하시겠습니까?\n(변경사항이 저장됩니다)",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("UI: Closing application. Requesting state save...")
            try:
                self.system_reference.save_system_state()
            except Exception as e:
                print(f"Error during save on exit: {e}")
                QMessageBox.warning(self, "저장 오류", f"종료 중 상태 저장 실패:\n{e}")
            event.accept()
        else:
            event.ignore()