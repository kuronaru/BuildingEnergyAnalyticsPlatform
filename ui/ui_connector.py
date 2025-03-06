from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QDialog

from static.BMSDialog import Ui_BMSDialog




class UIBMSDialog(QDialog, Ui_BMSDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # 将父窗口传递给 QDialog
        self.setupUi(self)
        self.remoteIPLineEdit.setText("192.168.1.19")
        self.remotePortLineEdit.setText("63322")
        # 在 UIConnector 中使用父窗口
        self.buttonBox.accepted.connect(self.closeconnector)

    def closeconnector(self):
        """ 关闭 UIConnector 并调用父窗口的 renew 方法 """
        ip = self.remoteIPLineEdit.text()  # 获取 QLineEdit 中的文本
        port=self.remotePortLineEdit.text()
        id=61512
        settings = QSettings("MyCompany", "BMSApp")  # 设置组织名称和应用名称
        settings.setValue("ip", ip)  # 保存数据到 QSettings
        settings.setValue("port", port)
        settings.setValue("id", id)

        self.close()  # 关闭 UIConnector 窗口

        parent = self.parentWidget()
        parent.renew()  # 调用父窗口的 renew 方法


