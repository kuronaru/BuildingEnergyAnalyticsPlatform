from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from static.connector import Ui_connector
from ui.ui_bms import Ui_main


class UIConnector(QWidget, Ui_connector):
    def __init__(self):
        super().__init__()

        # 调用生成的 UI 类的 setupUi 方法
        self.setupUi(self)

        # 添加自定义功能
        self.Start_button.clicked.connect(self.on_start)

    @staticmethod
    def on_start():
        bms_main = QtWidgets.QWidget()  # 创建一个主窗口
        ui = Ui_main()  # 创建 UI 实例
        ui.setupUi(bms_main)  # 将 UI 设置到主窗口上
        bms_main.show()  # 显示主窗口