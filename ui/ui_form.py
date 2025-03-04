import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

from server_status import SUCCESS
from static.Form import Ui_Form


class UIForm(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        # 调用生成的 UI 类的 setupUi 方法
        self.setupUi(self)

        # 添加自定义功能
        self.load_user_info_to_table()
        self.load_bms_info_to_table()
        self.pushButton_6.clicked.connect(self.reload_register_interface)

    @staticmethod
    def reload_register_interface():
        """重新加载注册界面"""
        from ui.ui_login import LoginApp
        ui_login = LoginApp()  # 直接创建 LoginApp 实例
        ui_login.setWindowModality(QtCore.Qt.ApplicationModal)  # 设置为模态窗口
        ui_login.show()  # 显示登录界面

    def show_page_1(self):
        """切换到第一个页面"""
        self.stackedWidget.setCurrentIndex(0)  # 显示第一个页面

    def show_page_2(self):
        """切换到第二个页面"""
        self.stackedWidget.setCurrentIndex(1)

    def show_page_3(self):
        """切换到第二个页面"""
        self.stackedWidget.setCurrentIndex(2)

    def show_page_4(self):
        """切换到第二个页面"""
        self.stackedWidget.setCurrentIndex(3)

    def show_page_5(self):
        """切换到第二个页面"""
        self.stackedWidget.setCurrentIndex(4)

    def load_bms_info_to_table(self):
        bms_info = self.get_bms_info()  # 获取 BMS 信息

        if bms_info:
            # 获取字典的键作为列头
            headers = list(bms_info.keys())

            # 设置表格的列数
            self.tableWidget_2.setColumnCount(len(headers))
            self.tableWidget_2.setHorizontalHeaderLabels(headers)  # 设置列头

            # 设置表格的行数
            self.tableWidget_2.setRowCount(1)  # 只需要一行

            # 填充数据到表格中
            for col_index, key in enumerate(headers):
                self.tableWidget_2.setItem(0, col_index, QtWidgets.QTableWidgetItem(str(bms_info[key])))

                # 调整列宽以适应内容
            self.tableWidget_2.resizeColumnsToContents()

            # 获取 tableWidget_2 的总宽度
            table_width = 559

            # 计算每列的宽度
            column_width = table_width // len(headers)  # 根据列数均匀分配宽度

            # 设置每列的宽度
            for col in range(self.tableWidget_2.columnCount()):
                self.tableWidget_2.setColumnWidth(col, column_width)

        else:
            print("No BMS data available.")

    def load_user_info_to_table(self):
        user_info = self.get_user_info()  # 获取 BMS 信息
        print(user_info)

    @staticmethod
    def get_bms_info():
        url = 'http://127.0.0.1:5000/homepage/get_bms_info'  # 替换为实际的接口 URL
        headers = {'Content-Type': 'application/json'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:  # 检查是否成功获取响应
            result = response.json()  # 解析 JSON 响应

            if result['status'] == SUCCESS:

                return result['data']  # 返回获取到的数据

            else:
                print("Failed to retrieve BMS data.")
                return None
        else:
            print("Error:", response.status_code)  # 如果请求失败，打印错误信息
            return None

    @staticmethod
    def get_user_info():
        url = 'http://127.0.0.1:5000/homepage/get_user_info'  # 替换为实际的接口 URL
        headers = {'Content-Type': 'application/json'}

        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 400:  # 检查是否成功获取响应
            result = response.json()  # 解析 JSON 响应

            if result['status'] == SUCCESS:
                print(result['data'])
                return result['data']  # 返回获取到的数据

            else:
                print("Failed to retrieve user data.")
                return None
        else:
            print("Error:", response.status_code)  # 如果请求失败，打印错误信息
            return None
