# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'photogate.ui'
#
# Created: Thu Aug 14 09:54:00 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PhotogateMainWindow(object):
    def setupUi(self, PhotogateMainWindow):
        PhotogateMainWindow.setObjectName("PhotogateMainWindow")
        PhotogateMainWindow.resize(567, 476)
        self.centralwidget = QtGui.QWidget(PhotogateMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoFrame = QtGui.QFrame(self.centralwidget)
        self.infoFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.infoFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.infoFrame.setObjectName("infoFrame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.infoFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.timeLabel = QtGui.QLabel(self.infoFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.timeLabel.setFont(font)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_2.addWidget(self.timeLabel)
        spacerItem = QtGui.QSpacerItem(340, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.modeLabel = QtGui.QLabel(self.infoFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.modeLabel.setFont(font)
        self.modeLabel.setObjectName("modeLabel")
        self.horizontalLayout_2.addWidget(self.modeLabel)
        self.verticalLayout.addWidget(self.infoFrame)
        self.dataText = QtGui.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.dataText.setFont(font)
        self.dataText.setReadOnly(True)
        self.dataText.setObjectName("dataText")
        self.verticalLayout.addWidget(self.dataText)
        self.controlsFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlsFrame.sizePolicy().hasHeightForWidth())
        self.controlsFrame.setSizePolicy(sizePolicy)
        self.controlsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.controlsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.controlsFrame.setObjectName("controlsFrame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.controlsFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.controlsFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.portComboBox = QtGui.QComboBox(self.controlsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portComboBox.sizePolicy().hasHeightForWidth())
        self.portComboBox.setSizePolicy(sizePolicy)
        self.portComboBox.setMinimumSize(QtCore.QSize(140, 0))
        self.portComboBox.setObjectName("portComboBox")
        self.horizontalLayout.addWidget(self.portComboBox)
        self.connectPushButton = QtGui.QPushButton(self.controlsFrame)
        self.connectPushButton.setObjectName("connectPushButton")
        self.horizontalLayout.addWidget(self.connectPushButton)
        spacerItem1 = QtGui.QSpacerItem(97, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.resetPushButton = QtGui.QPushButton(self.controlsFrame)
        self.resetPushButton.setObjectName("resetPushButton")
        self.horizontalLayout.addWidget(self.resetPushButton)
        self.verticalLayout.addWidget(self.controlsFrame)
        PhotogateMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PhotogateMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        PhotogateMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PhotogateMainWindow)
        self.statusbar.setObjectName("statusbar")
        PhotogateMainWindow.setStatusBar(self.statusbar)
        self.actionSaveMat = QtGui.QAction(PhotogateMainWindow)
        self.actionSaveMat.setObjectName("actionSaveMat")
        self.actionSaveTxt = QtGui.QAction(PhotogateMainWindow)
        self.actionSaveTxt.setObjectName("actionSaveTxt")
        self.menuFile.addAction(self.actionSaveMat)
        self.menuFile.addAction(self.actionSaveTxt)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PhotogateMainWindow)
        QtCore.QMetaObject.connectSlotsByName(PhotogateMainWindow)

    def retranslateUi(self, PhotogateMainWindow):
        PhotogateMainWindow.setWindowTitle(QtGui.QApplication.translate("PhotogateMainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Time: __.__ ", None, QtGui.QApplication.UnicodeUTF8))
        self.modeLabel.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Mode:              ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.connectPushButton.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.resetPushButton.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("PhotogateMainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveMat.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Save Mat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveTxt.setText(QtGui.QApplication.translate("PhotogateMainWindow", "Save Txt", None, QtGui.QApplication.UnicodeUTF8))

