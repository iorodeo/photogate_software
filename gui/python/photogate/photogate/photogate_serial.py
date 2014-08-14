from __future__ import print_function
import serial
import platform
import time
import json

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

# -----------------------------------------------------------------------------
if __name__ == '__main__': 

    port = '/dev/ttyACM0'
    dev = PhotogateDevice(port)

    while True:
        dataDict = dev.getData()
        print(dataDict)

