import requests
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QWidget
from PyQt5.QtWidgets import QMessageBox

from server_status import SUCCESS
from static.MainWindow import Ui_MainWindow
from ui.ui_bms import UIBms
from ui.ui_form import UIForm



class UIMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置页面
        self.ui_bms = UIBms()
        # 确保 bmsPage 被正确初始化
        self.ui_bms.setupUi(self.bmsPage)
        self.ui_form = UIForm()
        self.ui_form.setupUi(self.dashboardPage)

        # 添加自定义功能
        self.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        # 向 Flask 服务发送 POST 请求
        try:
            response = requests.post(
                'http://127.0.0.1:5000/login',
                json={'username': username, 'password': password}
            )
            result = response.json()
            print('response ', result)
            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
                self.stackedWidget.setCurrentIndex(1)
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

    def handle_register(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

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
                self.handle_login()
            else:
                QMessageBox.warning(self, 'Error', result.get('message', 'Registration failed'))
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')





