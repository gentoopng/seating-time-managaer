from datetime import datetime

class SeatingDetector:
    defaultDist = None
    threshold = None
    unmeasurable = 2000
    minuteData = []
    minuteOfData = None
    previousTimeOfData = None
    count = 0

    def __init__(self, threshold=30):
        self.threshold = threshold  # default: 30 cm
    
    def setDefault(cls, dist):
        cls.defaultDist = dist
        if int(dist) >= (cls.unmeasurable - 50):
            print("注意: この設置場所では正しく計測できない可能性があります。\n超音波が反射するように設置場所を変えて再試行してください。\nできるだけ硬い面に相対させてください。\n")

    def check(cls, dist):
        if (abs(cls.defaultDist - int(dist))) >= cls.threshold:
            return True
        elif int(dist) >= cls.unmeasurable:
            return True
        return False

    def checkMin(cls, data):
        created = data["created"]
        createdMin = datetime.strftime(created, "%M")
        if cls.minuteOfData == None:
            cls.minuteOfData = createdMin
        if cls.previousTimeOfData == None:
            cls.previousTimeOfData = created

        print(createdMin)
        print(cls.minuteOfData)

        result = None

        if createdMin != cls.minuteOfData:
            result = cls.checkMinuteData(cls.minuteData, cls.previousTimeOfData)
            cls.minuteData = []
            cls.previousTimeOfData = created

        cls.minuteData.append(data)
        cls.minuteOfData = createdMin
        return result

    def checkMinuteData(cls, minuteData, created):
        count = 0
        length = len(minuteData)
        if length <= 1:
            return None
        else:
            for item in minuteData:
                isSeating = cls.check(item["d2"])   # d2: dist
                count += isSeating
            
            createdStr = datetime.strftime(created, "%Y-%m-%d %H:%M:00")
            if count >= length / 2:
                return {"created": createdStr, "d1": 1}
            else:
                return {"created": createdStr, "d1": 0}
