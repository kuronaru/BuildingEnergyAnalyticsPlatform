import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World App")

        # Set up UI components
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # QLabel for displaying messages
        self.label = QtWidgets.QLabel("Click the button to fetch a message")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # QPushButton for triggering requests
        self.pushButton = QtWidgets.QPushButton("Fetch Message")
        self.layout.addWidget(self.pushButton)

        self.pushButton.clicked.connect(self.fetch_message)
        # 导入使用PyQt Designer设计UI时生成的.ui文件
        # uic.loadUi('ui/ui_main_window.ui', self)  # Load UI file
        # self.init_ui()

    # def init_ui(self):
    #     self.pushButton.clicked.connect(self.fetch_message)

    def fetch_message(self):
        try:
            response = requests.get('http://127.0.0.1:5000/api/hello')
            if response.status_code == 200:
                self.label.setText(response.json().get('message', 'No message'))
            else:
                self.label.setText('Error: Unable to fetch message')
        except Exception as e:
            self.label.setText(f'Error: {str(e)}')
