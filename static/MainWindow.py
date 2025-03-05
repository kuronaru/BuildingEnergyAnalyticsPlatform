# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1279, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Singapore))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.login = QtWidgets.QWidget()
        self.login.setObjectName("login")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.login)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(560, 350, 541, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout.setContentsMargins(0, -1, 0, -1)
        self.formLayout.setObjectName("formLayout")
        self.usernameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.usernameLineEdit)
        self.passwordLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.loginButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setMinimumSize(QtCore.QSize(120, 0))
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout.addWidget(self.loginButton, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.stackedWidget.addWidget(self.login)
        self.main = QtWidgets.QWidget()
        self.main.setObjectName("main")
        self.layoutWidget = QtWidgets.QWidget(self.main)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1281, 721))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.menu = QtWidgets.QListWidget(self.layoutWidget)
        self.menu.setEnabled(True)
        self.menu.setMinimumSize(QtCore.QSize(0, 0))
        self.menu.setAutoFillBackground(False)
        self.menu.setIconSize(QtCore.QSize(35, 35))
        self.menu.setResizeMode(QtWidgets.QListView.Fixed)
        self.menu.setGridSize(QtCore.QSize(0, 60))
        self.menu.setBatchSize(100)
        self.menu.setObjectName("menu")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        item.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/home_regular.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/home_solid.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/home_regular.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item.setIcon(icon)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.menu.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/server_regular.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/server_solid.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/server_regular.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item.setIcon(icon1)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.menu.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/dashboard_regular.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icon/dashboard_solid.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icon/dashboard_regular.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item.setIcon(icon2)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.menu.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/log_regular.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/icon/log_solid.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/icon/log_regular.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item.setIcon(icon3)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.menu.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/user_regular.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/icon/user_solid.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/icon/user_regular.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item.setIcon(icon4)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.menu.addItem(item)
        self.horizontalLayout_1.addWidget(self.menu)
        self.pages = QtWidgets.QStackedWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages.sizePolicy().hasHeightForWidth())
        self.pages.setSizePolicy(sizePolicy)
        self.pages.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Singapore))
        self.pages.setObjectName("pages")
        self.homePage = QtWidgets.QWidget()
        self.homePage.setEnabled(True)
        self.homePage.setObjectName("homePage")
        self.pages.addWidget(self.homePage)
        self.bmsPage = QtWidgets.QWidget()
        self.bmsPage.setObjectName("bmsPage")
        self.pages.addWidget(self.bmsPage)
        self.dashboardPage = QtWidgets.QWidget()
        self.dashboardPage.setObjectName("dashboardPage")
        self.pages.addWidget(self.dashboardPage)
        self.logPage = QtWidgets.QWidget()
        self.logPage.setObjectName("logPage")
        self.pages.addWidget(self.logPage)
        self.userPage = QtWidgets.QWidget()
        self.userPage.setObjectName("userPage")
        self.pages.addWidget(self.userPage)
        self.horizontalLayout_1.addWidget(self.pages)
        self.horizontalLayout_1.setStretch(0, 2)
        self.horizontalLayout_1.setStretch(1, 9)
        self.stackedWidget.addWidget(self.main)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.menu.setCurrentRow(-1)
        self.pages.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Building Energy Analytics Platform"))
        self.usernameLabel.setText(_translate("MainWindow", "Username:"))
        self.passwordLabel.setText(_translate("MainWindow", "Password:"))
        self.loginButton.setText(_translate("MainWindow", "Login"))
        self.menu.setSortingEnabled(False)
        __sortingEnabled = self.menu.isSortingEnabled()
        self.menu.setSortingEnabled(False)
        item = self.menu.item(0)
        item.setText(_translate("MainWindow", "Home"))
        item = self.menu.item(1)
        item.setText(_translate("MainWindow", "BMS"))
        item = self.menu.item(2)
        item.setText(_translate("MainWindow", "Dashboard"))
        item = self.menu.item(3)
        item.setText(_translate("MainWindow", "Log"))
        item = self.menu.item(4)
        item.setText(_translate("MainWindow", "Admin"))
        self.menu.setSortingEnabled(__sortingEnabled)
import icon_rc
