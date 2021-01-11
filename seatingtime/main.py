import time
import json
from datetime import datetime

from arduinoAccessor import ArduinoAccessor
from ambientAccessor import AmbientAccessor
from seatingDetector import SeatingDetector

json_open = open("settings.json", "r")
settings = json.load(json_open)

PORT = settings["port"]
RATE = settings["rate"]
WRITE_KEY = settings["writekey"]
CHANNEL_ID = settings["channelid"]

TIME_TO_STAND = 1   # minute

ard = ArduinoAccessor(PORT, RATE)
amb = AmbientAccessor(WRITE_KEY, CHANNEL_ID)

detector = SeatingDetector(20)

print("10秒後に離席時の距離を設定します。センサをセットして離れてください。")
time.sleep(10)
print("設定中")
absentDist = ard.getData()
ard.closePort()
detector.setDefault(absentDist)
print("離席時距離: " + str(absentDist) + "cm")
print("開始します...")

isSitting = False
start = time.time()

try:
    while True:
        data = ard.getData(1)
        while data["d2"] == "48":
            data = ard.getData(1)
        print(data)

        checkresult = detector.checkMin(data)
        if checkresult != None:
            print("Sending: " + str(checkresult))
            amb.send(checkresult)
            if checkresult["d1"] == 1:
                if not isSitting:
                    start = time.time()
                isSitting = True
            elif checkresult["d1"] == 0:
                isSitting = False
        
        if isSitting:
            elapsedTime = time.time() - start
            elapsedTimeStr = print(datetime.fromtimestamp(elapsedTime).strftime("%M:%S"))
            if elapsedTime >= TIME_TO_STAND * 60:
                ard.sendData("2")
            else:
                ard.sendData("1")
        else:
            ard.sendData("0")
        # ard.ser.flush()
        # ard.resetBuffer()
        time.sleep(5)

except KeyboardInterrupt:
    # ctrl-C をキャッチ
    ard.closePort()
    print("Interrupted! 終了します.")
    exit()