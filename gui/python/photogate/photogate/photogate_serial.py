from __future__ import print_function
import serial
import time
import json
import platform
import itertools


class PhotogateDevice(serial.Serial):

    BAUDRATE = 115200
    RESET_TIMEOUT = 2.5

    def __init__(self, port='/dev/ttyACM0', timeout=1.0):
        super(PhotogateDevice,self).__init__(port,self.BAUDRATE,timeout=timeout)
        time.sleep(self.RESET_TIMEOUT)
        if platform.system() == 'Linux':
            self.posixHack()
        self.flushInput()
        self.flushOutput()
        self.clearInWaiting()
        self.reset()

    def clearInWaiting(self):
        while self.inWaiting()>0:
            self.read()

    def reset(self):
        self.write('r')

    def getData(self):
        self.write('j')
        jsonStr = self.readline()
        jsonStr = jsonStr.strip()
        try:
            dataDict = json.loads(jsonStr)
        except ValueError:
            dataDict = {}
        return dataDict

    def posixHack(self):
        # Toggle baudrate ... fixes issue which seem to effect pyserial 2.7 and
        # Arduino Uno's on Linux.. Basically When device is unplugged and re-connected 
        # communications using pyserial don't seem to work properly. Toggling the 
        # baudrate seems to fix this. Note, I'm not really sure why this works. 
        self.baudrate = 9600
        self.baudrate = self.BAUDRATE


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

    if 1:
        port = '/dev/ttyACM0'
        dev = PhotogateDevice(port)

        while True:
            dataDict = dev.getData()
            print(dataDict)

    if 0:
        portList = getListOfPorts()
        print(portList)

