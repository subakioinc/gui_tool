# 동작 Flow
# main.py
 * main()
   * QApplicatio() : Qt 어플리케이션 인스턴스 생성
   * 초기화
     * interface
     * dsdl 디렉토리
     * node 생성 (uavcan.make_node())
     * node 실행 (node.spin())
   * MainWindow() : MainWindow 인스턴스 생성

 * MainWindow class
   * __init__()
     * 각종 변수 초기화
       * interface
       * node 생성 및 동작 timer
       * widget 생성
         * node monitor widget
         * local node widget
         * log message widget
         * dynamic node id allocation widget
         * file server widget
       * manager
         * plotter manager
         * bus monitor manager
         * console manager
       * Menu
         * File menu
         * Tools menu
         * Panel menu
         * Help menu
       * Window layout 표시
   * _try_spawn_can_adapter_control_panel()
     * can adapter 제어판 생성
   * _make_console_context()
     * methods
       * print_yaml()
         * 수신한 UAVCAN 구조체를 출력하기 위한 함수
       * throw_if_anonymous()
         * node가 anonymous 모드로 설정된 경우 node ID를 지정해야한다.
       * request()
         * service request를 특정 node에게 전달
       * serve()
         * service server를 등록
         * callback 호출 : 특정 type의 service request를 받을때마다 
       * broadcast()
         * 1회 혹은 주기적으로 message를 broadcast
       * subscribe()
         * 특정 UAVCAN message를 수신
       * periodic()
         * 지정한 시간 주기로 지정한 callback 호출
       * defer()
         * 지정한 시간 이후에 지정한 callback을 호출
       * stop()
         * 주기적으로 보내던 broadcast들을 모두 중단
       * can_send()
         * CAN으로 전송
   * _show_console_window()
     * console 창 보여주기
   * _show_node_window()
     * node 윈도우 보여주기
   * _spin_node()
     * node 동작 실행
   * closeEvent()


# setup_window.py
 * main() -> run_setup_window() 호출
 * run_setup_window() 
   * Dialog 인스턴스 생성
   * interface 목록 업데이트 (serial 포트 업데이트)
   * OK 버튼 클릭 callback 함수


# UI layout
 * run_setup_window()
 * 각종 widget
