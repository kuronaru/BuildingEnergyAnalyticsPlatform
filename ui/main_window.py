from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Menu')
        self.resize(1000, 1000)

        # 创建主窗口
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建主布局（垂直布局）
        main_layout = QVBoxLayout(self.central_widget)

        # 创建导航栏（横向布局）
        self.nav_layout = QHBoxLayout()

        # 按钮样式
        self.default_style = """
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        self.selected_style = """
            QPushButton {
                background-color: #4CAF50; /* 绿色 */
                color: white;
                border: 2px solid #388E3C;
                border-radius: 5px;
                padding: 8px;
            }
        """

        # 创建5个按钮
        self.button_names = [
            "Homepage", "Data Mgmt", "Sensor",
            "Machine Learning", "Visualization"
        ]
        self.buttons = []
        for index, name in enumerate(self.button_names):
            button = QPushButton(name)
            button.setFont(QFont("Arial", 10, QFont.Bold))
            button.setStyleSheet(self.default_style)
            button.clicked.connect(lambda _, i=index: self.switch_page(i))
            self.nav_layout.addWidget(button)
            self.buttons.append(button)

        main_layout.addLayout(self.nav_layout)  # 添加导航栏

        # 创建内容区域（QStackedWidget）
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # 添加5个页面
        self.pages = []
        for name in self.button_names:
            page = self.create_page(name)
            self.stacked_widget.addWidget(page)
            self.pages.append(page)

        # 默认选中第一个按钮
        self.switch_page(0)

    def create_page(self, title):
        """创建模块页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(f"{title} Data Display Area")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(label)
        return page

    def switch_page(self, index):
        """切换页面并更新按钮样式"""
        self.stacked_widget.setCurrentIndex(index)

        # 更新按钮颜色
        for i, button in enumerate(self.buttons):
            if i == index:
                button.setStyleSheet(self.selected_style)  # 当前选中按钮变绿
            else:
                button.setStyleSheet(self.default_style)  # 其他按钮恢复默认样式
