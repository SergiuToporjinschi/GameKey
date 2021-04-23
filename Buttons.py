import json
import time
import Pins

import usb_hid
from adafruit_hid.keyboard import Keyboard
# from adafruit_hid.keycode import Keycode

from GameKey.Buttons import Buttons
from GameKey.Joystick import Joystick
from GameKey.Joystick import JoystickCalibration

keyboard = Keyboard(usb_hid.devices)

class ConvertToKeys:
    def __init__(self, mapFileName, usbKeyCodes):
        with open(usbKeyCodes, 'r') as j:
            usbKeyCodes = json.load(j)
            keys = usbKeyCodes['keys'].copy()
            self.keyCodes = usbKeyCodes['modifiers']
            self.keyCodes.update(keys)

        with open(mapFileName, 'r') as j:
            mapping = json.load(j)
            self.btnMap = mapping['buttons']
            self.joyMap = mapping['joystick']
        self.addDefaultValues()

    def addDefaultValues(self):
        if not isinstance(self.joyMap['slowProcentage'], int):
            print('Remove joystick\slowProcentage: not valid type')
            del self.joyMap['slowProcentage']

        if not 'slowProcentage' in self.joyMap:
            print('Set "slowProcentage" with default (90%) ')
            self.joyMap['slowProcentage'] = 90

        for key, value in self.btnMap.items():
            if not isinstance(value, str) and not isinstance(value, list):
                print(
                    'Remove buttons\[{0}:{1}]: not valid type'.format(key, value))
                del self.btnMap[key]

    def convert(self, btns, joys):
        ret = []
        if len(btns) > 0:
            ret = ret + self.convertBtn(btns)
        if len(joys) > 0:
            ret = ret + self.convertJoys(joys)
        return ret

    def convertBtn(self, keys):
        ret = []
        for key in keys:
            if not key in self.btnMap:
                continue
            if isinstance(self.btnMap[key], str):
                ret.append(self.btnMap[key])
            elif isinstance(self.btnMap[key], list):
                ret = ret + self.btnMap[key]
        return ret

    def convertJoys(self, joyMoves):
        ret = []
        for m in joyMoves:
            if ':' in m:
                key = m.split(':')[0]
                val = m.split(':')[1]
                if int(val) < self.joyMap['slowProcentage']:
                    ret.append(self.joyMap[key]['slow'])
                else:
                    ret.append(self.joyMap[key]['fast'])
        return ret

    def convertToUSBCode(self, *keyList):
        ret = []
        for k in keyList:
            ret.append(int(self.keyCodes[k], 16))
        return ret

def loadConfig():
    with open('Pins.json', 'r') as j:
        return json.load(j)

def sendKeys(keys, convertor):
    toSend = []
    for i in keys:
        if ':' in i:
            modifier = i.split(':')[0]
            key = i.split(":")[1]
            toSend = toSend + convertor.convertToUSBCode(modifier, key)
        else:
            toSend = toSend + convertor.convertToUSBCode(i.lower())
    # keyboard.press(*toSend)



config = loadConfig()
convertor = ConvertToKeys('BtnMap.json', 'USBKeyCodes.json')
btns = Buttons(config['buttons'])
joy = Joystick(config['joystick'])
calibration = JoystickCalibration(joy, keyboard)

# Start calibration if need it
bts = btns.scanButtons()
if len(bts) > 2:
    calibration.beginCalibration()
#end calibration

lastOut = []
lastLen = 0
while True:
    # print(value)
    out = convertor.convert(btns.scanButtons(), joy.scanJoystick())
    if set(lastOut) != set(out):
        keyboard.release_all()
        if len(out) > 0:
            sendKeys(out)
            lastOut = out
        elif lastLen != len(out):
            print('out')
            lastOut = []
            keyboard.release_all()
    lastLen = len(out)
    time.sleep(0.01)
