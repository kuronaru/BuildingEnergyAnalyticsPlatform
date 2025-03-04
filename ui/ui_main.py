from PyQt5.QtWidgets import QMainWindow

from static.MainWindow import Ui_MainWindow
from ui.bms_main import Ui_main


class UIMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 调用生成的 UI 类的 setupUi 方法
        self.setupUi(self)

        # 设置页面
        ui_home = Ui_main()
        ui_home.setupUi(self.home)

        # 添加自定义功能
