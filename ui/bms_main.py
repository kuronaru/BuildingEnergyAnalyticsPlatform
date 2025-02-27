from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QPixmap, QColor, QPen
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QCheckBox, QWidget, QHBoxLayout, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import QSettings
import requests
from server_status import SUCCESS
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(739, 514)
        self.gridLayout = QtWidgets.QGridLayout(main)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Devices = QtWidgets.QLabel(main)
        self.Devices.setObjectName("Devices")
        self.verticalLayout.addWidget(self.Devices)

        # 更改为 QTreeWidget
        self.tree = QTreeWidget()
        self.verticalLayout.addWidget(self.tree)
        self.tree.setHeaderLabels(['Key'])
        self.tree.setHeaderHidden(True)
        root = QTreeWidgetItem(self.tree)
        port = load_port()

        root.setText(0, 'UDP:'+str(port))  # 确保是字符串
        child1 = QTreeWidgetItem(root)
        ip=load_ip()

        child1.setText(0, ip)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.Objects = QtWidgets.QLabel(main)
        self.Objects.setObjectName("Objects")
        self.verticalLayout.addWidget(self.Objects)
        self.treeView = QtWidgets.QTreeWidget(main)
        self.verticalLayout.addWidget(self.treeView)
        self.treeView.setObjectName("treeView")
        self.treeView.setHeaderLabels(['Key'])
        self.treeView.setHeaderHidden(True)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.treeView.setColumnHidden(0,True)
        self.treeView.itemDoubleClicked.connect(self.on_item_double_clicked)



        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Subscriptions = QtWidgets.QLabel(main)
        self.Subscriptions.setObjectName("Subscriptions")
        self.verticalLayout_2.addWidget(self.Subscriptions)
        self.tableWidget = QtWidgets.QTableWidget(main)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Show","Device","ObjectID","Name","Value","Time","Status","Description"])
        self.tableWidget.resizeColumnsToContents()

        self.verticalLayout_2.addWidget(self.tableWidget)
        self.graphicsView = QtWidgets.QGraphicsView(main)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Properties = QtWidgets.QLabel(main)
        self.Properties.setObjectName("Properties")
        self.verticalLayout_4.addWidget(self.Properties)
        self.listWidget = QtWidgets.QListWidget(main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Log = QtWidgets.QLabel(main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Log.sizePolicy().hasHeightForWidth())
        self.Log.setSizePolicy(sizePolicy)
        self.Log.setObjectName("Log")
        self.verticalLayout_3.addWidget(self.Log)
        self.textBrowser = QtWidgets.QTextBrowser(main)
        self.textBrowser.setMaximumSize(QtCore.QSize(1500, 140))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Form"))
        self.Devices.setText(_translate("main", "Devices"))
        self.Objects.setText(_translate("main", "Objects"))
        self.Subscriptions.setText(_translate("main", "Subscriptions, Periodic Polling, Events/Alarms"))
        self.Properties.setText(_translate("main", "Properties"))
        self.Log.setText(_translate("main", "Log"))

    def on_item_double_clicked(self,item):
        device_id=load_device_id()
        ip=load_ip()
        text = item.text(0)
        if text == ip:
            if self.treeView.isColumnHidden(0):
                try:
                    # 向后端发送连接请求
                    response = requests.get(
                        'http://127.0.0.1:5000/bms/device_objects',
                        json={'device_id':device_id}
                    )
                    result = response.json()

                    # if result['status'] == SUCCESS:
                    #     QMessageBox.information(self, 'Success', result['message'])
                    # else:
                    #     QMessageBox.warning(self, 'Error', result['message'])
                except requests.ConnectionError:
                    QMessageBox.critical(self, 'Error', 'Unable to connect to the server')


                device_id = result['device_id']


                # 遍历 objects 列表
                for obj in result['objects']:
                    instance = obj.get('object_instance', None)
                    obj_type = obj.get('object_type', None)


                self.treeView.setColumnHidden(0,False)
                root_item = QTreeWidgetItem(self.treeView, [str(device_id)])
                self.treeView.addTopLevelItem(QTreeWidgetItem(root_item, [str(obj_type)+':'+str(instance)]))

            else:
                return
        elif ":" in text:
            obj_type, instance = text.split(":", 1)
            if obj_type == "analogInput" and instance == "0":
                print(1)
            elif obj_type == "analogOutput" and instance == "1":
                print(2)


        """""
        elif item.text(0) == 'Temperature.Indoor (AI:0)':
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.setup_checkbox(self.tableWidget, row, 0)
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("1664976"))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem("1664976"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("AI:1"))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem("Temperature Water"))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem("20"))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem("17:00:00"))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem("OK"))
        """

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
        data_points = [(0,200),(200,0)]

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

    def add_axis_ticks(self, scene, axis, axis_type):
        # 假设我们以 20 为步长绘制刻度
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


def load_port():
    """ 读取 QSettings 里的端口，确保返回字符串 """
    settings = QSettings("MyCompany", "BMSApp")
    port = settings.value("port", "12345")  # 读取端口，默认值 12345
    return str(port)  # 确保返回的是字符串

def load_ip():
    settings = QSettings("MyCompany", "BMSApp")
    ip = settings.value("ip", "1.1")  # 读取端口，默认值 12345
    return str(ip)  # 确保返回的是字符串

def load_device_id():
    settings = QSettings("MyCompany", "BMSApp")
    device_id = settings.value("device_id", "1.1")  # 读取端口，默认值 12345
    return str(device_id)  # 确保返回的是字符串







