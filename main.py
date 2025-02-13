import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication
from applications import create_app
from ui.bms_integration import BMSIntegrationApp
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
    # main_window = LoginApp()
    main_window = BMSIntegrationApp()
    main_window.show()
    sys.exit(qt_app.exec_())
