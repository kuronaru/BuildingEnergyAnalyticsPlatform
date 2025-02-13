import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication


from applications import create_app
from ui.mainwindow import Ui_Form
from ui.ui_login import LoginApp



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
    main_window = QtWidgets.QWidget()
    ui = Ui_Form()  # 创建 UI 实例
    ui.setupUi(main_window)  # 将 UI 设置到主窗口上
    main_window.show()
    sys.exit(qt_app.exec_())
