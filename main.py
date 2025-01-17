import sys
from PyQt5.QtWidgets import QApplication
from threading import Thread
from applications import create_app, db
from ui.main_window import MainWindow


def start_flask():
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start PyQt application
    qt_app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(qt_app.exec_())
