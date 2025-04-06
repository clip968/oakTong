# main.py
import sys
import os

# PyQt5 관련 모듈 import
from PyQt5.QtWidgets import QApplication, QMessageBox # QMessageBox 추가

# 우리가 만든 주요 클래스들 import
from system import System
# ui.py에서 MainWindow 클래스를 import 하도록 변경
from ui import MainWindow

def main():
    """애플리케이션 메인 실행 함수"""
    print("Application starting...")

    # PyQt5 애플리케이션 인스턴스 생성
    app = QApplication(sys.argv)
    print("QApplication instance created.")

    # 백엔드 시스템 객체 생성
    system = System()
    print("System instance created.")

    # 시스템 초기화 결과 확인
    initialization_successful = system.initialize()
    print(f"System initialization attempt finished. User loaded: {initialization_successful}")

    # MainWindow 인스턴스 생성
    # MainWindow 생성 시 내부에서 System 참조를 받으므로, System 초기화 이후에 생성
    main_window = MainWindow(system_reference=system)
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

    # 종료 전 상태 저장은 MainWindow의 closeEvent에서 처리

    sys.exit(exit_code)


if __name__ == '__main__':
    main()