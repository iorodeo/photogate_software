from __future__ import print_function
import os
import sys
import serial.tools.list_ports
from PyQt4 import QtCore
from PyQt4 import QtGui
from photogate_ui import Ui_PhotogateMainWindow
from photogate_serial import PhotogateDevice
from photogate_serial import getListOfPorts
import dependency_hack
try:
    import scipy.io
    HAVE_SCIPY_IO = True
except ImportError:
    HAVE_SCIPY_IO = False


class PhotogateMainWindow(QtGui.QMainWindow, Ui_PhotogateMainWindow):

    PORT_MONITOR_TIMER_DT = 1000
    DATA_ACQUISITION_TIMER_DT = 10
    NOT_AVAILABLE_STR = ''
    FILE_TYPE_TO_FILTER = {
            '.txt' : "Text (*.txt);;All files (*.*)",
            '.mat' : "Mat (*.mat);;All files (*.*)",
            '.csv' : "CSV (*.csv);;All files (*.*)",
            }

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
        self.actionSaveCsv.triggered.connect(self.saveCsv_Callback)

    def main(self):
        self.show()
        self.raise_()

    def initialize(self):
        self.dev = None
        self.lastDataDict = None
        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.lastSaveDir = self.userHome

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
        self.dataAcquisitionTimer.setSingleShot(True); # Serial communications sets the pacing
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
                self.setStatusbarMessage(dataDict)
                if self.lastDataDict is not None:
                    if self.lastDataDict['running']:
                        self.setDataText(dataDict)
                else:
                    self.setDataText(dataDict)
                self.lastDataDict = dataDict
                self.updateSaveWidgetEnabled()
        self.dataAcquisitionTimer.start()

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

    def fileSaveDialog(self,fileExt):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        if os.path.isdir(self.lastSaveDir):
            saveDir = self.lastSaveDir
        else:
            saveDir = self.userHome
        fileNameFullPath = dialog.getSaveFileName(
                   None,
                   'Select {0} file'.format(fileExt),
                   saveDir,
                   self.FILE_TYPE_TO_FILTER[fileExt],
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        fileNameFullPath = str(fileNameFullPath)
        if fileNameFullPath:
            # Extract last save path and check for file extension 
            filePath, fileName = os.path.split(fileNameFullPath)
            self.lastSaveDir = filePath
            fileName = autoAddFileExtension(fileName,fileExt)
            fileNameFullPath = os.path.join(filePath,fileName)
        return fileNameFullPath

    def saveMat_Callback(self):
        if not HAVE_SCIPY_IO:
            return
        fileExt = '.mat'
        dataDict = self.lastDataDict
        fileNameFullPath = self.fileSaveDialog(fileExt)
        if fileNameFullPath:
            matDict = self.getMatDict(dataDict)
            scipy.io.savemat(fileNameFullPath,matDict)

    def getMatDict(self,dataDict):
        matDict = {}
        for i, photogateDict in enumerate(dataDict['photogates']):
            if photogateDict['isConnected']:
                entryTime, exitTime, timeInGate = getPhotogateTimes(photogateDict)
                matDict['photogate{0}'.format(i)] = {
                        'entryTime'   : entryTime,
                        'exitTime'    : exitTime, 
                        'timeInGate'  : timeInGate, 
                        }
        if dataDict['operatingMode'] == 'TWO_PHOTOGATE':
            timeBetweenGates = getTimeBetweenGates(dataDict['photogates'])
            matDict['timeBetweenGates'] = timeBetweenGates
        return matDict

    def saveTxt_Callback(self):
        fileExt = '.txt'
        dataStr = self.getDataStr(self.lastDataDict)
        fileNameFullPath = self.fileSaveDialog(fileExt)
        if fileNameFullPath:
            with open(fileNameFullPath,'w') as f:
                f.write(dataStr)

    def saveCsv_Callback(self):
        fileExt = '.csv'
        dataDict = self.lastDataDict
        fileNameFullPath = self.fileSaveDialog(fileExt)
        if fileNameFullPath:
            csvDataStr = self.getCsvDataStr(dataDict)
            with open(fileNameFullPath,'w') as f:
                f.write(csvDataStr)

    def getCsvDataStr(self,dataDict):
        dataStrList = ['field,value']
        for i,photogateDict  in enumerate(dataDict['photogates']):
            if photogateDict['isConnected']:
                entryTime, exitTime, timeInGate = getPhotogateTimes(photogateDict)
                dataStrList.append('"photogate {0} enter",{1}'.format(i,entryTime))
                dataStrList.append('"photogate {0} exit",{1}'.format(i,exitTime))
                dataStrList.append('"photogate {0} in-gate",{1}'.format(i,timeInGate))
        if dataDict['operatingMode'] == 'TWO_PHOTOGATE':
            timeBetweenGates = getTimeBetweenGates(dataDict['photogates'])
            dataStrList.append('"between gates",{0}'.format(timeBetweenGates))
        dataStr = '\n'.join(dataStrList)
        return dataStr

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
        self.updateSaveWidgetEnabled()

    def updateSaveWidgetEnabled(self): 
        if self.lastDataDict is not None:
            if not self.lastDataDict['running'] and not self.lastDataDict['timeout']:
                if HAVE_SCIPY_IO:
                    self.actionSaveMat.setEnabled(True)
                self.actionSaveTxt.setEnabled(True)
                self.actionSaveCsv.setEnabled(True)
            else:
                self.actionSaveMat.setEnabled(False)
                self.actionSaveTxt.setEnabled(False)
                self.actionSaveCsv.setEnabled(False)
        else:
            self.actionSaveMat.setEnabled(False)
            self.actionSaveTxt.setEnabled(False)
            self.actionSaveCsv.setEnabled(False)

    def populatePortComboBox(self):
        currPort = str(self.portComboBox.currentText())
        self.portComboBox.clear()
        portNameList = getListOfPorts()
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

    def getDataStr(self,dataDict):
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
                timeBetween = getTimeBetweenGates(dataDict['photogates'])
                timeBetweenStr = '{0:1.5f}'.format(timeBetween)
            timeBetweenStr = 'between-gates: {0}'.format(timeBetweenStr)
            dataStrList.append(timeBetweenStr)

        dataStr = '\n'.join(dataStrList)
        return dataStr

    def setDataText(self,dataDict):
        dataStr = self.getDataStr(dataDict)
        self.dataText.clear()
        self.dataText.setPlainText(dataStr)

    def getPhotogateDataStr(self,photogateDict, indent=2):
        indentStr = ' '*indent
        dataStrList = []
        entryTime, exitTime, timeInGate = getPhotogateTimes(photogateDict)

        # Add entry time
        if photogateDict['hasEntryTime']:
            entryTimeStr = '{0:1.5f}'.format(entryTime)
        else:
            entryTimeStr =  self.NOT_AVAILABLE_STR
        entryTimeStr = '{0}enter:   {1}'.format(indentStr, entryTimeStr)
        dataStrList.append(entryTimeStr)

        # Add exit time
        if photogateDict['hasExitTime']:
            exitTimeStr ='{0:1.5f}'.format(exitTime) 
        else:
            exitTimeStr = self.NOT_AVAILABLE_STR
        exitTimeStr = '{0}exit:    {1}'.format(indentStr, exitTimeStr)
        dataStrList.append(exitTimeStr)

        # Add time in-gate
        if photogateDict['isDone']:
            timeInGateStr = '{0:1.5f}'.format(timeInGate)
        else:
            timeInGateStr = self.NOT_AVAILABLE_STR
        timeInGateStr = '{0}in-gate: {1}'.format(indentStr, timeInGateStr)
        dataStrList.append(timeInGateStr)

        dataStr = '\n'.join(dataStrList)
        return dataStr


# Utility functions
# -----------------------------------------------------------------------------

def getPhotogateTimes(photogateDict):
    entryTime = uSecToSec(float(photogateDict['entryTime']))
    exitTime = uSecToSec(float(photogateDict['exitTime']))
    timeInGate = exitTime - entryTime
    return entryTime, exitTime, timeInGate

def getTimeBetweenGates(photogateList): 
    entryTime0 = uSecToSec(float(photogateList[0]['entryTime'])) 
    entryTime1 = uSecToSec(float(photogateList[1]['entryTime'])) 
    timeBetween = entryTime1 - entryTime0
    return timeBetween

def autoAddFileExtension(fileName,autoExt): 
    fileNameBase, fileNameExt = os.path.splitext(fileName)
    if not fileNameExt:
        # Only add extension if there isn't one already
        fileName = '{0}{1}'.format(fileNameBase,autoExt)
    return fileName

def uSecToSec(value):
    return (1.0e-6)*value
    
def runPhotogateApp():
    app = QtGui.QApplication(sys.argv)
    mainWindow = PhotogateMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    runPhotogateApp()


