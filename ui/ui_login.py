import random
import string


import requests
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5 import QtWidgets

#from ui.main_window import MainWindow
from ui.mainwindow import Ui_Form
from server_status import SUCCESS


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login System')
        self.resize(320, 200)

        layout = QVBoxLayout()
        layout.setSpacing(15)  # 设置控件间距
        # 标题
        self.title = QLabel("User Login")
        self.title.setFont(QFont("Arial", 14, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        # 用户名输入
        self.username_label = QLabel('Username:')
        self.username_label.setFont(QFont("Arial", 10))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)


        # 密码输入
        self.password_label = QLabel('Password:')
        self.password_label.setFont(QFont("Arial", 10))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        """"
        # 验证码部分
        captcha_layout = QHBoxLayout()
        self.captcha_label = QLabel()
        self.captcha_label.setFixedSize(100, 40)
        self.refresh_captcha()  # 初始化验证码
        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Enter Captcha")
        self.captcha_input.setFixedWidth(100)
        self.refresh_button = QPushButton("↻")
        self.refresh_button.setFixedSize(40, 40)
        self.refresh_button.clicked.connect(self.refresh_captcha)
        captcha_layout.addWidget(self.captcha_label)
        captcha_layout.addWidget(self.captcha_input)
        captcha_layout.addWidget(self.refresh_button)
        layout.addLayout(captcha_layout)
        """
        # 登录按钮
        self.login_button = QPushButton('Login')
        self.login_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        # 注册按钮
        self.register_button = QPushButton('Register')
        self.register_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.register_button.clicked.connect(self.handle_register)  # 注册按钮点击事件
        layout.addWidget(self.register_button)
        # 设置样式表
        self.setStyleSheet("""
                QWidget {
                    background-color: #f4f4f4;
                }
                QLabel {
                    color: #333;
                }
                QLineEdit {
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #0078D7;
                }
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
                QPushButton:pressed {
                    background-color: #004577;
                }
            """)

    def refresh_captcha(self):
       
        self.captcha_text = ''.join(random.sample(string.ascii_uppercase + string.digits, 5))
        pixmap = QPixmap(100, 40)
        pixmap.fill(QColor('white'))
        painter = QPainter(pixmap)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(QColor(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))
        painter.drawText(10, 30, self.captcha_text)
        painter.end()
        self.captcha_label.setPixmap(pixmap)






    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()


        # 向 Flask 服务发送 POST 请求
        try:
            response = requests.post(
                'http://127.0.0.1:5000/login',
                json={'username': username, 'password': password}
            )
            result = response.json()
            print('response ', response.text)
            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
                self.open_main_window()
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

    def handle_register(self):

        username = self.username_input.text()
        password = self.password_input.text()

        # 校验用户输入
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        # 向 Flask 服务发送注册请求
        try:
            response = requests.post(
                'http://127.0.0.1:5000/register',
                json={'username': username, 'password': password, 'authority': 1}  # 默认权限为 1
            )
            result = response.json()
            if response.status_code == 201 and result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result.get('message', 'Registration failed'))
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')



    def open_main_window(self):
        """ 登录成功后打开主界面，并关闭当前窗口 """
        self.main_window = QtWidgets.QWidget()  # 创建一个主窗口
        self.ui = Ui_Form()  # 创建 UI 实例
        self.ui.setupUi(self.main_window)  # 将 UI 设置到主窗口上
        self.main_window.show()  # 显示主窗口
        self.close()  # 关闭当前登录窗口




