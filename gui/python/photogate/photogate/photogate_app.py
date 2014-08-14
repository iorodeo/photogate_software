from __future__ import print_function
import sys
import serial.tools.list_ports
from PyQt4 import QtCore
from PyQt4 import QtGui
from photogate_ui import Ui_PhotogateMainWindow
from photogate_serial import PhotogateDevice


class PhotogateMainWindow(QtGui.QMainWindow, Ui_PhotogateMainWindow):

    PORT_MONITOR_TIMER_DT = 1000
    DATA_ACQUISITION_TIMER_DT = 50 
    NOT_AVAILABLE_STR = ''

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
        self.populatePortComboBox()
        self.updateWidgetEnabled()
        self.setupTimers()
        self.portMonitorTimer.start()
        self.statusbar.showMessage('Not Connected')

    def setupTimers(self):
        self.portMonitorTimer = QtCore.QTimer(self)
        self.portMonitorTimer.setInterval(self.PORT_MONITOR_TIMER_DT)
        self.portMonitorTimer.timeout.connect(self.portMonitorTimer_Callback)
        self.dataAcquisitionTimer = QtCore.QTimer(self)
        self.dataAcquisitionTimer.setInterval(self.DATA_ACQUISITION_TIMER_DT)
        self.dataAcquisitionTimer.timeout.connect(self.dataAcquisitionTimer_Callback)

    def portMonitorTimer_Callback(self):
        self.populatePortComboBox()

    def dataAcquisitionTimer_Callback(self):
        if self.dev is not None:
            try:
                dataDict = self.dev.getData()
            except:
                self.statusbar.showMessage('Data Acquistion Error')
                dataDict = {}
            if dataDict:
                self.setRunTime(dataDict)
                self.setMode(dataDict)
                self.setDataText(dataDict)
                self.setStatusbarMessage(dataDict)

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
        
    def resetClicked_Callback(self):
        if self.dev is not None:
            self.dev.reset()

    def saveMat_Callback(self):
        print('save mat')

    def saveTxt_Callback(self):
        print('save txt')

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
            self.portMonitorTimer.stop()
            self.dataAcquisitionTimer.start()
            self.statusbar.showMessage('Connected')

    def disconnectDevice(self):
        if self.dev is not None:
            try:
                self.dev.close()
            except:
                pass
            self.dev = None
        self.dataAcquisitionTimer.stop()
        self.portMonitorTimer.start()
        self.connectPushButton.setText('Connect')
        self.statusbar.showMessage('Not Connected')

    def updateWidgetEnabled(self):
        if self.dev is None:
            self.portComboBox.setEnabled(True)
            self.infoFrame.setEnabled(False)
            self.dataText.setEnabled(False)
            self.resetPushButton.setEnabled(False)
        else:
            self.portComboBox.setEnabled(False)
            self.infoFrame.setEnabled(True)
            self.dataText.setEnabled(True)
            self.resetPushButton.setEnabled(True)

    def populatePortComboBox(self):
        currPort = str(self.portComboBox.currentText())
        self.portComboBox.clear()
        portNameList = [name for name,dummy,dummy in serial.tools.list_ports.comports()]
        portNameList = [name for name in portNameList if 'USB' in name or 'ACM' in name]
        for portName in portNameList:
            self.portComboBox.addItem(portName)
        try:
            index = portNameList.index(currPort)
        except ValueError:
            index = 0
        self.portComboBox.setCurrentIndex(index)

    def setRunTime(self,dataDict):
        runTime = uSecToSec(float(dataDict['runTime']))
        runTimeLabelStr = 'Time: {0:2.2f}'.format(runTime)
        self.timeLabel.setText(runTimeLabelStr)

    def setMode(self,dataDict):
        modeRaw = dataDict['operatingMode']
        if modeRaw == 'TWO_PHOTOGATE':
            mode = 'Two Photogates'
        elif modeRaw == 'ONE_PHOTOGATE':
            mode = 'One Photogate'
        elif modeRaw == 'NO_PHOTOGATE':
            mode = 'No Photogates'
        else:
            mode = 'Unknown'
        modeLabelStr = 'Mode: {0}'.format(mode)
        self.modeLabel.setText(modeLabelStr)

    def setStatusbarMessage(self,dataDict):
        running = dataDict['running']
        timeout = dataDict['timeout']
        if running:
            message = 'Running'
        else:
            if timeout:
                message = 'Stopped, Timeout'
            else:
                message = 'Measurement Complete'
        self.statusbar.showMessage(message)

    def setDataText(self,dataDict):
        self.dataText.clear()
        dataStrList = []
        infoStr = 'Timing Data (units = s, resolution = 10us)'
        dataStrList.append(infoStr)
        dataStrList.append(' ')

        # Add photogate data
        for i, photogateDict in enumerate(dataDict['photogates']):
            if photogateDict['isConnected']:
                dataStrList.append('Photogate: {0}'.format(i+1))
                photogateDataStr = self.getPhotogateDataStr(photogateDict)
                dataStrList.append(photogateDataStr)
                dataStrList.append(' ')

        # Add time between gates if in two photogate mode
        if dataDict['operatingMode'] == 'TWO_PHOTOGATE':
            if dataDict['running'] or dataDict['timeout']:
                timeBetweenStr = self.NOT_AVAILABLE_STR
            else:
                entryTime0 = uSecToSec(float(dataDict['photogates'][0]['entryTime']))
                entryTime1 = uSecToSec(float(dataDict['photogates'][1]['entryTime']))
                timeBetween = entryTime1 - entryTime0
                timeBetweenStr = '{0:1.5f}'.format(timeBetween)
            timeBetweenStr = 'between-gates: {0}'.format(timeBetweenStr)
            dataStrList.append(timeBetweenStr)

        dataStr = '\n'.join(dataStrList)
        self.dataText.setPlainText(dataStr)

    def getPhotogateDataStr(self,photogateDict, indent=2):
        indentStr = ' '*indent
        dataStrList = []

        # Add entry time
        entryTime = uSecToSec(float(photogateDict['entryTime']))
        if photogateDict['hasEntryTime']:
            entryTimeStr = '{0:1.5f}'.format(entryTime)
        else:
            entryTimeStr =  self.NOT_AVAILABLE_STR
        entryTimeStr = '{0}enter:   {1}'.format(indentStr, entryTimeStr)
        dataStrList.append(entryTimeStr)

        # Add exit time
        exitTime = uSecToSec(float(photogateDict['exitTime']))
        if photogateDict['hasExitTime']:
            exitTimeStr ='{0:1.5f}'.format(exitTime) 
        else:
            exitTimeStr = self.NOT_AVAILABLE_STR
        exitTimeStr = '{0}exit:    {1}'.format(indentStr, exitTimeStr)
        dataStrList.append(exitTimeStr)

        # Add time in gate
        timeInGate = exitTime - entryTime
        if photogateDict['isDone']:
            timeInGateStr = '{0:1.5f}'.format(timeInGate)
        else:
            timeInGateStr = self.NOT_AVAILABLE_STR
        timeInGateStr = '{0}in-gate: {1}'.format(indentStr, timeInGateStr)
        dataStrList.append(timeInGateStr)

        dataStr = '\n'.join(dataStrList)
        return dataStr


      
def runPhotogateApp():
    app = QtGui.QApplication(sys.argv)
    mainWindow = PhotogateMainWindow()
    mainWindow.main()
    app.exec_()


def uSecToSec(value):
    return (1.0e-6)*value
    


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    runPhotogateApp()


