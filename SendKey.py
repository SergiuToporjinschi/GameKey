import json

class SendKey:
    NULL_CHAR = chr(0)
    W = chr(26)
    S = chr(22)
    A = chr(4)
    D = chr(7)
    SP = chr(44)
    EN = chr(40)
    SH = chr(32)

    def __init__(self):
        self.loadUSBKeyCodes()
        self.loadKeyMap()

    def write_report(self, report):
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())


    def send(self, char, sh=False):
        # try:
        if sh:
            self.write_report(self.SH + self.NULL_CHAR + char + self.NULL_CHAR * 5)
        else:
            self.write_report(self.NULL_CHAR * 2 + char + self.NULL_CHAR * 5)
        # except:
        #     self.release()

    def release(self):
        self.write_report(self.NULL_CHAR*8)

    def loadUSBKeyCodes(self):
        with open('USBKeyCodes.json', 'r') as j:
            self.usbKeyCodes = json.load(j)

    def loadKeyMap(self):
        with open('MouseBtnMap.json', 'r') as j:
            self.keyMap = json.load(j)


