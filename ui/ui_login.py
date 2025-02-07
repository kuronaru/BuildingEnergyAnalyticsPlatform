import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from server_status import SUCCESS


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login System')
        self.resize(300, 150)

        layout = QVBoxLayout()

        # 用户名输入
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # 密码输入
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # 向 Flask 服务发送 POST 请求
        try:
            response = requests.post(
                'http://127.0.0.1:5000/login/auth',
                json={'username': username, 'password': password}
            )
            result = response.json()
            print('response ', response.text)
            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')
