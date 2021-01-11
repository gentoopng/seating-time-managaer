import serial
import re
from datetime import datetime

class ArduinoAccessor:
    PORT = None
    RATE = None
    isOpened = False
    ser = None

    def __init__(self, port, rate):
        self.PORT = port
        self.RATE = rate
    
    def openPort(cls):
        cls.ser = serial.Serial(cls.PORT, cls.RATE)
        """
        cls.ser = serial.Serial()
        cls.ser.port = cls.PORT
        cls.ser.baudrate = cls.RATE
        #cls.ser.setDTR(False)
        cls.ser.open()
        """
        cls.isOpened = True
        # print("opened")
    
    def closePort(cls):
        # TODO エラー処理
        if cls.ser != None:
            cls.ser.close()
            cls.isOpened = False
        else:
            print("Error: object of Serial is missing")

    def getData(cls, mode=0):
        """
            mode = 0: return integer
            mode = 1: return dict ({"created": YYYY-MM-DD hh:mm:ss, "dist": x})
        """
        # print(cls.isOpened)
        if cls.isOpened == False or cls.ser == None:
            cls.openPort()
        
        data = cls.ser.readline().decode("utf-8")
        # print(data)
        dataInt = re.sub("\\D", "", data)
        if mode == 0:
            return dataInt

        currentTime = datetime.now()
        timeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")  # YYYY-MM-DD HH:mm:ss
        dataDict = {"created": currentTime, "d2": dataInt}
        return dataDict
    
    def sendData(cls, data):
        cls.ser.write(data.encode())
    
    def resetBuffer(cls):
        cls.ser.reset_input_buffer()
    
    def setLEDMode(cls, mode):
        """
            mode 0: not sitting
            mode 1: sitting
            mode 2: sitting for a long time (eg. 1 hour)
        """
        cls.sendData(int(mode))

    
    def makeLCDContent(cls, status, seatingTime=0): # NOT IN USE
        if status:
            statusMsg = "seating"
        else:
            statusMsg = "absent"
        fitstLine = "Seem to be" + statusMsg