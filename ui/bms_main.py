from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem

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
        self.treeView_2 = QtWidgets.QTreeWidget(main)
        self.treeView_2.setObjectName("treeView_2")
        self.verticalLayout.addWidget(self.treeView_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.Objects = QtWidgets.QLabel(main)
        self.Objects.setObjectName("Objects")
        self.verticalLayout.addWidget(self.Objects)

        # 使用 QTreeWidget 替代 QTreeView
        self.treeView = QtWidgets.QTreeWidget(main)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout.addLayout(self.verticalLayout)

        """""
        self.init_device_data()
        
        """

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Subscriptions = QtWidgets.QLabel(main)
        self.Subscriptions.setObjectName("Subscriptions")
        self.verticalLayout_2.addWidget(self.Subscriptions)
        self.tableWidget = QtWidgets.QTableWidget(main)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
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

    def init_device_data(self):
        self.treeView_2.clear()
        # 使用 QTreeWidget 进行设备和对象的初始化
        device = QTreeWidgetItem(self.treeView, ["RoomController.Simulator"])

        # 添加与该设备相关的对象
        QTreeWidgetItem(device, ["Temperature.Indoor"])
        QTreeWidgetItem(device, ["Temperature.Water"])
        QTreeWidgetItem(device, ["Temperature.Outdoor"])
        QTreeWidgetItem(device, ["SetPoint.Value"])
        QTreeWidgetItem(device, ["State.Heater"])
        QTreeWidgetItem(device, ["State.Chiller"])

