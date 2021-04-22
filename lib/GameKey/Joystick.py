import Pins

import digitalio
from analogio import AnalogIn

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
