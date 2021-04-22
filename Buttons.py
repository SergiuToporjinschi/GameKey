import json
import time
import Pins

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from GameKey.Buttons import Buttons
from GameKey.Joystick import Joystick

time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
print('hello')

class ConvertToKeys:
    def __init__(self, mapFileName):
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
            self.joyMap['slowProcentage'] =  90

        for key, value  in self.btnMap.items():
            if not isinstance(value, str) and not isinstance(value, list):
                print('Remove buttons\[{0}:{1}]: not valid type'.format(key, value))
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
            if not key in self.btnMap: continue
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

kb = KeyboardLayoutUS(keyboard)

def sendKeys(keys):
    strToSend = ""
    for i in keys:
        if 'SHIFT' in i:
            val = i.split(':')[1]
            # kb._char_to_keycode()
            strToSend = strToSend + 'Keycode.SHIFT, Keycode.{0},'.format(val.upper())
        else:
            strToSend = strToSend + 'Keycode.{0},'.format(i.upper())
    print(strToSend)
    eval('keyboard.press({0})'.format(strToSend))
#


convertor = ConvertToKeys('BtnMap.json')

btnMap = ""

config = 0
with open('Pins.json', 'r') as j:
    config = json.load(j)

btns = Buttons(config['buttons'])
joy = Joystick(config['joystick'])

lastOut = []
lastLen = 0
while True:
    # print(value)
    out = convertor.convert(btns.scanButtons(), joy.scanJoystick())
    if set(lastOut) != set(out):
        keyboard.release_all()
        if len(out) > 0:
            print(out)
            sendKeys(out)
            lastOut = out
        elif lastLen != len(out):
            print('out')
            lastOut = []
            keyboard.release_all()
    lastLen = len(out)
    time.sleep(0.01)
