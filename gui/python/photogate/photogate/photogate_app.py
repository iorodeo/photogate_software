from __future__ import print_function
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from photogate_ui import Ui_PhotogateMainWindow


class PhotogateMainWindow(QtGui.QMainWindow, Ui_PhotogateMainWindow):

    def __init__(self,parent=None):
        super(PhotogateMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectWidgets()
        self.initialize()

    def connectWidgets(self):
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.resetPushButton.clicked.connect(self.resetClicked_Callback)
        self.actionSaveMat.triggered.connect(self.saveMat_Callback)
        self.actionSaveTxt.triggered.connect(self.saveTxt_Callback)

    def main(self):
        self.show()
        self.raise_()

    def initialize(self):
        self.dev = None

    def connectPressed_Callback(self):
        print('connect pressed')

    def connectClicked_Callback(self):
        print('connect clicked')

    def resetClicked_Callback(self):
        print('reset clicked')

    def saveMat_Callback(self):
        print('save mat')

    def saveTxt_Callback(self):
        print('save txt')
      
def runPhotogateApp():
    app = QtGui.QApplication(sys.argv)
    mainWindow = PhotogateMainWindow()
    mainWindow.main()
    app.exec_()


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    runPhotogateApp()


