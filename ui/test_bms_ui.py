import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

from applications.database.db_bms_manager import BMSDataManager
from server_status import SUCCESS

settings = QSettings("MyCompany", "BMSApp")


class BMSIntegrationApp(QtWidgets.QWidget):
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

        # 设备IP 输入框
        self.ip_label = QLabel('BMS Device IP:')
        self.ip_label.setFont(QFont("Arial", 10))
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Enter BMS Device IP (e.g., 192.168.0.1)")
        self.ip_input.setText("1.1.1.115")
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)

        # 端口 输入框
        self.port_label = QLabel('BMS Local Port:')
        self.port_label.setFont(QFont("Arial", 10))
        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Enter BMS Local Port (e.g., 47808)")
        self.port_input.setText("47809")
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        # 设备端口 输入框
        self.device_port_label = QLabel('Device Port:')
        self.device_port_label.setFont(QFont("Arial", 10))
        self.device_port_input = QLineEdit()
        self.device_port_input.setPlaceholderText("Enter Device Port (e.g., 59194)")
        self.device_port_input.setText("56530")
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
        self.read_button.clicked.connect(self.save_setting)
        self.read_button.clicked.connect(self.goto_bms_main)
        button_layout.addWidget(self.read_button)

        # 清除数据按钮
        self.clear_data_button = QPushButton('Clear Data')
        self.clear_data_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.clear_data_button.clicked.connect(self.handle_clear_data)
        button_layout.addWidget(self.clear_data_button)

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


    def save_setting(self):
        port = self.port_input.text().strip()
        settings.setValue("port", port)  # 存入 QSettings
        ip = self.ip_input.text().strip()
        settings.setValue("ip", ip)  # 存入 QSettings
        device_id = 'RoomSimulator'
        settings.setValue("device_id", device_id)
        settings.sync()


    def goto_bms_main(self):
        try:
            from ui.ui_bms import Ui_main  # 这里重新导入

            self.bms_main = QtWidgets.QWidget()  # 使用 QMainWindow，而不是 QWidget
            self.ui = Ui_main()
            self.ui.setupUi(self.bms_main)
            self.bms_main.show()

        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to import UI: {e}")

        except AttributeError as e:
            QMessageBox.critical(self, "Error", f"UI setup error: {e}")


    def handle_connect(self):
        """ 处理连接操作 """
        device_ip = self.ip_input.text().strip()
        local_port = self.port_input.text().strip()

        if not device_ip or not local_port:
            QMessageBox.warning(self, 'Input Error', 'Please provide both IP and Port.')
            return

        try:
            # 向后端发送连接请求
            response_local_ip = requests.get('http://127.0.0.1:5000/bms/get_local_ip').json()
            local_ip = response_local_ip['local_ip']
            response = requests.post(
                'http://127.0.0.1:5000/bms/connect_bms',
                json={'local_ip': local_ip, 'local_port': local_port}
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
        device_ip = self.ip_input.text().strip()
        local_port = self.port_input.text().strip()

        if not device_ip or not local_port:
            QMessageBox.warning(self, 'Input Error', 'Please provide both IP and Port.')
            return

        try:
            # 向后端发送断开请求
            response = requests.post(
                'http://127.0.0.1:5000/bms/disconnect_bms',
                json={'ip': device_ip, 'port': local_port}
            )
            result = response.json()

            if result['status'] == SUCCESS:
                QMessageBox.information(self, 'Success', result['message'])
            else:
                QMessageBox.warning(self, 'Error', result['message'])
        except requests.ConnectionError:
            QMessageBox.critical(self, 'Error', 'Unable to connect to the server')


    def handle_clear_data(self):
        """Handle logic for clearing data."""
        try:
            # Call the backend logic to clear data
            response = requests.post(
                'http://127.0.0.1:5000/bms/clear_data',
                json={'clear_all': True, 'value': 5, 'unit': 'minutes'})  # Example: Clears old data for last 10 minutes
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Data cleared successfully!")
            else:
                QMessageBox.warning(self, "Failure", "Failed to clear data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


    def handle_read_data(self):
        """ 处理读取数据操作 """
        device_ip = self.ip_input.text().strip()
        local_port = self.port_input.text().strip()
        device_id = 'RoomSimulator'
        device_port = self.device_port_input.text().strip()
        object_instance = self.object_instance_input.text().strip()

        if not device_ip or not local_port:
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
                    'device_ip': device_ip,
                    'device_id': device_id,
                    'local_port': local_port,
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


