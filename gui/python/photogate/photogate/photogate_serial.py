from __future__ import print_function
import serial
import platform
import time
import json


class PhotogateDev(serial.Serial):

    BAUDRATE = 115200
    RESET_TIMEOUT = 2.0

    def __init__(self, port='/dev/ttyACM0', timeout=1.0):
        super(PhotogateDev,self).__init__(port,self.BAUDRATE,timeout=timeout)
        time.sleep(self.RESET_TIMEOUT)
        self.reset()
        self.flushInput()
        self.flushOutput()

    def reset(self):
        self.write('r')

    def getData(self):
        self.write('j')
        jsonStr = self.readline()
        jsonStr = jsonStr.strip()
        dataDict = json.loads(jsonStr)
        return dataDict

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    port = '/dev/ttyACM0'
    dev = PhotogateDev(port)

    while True:
        dataDict = dev.getData()
        print(dataDict)
        #time.sleep(0.05)
