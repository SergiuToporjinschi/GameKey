import json
import time
import Pins

import digitalio
from analogio import AnalogIn


import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

time.sleep(1)
keyboard = Keyboard(usb_hid.devices)


class Button:

    def __init__(self, data, name):
        self.name = name
        print('Initializing button: ' + name)
        print('Pin: ' + str(data['gpio']))
        self.pin = digitalio.DigitalInOut(Pins.Digital[data['gpio']])
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN

    def pressed(self):
        keyboard_layout.write('d')

    def released(self):
        keyboard_layout.write('u')

class Buttons:
    btns = []
    def __init__(self, config):
        self.config = config
        self.initButtons()
        self.keypressed = []

    def initButtons(self):
        btnCnt = 0
        for i in self.config:
            name = next(iter(i.keys()))
            self.btns.append(Button(i[name], name))
            btnCnt = btnCnt + 1

    def scanButtons(self):
        ret = []
        for btn in self.btns:
            if btn.pin.value:
                ret.append(btn.name)
        return ret

class Joystick:
    axes = []
    def __init__(self, config):
        self.config = config
        self.init()

    #initialize joystick
    def init(self):
        axex = type('', (), {})
        axex.pin = AnalogIn(Pins.Analog[self.config['x']['gpio']])
        axex.name = 'x'
        self.axes.append(axex)
        axey = type('', (), {})
        axey.pin = AnalogIn(Pins.Analog[self.config['y']['gpio']])
        axey.name = 'y'
        self.axes.append(axey)
        self.btn = digitalio.DigitalInOut(Pins.Digital[self.config['btn']['gpio']])
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP

    def getValue(self, value):
        value = round((value/65535)*100)
        if value < 50:
            value = (100 - value) * -1
        elif value == 50:
            value = 0
        elif value > 50:
            value = (value - 50) *2

        if abs(value) < self.config['trashHold']:
            value = 0
        return value

    def scanJoystick(self):
        # print(self.btn.value)
        ret = []
        for axe in self.axes:
            axeValue = self.getValue(axe.pin.value)
            if axeValue != 0:
                direction = "+"
                if axeValue < 0:
                    direction = "-"
                ret.append("{0}:{1}".format(self.config[axe.name][direction], str(abs(axeValue))))
        if not self.btn.value:
            ret.append(btn.name)
        return ret

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
