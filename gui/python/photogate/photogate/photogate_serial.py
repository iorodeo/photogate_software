from __future__ import print_function
import serial
import time
import json
import platform
import itertools

if platform.system() == 'Windows':
    import _winreg as winreg


class PhotogateDevice(serial.Serial):

    BAUDRATE = 115200
    RESET_TIMEOUT = 2.0

    def __init__(self, port='/dev/ttyACM0', timeout=1.0):
        super(PhotogateDevice,self).__init__(port,self.BAUDRATE,timeout=timeout)
        time.sleep(self.RESET_TIMEOUT)
        self.reset()
        self.flushInput()
        self.flushOutput()
        self.clearInWaiting()

    def reset(self):
        self.write('r')

    def clearInWaiting(self):
        while self.inWaiting()>0:
            self.read()

    def getData(self):
        self.write('j')
        jsonStr = self.readline()
        jsonStr = jsonStr.strip()
        try:
            dataDict = json.loads(jsonStr)
        except ValueError:
            dataDict = {}
        return dataDict

# Utility functions
# -----------------------------------------------------------------------------
def getListOfPorts():
    systemType = platform.system()
    portList = [name for name,dummy,dummy in serial.tools.list_ports.comports()]
    if systemType == 'Linux':
        portList = [name for name in portList if 'USB' in name or 'ACM' in name]
    elif systemType == 'Windows':
        portList = [name for name in portList if 'COM' in name]
    else:
        raise RuntimeError, '{0} not supported yet'.format(platform.system())
    return portList

# -----------------------------------------------------------------------------
if __name__ == '__main__': 

    if 0:

        port = '/dev/ttyACM0'
        dev = PhotogateDevice(port)

        while True:
            dataDict = dev.getData()
            print(dataDict)

    if 1:
        portList = getListOfPorts()
        print(portList)

