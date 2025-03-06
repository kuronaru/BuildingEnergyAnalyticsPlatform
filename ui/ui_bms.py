import requests
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QTreeWidgetItem, QCheckBox, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, QMenu, \
    QTreeWidget, QLabel, QVBoxLayout, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QMessageBox, QHBoxLayout
from PyQt5.uic.properties import QtWidgets, QtCore

from static import BMS
from static.BMS import Ui_BMS
from ui.ui_connector import UIBMSDialog


class UIBms(QWidget, Ui_BMS):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def start_connector(self):
        self.UIBMSDialog = UIBMSDialog(self)
        self.UIBMSDialog.exec_()

    def renew(self):
        device_ip=load_setting("ip")
        self.deviceTree.headerItem().setText(0, "Local IP Address:"+device_ip)
        self.Port_label.setText(load_setting("id"))

    def on_item_double_clicked(self,event):
        content=self.Port_label.text()
        if content == "Double-click to open UIConnector":
            self.start_connector()
        elif content == load_setting("id"):
            device_id=load_setting("id")
            try:
                        # 向后端发送连接请求
                        response = requests.get('http://127.0.0.1:5000/bms/device_objects',
                                                json={'device_id': device_id})
                        result = response.json()

                        for obj in result['objects']:
                            instance = obj.get('object_instance', None)
                            obj_type = obj.get('object_type', None)
                            self.objectList.addItem(f"{obj_type}: {instance}")
                            self.objectList.itemDoubleClicked.connect(self.on_content_double_clicked)

            except requests.ConnectionError:
                QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

        else:
            return  # elif ":" in text:  #     obj_type, instance = text.split(":", 1)  #     if obj_type == "analogInput" and instance == "0":  #         print(1)  #     elif obj_type == "analogOutput" and instance == "1":  #         print(2)

    def on_content_double_clicked(self,item):
        item_text = item.text()
        device_id = load_setting("id")
        if ":" in item_text:
            obj_type, instance = item_text.split(":", 1)  # 拆分文本，只拆分第一个冒号



        # 进行其他操作
        if item_text.endswith("0"):
            try:
                        # 向后端发送连接请求
                        response = requests.post('http://127.0.0.1:5000/bms/get_object_data',
                                                json={'device_id': device_id, 'object_type': obj_type,'object_instance':instance})
                        result = response.json()
                        time=result['time']
                        self.add_data_to_table(device_id,obj_type,instance,time)



            except requests.ConnectionError:
                QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

    def add_data_to_table(self,device_id,obj_type,instance,time):
        # 添加一行数据到表格
        row_position = self.instanceTable.rowCount()  # 获取当前行数
        self.instanceTable.insertRow(row_position)  # 插入新的一行
        items = [[f'{device_id}',f'{obj_type}: {instance}',f'{time}']]
        for i in range(len(items)):
            item = items[i]

            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.instanceTable.setItem(row_position, j+1, item)
        self.setup_checkbox(self.instanceTable, row_position, 0)
        self.instanceTable.resizeColumnsToContents()

    def setup_checkbox(self, table_widget, row1, column):
        widget = QWidget()  # 方法内的局部变量，每次调用都是新的副本，所以才能单独让每个tablewidget的勾选框独立连接信号
        widget.checkbox = QCheckBox()  # 将checkbox放在widget中
        playout = QHBoxLayout(widget)
        playout.addWidget(widget.checkbox)  # 为小部件添加checkbox属性
        widget.setLayout(playout)  # 在QWidget放置布局
        table_widget.setCellWidget(row1, column, widget)
        # widget.checkbox.stateChanged.connect(lambda state, row=row1: self.on_checkbox_state_changed(state, row))

    # def on_checkbox_state_changed(self, state, row):
    #     # 根据复选框状态来显示图像
    #     if state:
    #         self.display_graph()
    #     else:
    #         # 复选框取消勾选时，清除图像
    #         self.clear_image()
    #
    # def display_graph(self):
    #
    #     scene = QGraphicsScene(self.graphicsView)
    #     scene.setSceneRect(0, 0, 200, 200)
    #     self.draw_axes(scene)
    #     # 示例数据点
    #     data_points = [(0, 200), (200, 0)]
    #
    #     # 创建折线
    #     previous_point = None
    #     for point in data_points:
    #         x = point[0] * 1  # 放大以便显示
    #         y = point[1] * 1  # 放大以便显示
    #         if previous_point:
    #             line = QGraphicsLineItem(previous_point[0], previous_point[1], x, y)  # 绘制折线
    #             line.setPen(QPen(QColor(255, 0, 255), 2))  # 设置线的颜色和宽度
    #             scene.addItem(line)  # 添加线到场景中
    #         previous_point = (x, y)
    #
    #     self.graphicsView.setScene(scene)  # 将场景设置给graphicsView
    #
    # def draw_axes(self, scene):
    #     # X 轴
    #     x_axis = QGraphicsLineItem(0, 200, 200, 200)  # 从 (0, 0) 到 (200, 0)
    #     x_axis.setPen(QPen(QColor(0, 0, 0), 2))  # 设置坐标轴的颜色和宽度
    #     scene.addItem(x_axis)  # 将 X 轴添加到场景中
    #
    #     # Y 轴
    #     y_axis = QGraphicsLineItem(0, 0, 0, 200)  # 从 (0, 0) 到 (0, 200)
    #     y_axis.setPen(QPen(QColor(0, 0, 0), 2))  # 设置坐标轴的颜色和宽度
    #     scene.addItem(y_axis)  # 将 Y 轴添加到场景中
    #
    #     # 添加 X 轴和 Y 轴的标签
    #     x_label = QGraphicsTextItem("X")
    #     x_label.setPos(205, 190)  # 设置 X 标签的位置
    #     scene.addItem(x_label)
    #
    #     y_label = QGraphicsTextItem("Y")
    #     y_label.setPos(-10, -10)  # 设置 Y 标签的位置
    #     scene.addItem(y_label)
    #
    #     # 添加坐标轴的刻度（可以根据需要调整间隔）
    #     self.add_axis_ticks(scene, x_axis, "x")
    #     self.add_axis_ticks(scene, y_axis, "y")
    #
    # @staticmethod
    # def add_axis_ticks(scene, axis, axis_type):
    #     # 假设我们以 20 为步长绘制刻度
    #     tick = None
    #     for i in range(0, 201, 20):  # 绘制刻度
    #         if axis_type == "x":
    #             tick = QGraphicsLineItem(i, 200, i, 195)  # 绘制 X 轴刻度
    #         elif axis_type == "y":
    #             tick = QGraphicsLineItem(0, i, 5, i)  # 绘制 Y 轴刻度
    #
    #         tick.setPen(QPen(QColor(0, 0, 0), 1))  # 设置刻度的颜色和宽度
    #         scene.addItem(tick)
    #
    #     # 为每个刻度添加标签（数字）
    #     for i in range(0, 201, 20):
    #         if axis_type == "x":
    #             label = QGraphicsTextItem(str(i))
    #             label.setPos(i - 5, 205)  # 设置标签位置
    #             scene.addItem(label)
    #         elif axis_type == "y":
    #             label = QGraphicsTextItem(str(i))
    #             label.setPos(5, 200 - i - 5)  # 反转Y轴
    #             scene.addItem(label)
    #
    # def clear_image(self):
    #     # 清除当前图像
    #     self.graphicsView.setScene(None)
    #

@staticmethod
def load_setting(key):
    """
    通用的读取 QSettings 设置的函数，确保返回字符串
    :param key: 配置的键名，例如 'port', 'ip', 'device_id'
    :param default_value: 如果配置不存在时返回的默认值
    :return: 配置值，类型为字符串
    """
    settings = QSettings("MyCompany", "BMSApp")
    value = settings.value(key, "1111")  # 读取配置，如果没有则返回默认值
    return str(value)  # 确保返回的是字符串




