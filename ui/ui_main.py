from PyQt5.QtWidgets import QMainWindow

from static.MainWindow import Ui_MainWindow
from ui.ui_bms import UIBms
from ui.ui_form import UIForm


class UIMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 调用生成的 UI 类的 setupUi 方法
        self.setupUi(self)

        # 设置页面
        ui_bms = UIBms()
        ui_bms.setupUi(self.home)
        ui_form = UIForm()
        ui_form.setupUi(self.dashboard)

        # 添加自定义功能
