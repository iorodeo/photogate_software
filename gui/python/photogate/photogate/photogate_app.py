from __future__ import print_function
import sys
import serial.tools.list_ports
from PyQt4 import QtCore
from PyQt4 import QtGui
from photogate_ui import Ui_PhotogateMainWindow
from photogate_serial import PhotogateDevice


class PhotogateMainWindow(QtGui.QMainWindow, Ui_PhotogateMainWindow):

    def __init__(self,parent=None):
        super(PhotogateMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectWidgets()
        self.initialize()

    def connectWidgets(self):
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.scanPushButton.clicked.connect(self.scanClicked_Callback)
        self.resetPushButton.clicked.connect(self.resetClicked_Callback)
        self.actionSaveMat.triggered.connect(self.saveMat_Callback)
        self.actionSaveTxt.triggered.connect(self.saveTxt_Callback)

    def main(self):
        self.show()
        self.raise_()

    def initialize(self):
        self.dev = None
        self.populatePortComboBox()
        self.updateWidgetEnabled()
        self.statusbar.showMessage('Not Connected')

    def connectPressed_Callback(self):
        if self.dev is None:
            self.connectPushButton.setText('Disconnect')
            self.connectPushButton.setFlat(True)
            self.portComboBox.setEnabled(False)
            self.statusbar.showMessage('Connecting...')

    def connectClicked_Callback(self):
        if self.dev is None:
            self.connectDevice()
        else:
            self.disconnectDevice()
        self.updateWidgetEnabled()
        self.connectPushButton.setFlat(False)

    def connectDevice(self):
        port = str(self.portComboBox.currentText())
        try:
            self.dev = PhotogateDevice(port)
        except Exception, e: 
            msgTitle = 'Connection Error'
            msgText = 'unable to connect to device: {0}'.format(str(e))
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            self.connectPushButton.setText('Connect')
            self.statusbar.showMessage('Not Connected')
            self.dev = None
        if self.dev is not None:
            self.statusbar.showMessage('Connected')

    def disconnectDevice(self):
        if self.dev is not None:
            try:
                self.dev.close()
            except:
                pass
            self.dev = None
        self.connectPushButton.setText('Connect')
        self.statusbar.showMessage('Not Connected')

    def updateWidgetEnabled(self):
        print('update widget enabled')

    def populatePortComboBox(self):
        self.portComboBox.clear()
        portList = serial.tools.list_ports.comports()
        for portName, portDesc, portId in portList:
            if 'USB' in portName or 'ACM' in portName:
                self.portComboBox.addItem(portName)
        self.portComboBox.setCurrentIndex(0)

    def scanClicked_Callback(self):
        self.populatePortComboBox()

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


