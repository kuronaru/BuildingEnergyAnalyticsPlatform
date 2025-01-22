import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication
from applications import create_app
from ui.main_window import MainWindow
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
    qt_app = QApplication(sys.argv)
    main_window = LoginApp()
    main_window.show()
    # main_window = MainWindow()
    sys.exit(qt_app.exec_())
