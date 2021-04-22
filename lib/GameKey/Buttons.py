import digitalio

import Pins

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
