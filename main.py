import sys
import asyncio
from threading import Thread
from PyQt5.QtWidgets import QApplication


from applications import create_app
#from ui.mainwindow import Ui_Form
#from ui.connector import Ui_connector

from ui.ui_login import LoginApp

from ui.test_bms_ui import BMSIntegrationApp
from ui.ui_main import Ui_MainWindow


def start_flask():
    app = create_app()
    app.run(use_reloader=False)


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start PyQt application
    from PyQt5 import QtCore, QtWidgets

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    qt_app = QApplication(sys.argv)
    # main_window = LoginApp()
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    """
    main_window = QtWidgets.QWidget()
    ui = Ui_Form()  # 创建 UI 实例
    ui.setupUi(main_window)  # 将 UI 设置到主窗口上
    """
    # connector.show()
    # ui = Ui_Form()  # 创建 UI 实例
    # ui.setupUi(main_window)  # 将 UI 设置到主窗口上


    bms_window = BMSIntegrationApp()
    bms_window.show()
    sys.exit(qt_app.exec_())
