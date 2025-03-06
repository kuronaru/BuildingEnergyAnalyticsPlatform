import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication, QDialog

from applications import create_app
from ui.ui_main import UIMain
#from ui.ui_bms import UIBms
#from ui.ui_connector import UIBMSDialog


def start_flask():
    app = create_app()
    app.run(use_reloader=False)


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start PyQt application
    from PyQt5 import QtCore

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    qt_app = QApplication(sys.argv)

    main_window = UIMain()
    main_window.show()

    # bms_window = BMSIntegrationApp()
    # bms_window.show()
    sys.exit(qt_app.exec_())
