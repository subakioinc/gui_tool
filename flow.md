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
         * 
       * broadcast()
       * subscribe()
       * periodic()
       * defer()
       * stop()
       * can_send()
   * _show_console_window()
     * 
   * _show_node_window()
   * _spin_node()
   * closeEvent()


# 