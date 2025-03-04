import requests
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QTreeWidgetItem, QCheckBox, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, QMenu
from PyQt5.QtWidgets import QWidget, QMessageBox, QHBoxLayout

from static.bms_main import Ui_main


class UIBms(QWidget, Ui_main):
    def __init__(self):
        super().__init__()

        # 调用生成的 UI 类的 setupUi 方法
        self.setupUi(self)

        # 添加自定义功能

    def on_item_double_clicked(self, item):
        device_id = self.load_setting('device_id', '1')
        ip = self.load_setting('ip', '127.0.0.1')
        port = self.load_setting('port', '5000')
        text = item.text(0)
        result = None
        obj_type = None
        instance = None
        if text == ip:
            if self.treeView.isColumnHidden(0):
                try:
                    # 向后端发送连接请求
                    response = requests.get('http://127.0.0.1:5000/bms/device_objects', json={'device_id': device_id})
                    result = response.json()

                except requests.ConnectionError:
                    QMessageBox.critical(self, 'Error', 'Unable to connect to the server')

                # 遍历 objects 列表
                for obj in result['objects']:
                    instance = obj.get('object_instance', None)
                    obj_type = obj.get('object_type', None)

                self.treeView.setColumnHidden(0, False)
                root_item = QTreeWidgetItem(self.treeView, [str(device_id)])
                self.treeView.addTopLevelItem(QTreeWidgetItem(root_item, [str(obj_type) + ':' + str(instance)]))

            else:
                return  # elif ":" in text:  #     obj_type, instance = text.split(":", 1)  #     if obj_type == "analogInput" and instance == "0":  #         print(1)  #     elif obj_type == "analogOutput" and instance == "1":  #         print(2)

    def on_tree_item_right_click(self, position):
        item = self.treeView.itemAt(position)
        if item is not None:
            menu = QMenu()
            subscribe_action = menu.addAction("Subscribe")
            action = menu.exec_(self.treeView.viewport().mapToGlobal(position))

            if action == subscribe_action:
                object_name = item.text()  # Assume the object name is the item's text.
                self.subscribe_to_object(object_name)

    def setup_checkbox(self, table_widget, row1, column):
        widget = QWidget()  # 方法内的局部变量，每次调用都是新的副本，所以才能单独让每个tablewidget的勾选框独立连接信号
        widget.checkbox = QCheckBox()  # 将checkbox放在widget中
        playout = QHBoxLayout(widget)
        playout.addWidget(widget.checkbox)  # 为小部件添加checkbox属性
        widget.setLayout(playout)  # 在QWidget放置布局

        table_widget.setCellWidget(row1, column, widget)
        widget.checkbox.stateChanged.connect(lambda state, row=row1: self.on_checkbox_state_changed(state, row))

    def on_checkbox_state_changed(self, state, row):
        # 根据复选框状态来显示图像
        if state:
            self.display_graph()
        else:
            # 复选框取消勾选时，清除图像
            self.clear_image()

    def display_graph(self):

        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 200, 200)
        self.draw_axes(scene)
        # 示例数据点
        data_points = [(0, 200), (200, 0)]

        # 创建折线
        previous_point = None
        for point in data_points:
            x = point[0] * 1  # 放大以便显示
            y = point[1] * 1  # 放大以便显示
            if previous_point:
                line = QGraphicsLineItem(previous_point[0], previous_point[1], x, y)  # 绘制折线
                line.setPen(QPen(QColor(255, 0, 255), 2))  # 设置线的颜色和宽度
                scene.addItem(line)  # 添加线到场景中
            previous_point = (x, y)

        self.graphicsView.setScene(scene)  # 将场景设置给graphicsView

    def draw_axes(self, scene):
        # X 轴
        x_axis = QGraphicsLineItem(0, 200, 200, 200)  # 从 (0, 0) 到 (200, 0)
        x_axis.setPen(QPen(QColor(0, 0, 0), 2))  # 设置坐标轴的颜色和宽度
        scene.addItem(x_axis)  # 将 X 轴添加到场景中

        # Y 轴
        y_axis = QGraphicsLineItem(0, 0, 0, 200)  # 从 (0, 0) 到 (0, 200)
        y_axis.setPen(QPen(QColor(0, 0, 0), 2))  # 设置坐标轴的颜色和宽度
        scene.addItem(y_axis)  # 将 Y 轴添加到场景中

        # 添加 X 轴和 Y 轴的标签
        x_label = QGraphicsTextItem("X")
        x_label.setPos(205, 190)  # 设置 X 标签的位置
        scene.addItem(x_label)

        y_label = QGraphicsTextItem("Y")
        y_label.setPos(-10, -10)  # 设置 Y 标签的位置
        scene.addItem(y_label)

        # 添加坐标轴的刻度（可以根据需要调整间隔）
        self.add_axis_ticks(scene, x_axis, "x")
        self.add_axis_ticks(scene, y_axis, "y")

    @staticmethod
    def add_axis_ticks(scene, axis, axis_type):
        # 假设我们以 20 为步长绘制刻度
        tick = None
        for i in range(0, 201, 20):  # 绘制刻度
            if axis_type == "x":
                tick = QGraphicsLineItem(i, 200, i, 195)  # 绘制 X 轴刻度
            elif axis_type == "y":
                tick = QGraphicsLineItem(0, i, 5, i)  # 绘制 Y 轴刻度

            tick.setPen(QPen(QColor(0, 0, 0), 1))  # 设置刻度的颜色和宽度
            scene.addItem(tick)

        # 为每个刻度添加标签（数字）
        for i in range(0, 201, 20):
            if axis_type == "x":
                label = QGraphicsTextItem(str(i))
                label.setPos(i - 5, 205)  # 设置标签位置
                scene.addItem(label)
            elif axis_type == "y":
                label = QGraphicsTextItem(str(i))
                label.setPos(5, 200 - i - 5)  # 反转Y轴
                scene.addItem(label)

    def clear_image(self):
        # 清除当前图像
        self.graphicsView.setScene(None)

    @staticmethod
    def load_setting(key, default_value):
        """
        通用的读取 QSettings 设置的函数，确保返回字符串
        :param key: 配置的键名，例如 'port', 'ip', 'device_id'
        :param default_value: 如果配置不存在时返回的默认值
        :return: 配置值，类型为字符串
        """
        settings = QSettings("MyCompany", "BMSApp")
        value = settings.value(key, default_value)  # 读取配置，如果没有则返回默认值
        return str(value)  # 确保返回的是字符串
