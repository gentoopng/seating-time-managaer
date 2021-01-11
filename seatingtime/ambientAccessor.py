import ambient

class AmbientAccessor:
    WRITE_KEY = None
    CHANNEL_ID = None
    # data = None
    ambi = None

    def __init__(self, writekey, channelid):
        self.WRITE_KEY = writekey
        self.CHANNEL_ID = channelid
        self.data = []
        self.ambi = ambient.Ambient(self.CHANNEL_ID, self.WRITE_KEY)
    
    def send(cls, data1, data2):
        d1 = []
        d2 = []
        d1.append(data1)
        d2.append(data2)

        r = cls.ambi.send({"d1": d1, "d2": d2})
        print(r)
    
    def send(cls, data={}):
        r = cls.ambi.send(data)
        print(r)
        