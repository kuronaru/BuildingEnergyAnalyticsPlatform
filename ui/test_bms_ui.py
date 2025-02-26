from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests
from server_status import SUCCESS


class BMSIntegrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('BMS Server Integration')
        self.resize(400, 250)

        # 主布局
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 标题
        self.title = QLabel("BMS Server Integration")
        self.title.setFont(QFont("Arial", 14, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # IP 输入框
        self.ip_label = QLabel('BMS Server IP:')
        self.ip_label.setFont(QFont("Arial", 10))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter BMS Server IP (e.g., 192.168.0.1)")
        self.ip_input.setText("1.1.1.115")
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)

        # 端口 输入框
        self.port_label = QLabel('BMS Server Port:')
        self.port_label.setFont(QFont("Arial", 10))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter BMS Server Port (e.g., 47808)")
        self.port_input.setText("47809")
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        # 设备端口 输入框
        self.device_port_label = QLabel('Device Port:')
        self.device_port_label.setFont(QFont("Arial", 10))
        self.device_port_input = QLineEdit()
        self.device_port_input.setPlaceholderText("Enter Device Port (e.g., 59194)")
        self.device_port_input.setText("59194")
        layout.addWidget(self.device_port_label)
        layout.addWidget(self.device_port_input)

        # 实例号 输入框
        self.object_instance_label = QLabel('Object Instance:')
        self.object_instance_label.setFont(QFont("Arial", 10))
        self.object_instance_input = QLineEdit()
        self.object_instance_input.setPlaceholderText("Enter Object Instance (e.g., 0)")
        self.object_instance_input.setText("0")
        layout.addWidget(self.object_instance_label)
        layout.addWidget(self.object_instance_input)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 连接按钮
        self.connect_button = QPushButton('Connect')
        self.connect_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.connect_button.clicked.connect(self.handle_connect)
        button_layout.addWidget(self.connect_button)

        # 断开按钮
        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.disconnect_button.clicked.connect(self.handle_disconnect)
        button_layout.addWidget(self.disconnect_button)

        # 读取数据按钮
        self.read_button = QPushButton('Read Data')
        self.read_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.read_button.clicked.connect(self.handle_read_data)
        button_layout.addWidget(self.read_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

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
            QPushButton:disabled {
                background-color: #999;
                color: #ccc;
            }
        """)

    def handle_connect(self):
        """ 处理连接操作 """
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()

        if not ip or not port:
            QMessageBox.warning(self, 'Input Error', 'Please provide both IP and Port.')
            return

        try:
            # 向后端发送连接请求
            response = requests.post(
                'http://127.0.0.1:5000/bms/connect_bms',
                json={'ip': ip, 'port': port}
            )
            result = response.json()

            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

    def handle_disconnect(self):
        """ 处理断开操作 """
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()

        if not ip or not port:
            QMessageBox.warning(self, 'Input Error', 'Please provide both IP and Port.')
            return

        try:
            # 向后端发送断开请求
            response = requests.post(
                'http://127.0.0.1:5000/bms/disconnect_bms',
                json={'ip': ip, 'port': port}
            )
            result = response.json()

            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

    def handle_read_data(self):
        """ 处理读取数据操作 """
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        device_port = self.device_port_input.text().strip()
        object_instance = self.object_instance_input.text().strip()

        if not ip or not port:
            QMessageBox.warning(self, 'Input Error', 'Please provide both IP and Port.')
            return

        db_name = "bms.db"
        save_data = True

        action = "start"

        try:
            # 向后端发送读取数据请求
            response = requests.post(
                'http://127.0.0.1:5000/bms/receive_data',
                json={
                    'action': action,
                    'save_data': save_data,
                    'db_name': db_name,
                    'ip': ip,
                    'server_port': port,
                    'device_port': device_port,
                    'object_instance': object_instance,
                    'interval': 1
                }
            )
            result = response.json()

            if result['status'] == SUCCESS:
                # 显示数据
                QMessageBox.information(self, 'BMS Data', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')
