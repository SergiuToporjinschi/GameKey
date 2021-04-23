import Pins
import time
import digitalio
from analogio import AnalogIn

from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


class Joystick:
    axes = []

    def __init__(self, config):
        self.config = config
        self.init()

    # initialize joystick
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
        value = round((value/(65224-264))*100)
        if value < 50:
            value = (100 - value) * -1
        elif value == 50:
            value = 0
        elif value > 50:
            value = (value - 50) * 2
        if abs(value) < self.config['trashHold']:
            value = 0
        return value

    def scanJoystick(self):
        # print(self.btn.value)
        ret = []
        for axe in self.axes:
            axeValue = self.getValue(axe.pin.value)
            if axe.name == 'x':
                print('{0}:{1}%'.format(axe.pin.value, axeValue))
            if axeValue != 0:
                direction = "+"
                if axeValue < 0:
                    direction = "-"
                ret.append("{0}:{1}".format(self.config[axe.name][direction], str(abs(axeValue))))
        if not self.btn.value:
            ret.append(btn.name)
        return ret


class JoystickCalibration:
    def __init__(self, joystick, keyboard):
        self.joystick = joystick
        self.keyboard = keyboard
        self.kbLayout = KeyboardLayoutUS(keyboard)
        self.calibration = {}


    def beginCalibration(self):
        result = ""
        procentageOkPlus = 65536 * 0.75 # 49152
        procentageOkMinus = 65536 * 0.25 # 16384

        self.keyboard.send(Keycode.WINDOWS, Keycode.R)
        time.sleep(1)
        self.kbLayout.write('notepad \n')
        time.sleep(1)

        self.kbLayout.write('Joystick calibration...\n')
        time.sleep(3)
        self.kbLayout.write('Hi! Your computer has a nice USB port, It`s so powerfull, it`s giving me LIFE :), I like it here... \n')
        self.kbLayout.write('Let`s make sure I have enough space... \n')
        time.sleep(1)
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        self.keyboard.send(Keycode.X)

        self.kbLayout.write('Don`t touch any of my key, your keyboard or mouse... I`m not here for socializing. \n')
        self.kbLayout.write('So... let`s get to work \n')
        time.sleep(2)
        self.kbLayout.write('Make sure joystick is released. Calibration begins in 20 sec ...\n')
        time.sleep(1)
        self.__wait(20)
        self.keyboard.send(Keycode.ENTER)

        self.kbLayout.write('Calibrating X0: ...')
        self.calibration['X0'] = self.__calibrate(self.joystick.axes[0])  # calibration X0
        self.__delLast(3)
        self.kbLayout.write(str(self.calibration['X0']) + "\n")

        self.kbLayout.write('Calibrating Y0: ...')
        self.calibration['Y0'] = self.__calibrate(self.joystick.axes[1])  # calibration Y0
        self.__delLast(3)
        self.kbLayout.write(str(self.calibration['Y0']) + "\n")

        self.kbLayout.write('Now, I need your help.\n')
        self.kbLayout.write('You have to push X("Walk forward") to maximum and keep it there until I told you \n')
        self.kbLayout.write('Get ready, start pushing, we begin in 20 sec')
        self.__wait(20, 4)
        self.kbLayout.write('Calibrating XMax: ...')
        self.calibration['XMax'] = self.__calibrate(self.joystick.axes[0])  # calibrate XMax
        self.__delLast(3)
        if self.calibration['XMax'] > procentageOkPlus : result = " OK "
        else: result = " NOT OK!!!!!"
        self.kbLayout.write(str(self.calibration['XMax']) + result + " \n")
        self.kbLayout.write('Thank you! Release it now \n')

        self.kbLayout.write('Now, you have to pull X("Walk backward") to maximum and keep it there until I told you \n')
        self.kbLayout.write('Get ready, start pulling, we begin in 20 sec')
        self.__wait(20, 4)
        self.kbLayout.write('Calibrating XMin: ...')
        self.calibration['XMin'] = self.__calibrate(self.joystick.axes[0])  # calibrate XMin
        self.__delLast(3)
        if self.calibration['XMin'] < procentageOkMinus : result = " OK "
        else: result = " NOT OK!!!!!"
        self.kbLayout.write(str(self.calibration['XMin']) + result + "\n")

        self.kbLayout.write('Thank you! Release it now \n')

        self.kbLayout.write('Now, you have to push Y("Walk to the right") to maximum and keep it there until I told you \n')
        self.kbLayout.write('Get ready, start pushing, we begin in 20 sec')
        self.__wait(20, 4)
        self.kbLayout.write('Calibrating YMax: ...')
        self.calibration['YMax'] = self.__calibrate(self.joystick.axes[1])  # calibrate YMin
        self.__delLast(3)
        if self.calibration['XMax'] > procentageOkPlus : result = " OK "
        else: result = "NOT OK!!!!!"
        self.kbLayout.write(str(self.calibration['YMax']) + result + " \n")

        self.kbLayout.write('Thank you! Release it now \n')

        self.kbLayout.write('Now, you have to push Y("Walk to the left") to maximum and keep it there until I told you \n')
        self.kbLayout.write('Get ready, start pushing, we begin in 20 sec')
        self.__wait(20, 4)
        self.kbLayout.write('Calibrating YMin: ...')
        self.calibration['YMin'] = self.__calibrate(self.joystick.axes[1])  # calibrate YMin
        self.__delLast(3)
        if self.calibration['XMin'] < procentageOkMinus : result = " OK "
        else: result = " NOT OK!!!!!"
        self.kbLayout.write(str(self.calibration['YMin']) + result + " \n")

        self.kbLayout.write('Thank you! I`m done here \n')
        self.kbLayout.write('If you saw some "NOT OK" messages, you have to repeat the calibration \n')

        self.kbLayout.write('I`ve added a new volume to "My computer" well... your computer with  the name "GAMEKEY", you have to edit Pins.Json with any text editor and put this values in joystick>calibration \n')
        self.kbLayout.write('Don`t forget to save the file.... \n')
        time.sleep(3)
        self.kbLayout.write('Ohhh don`t mess the files or file formats.... you know... are mine... you can also edit and adapt shortcut keys in BtnMap.json \n')
        time.sleep(2)
        self.kbLayout.write('Just to make sure... Here.. you can copy paste this, I know you are good on this: \n')
        self.kbLayout.write('"X0": {0}, \n'.format(self.calibration['X0']))
        self.kbLayout.write('"Y0": {0}, \n'.format(self.calibration['Y0']))
        self.kbLayout.write('"XMax": {0}, \n'.format(self.calibration['XMax']))
        self.kbLayout.write('"XMin": {0}, \n'.format(self.calibration['XMin']))
        self.kbLayout.write('"YMax": {0}, \n'.format(self.calibration['YMax']))
        self.kbLayout.write('"YMin": {0} \n'.format(self.calibration['YMin']))

        self.kbLayout.write('After changing the files, don`t forget reconnect me to your computer, like I said, I like it here ;) \n')
        self.kbLayout.write('I will open the file explorer for you! and then ... let`s play something \n')
        time.sleep(2)
        self.kbLayout.write('The keyboard is yours now. Bye!!!')
        self.keyboard.send(Keycode.WINDOWS, Keycode.E)

    def __delLast(self, cnt):
        for i in range(cnt):
            self.keyboard.send(Keycode.BACKSPACE)

    def __wait(self, sec, back=0):
        if back > 0:
            for r in range(back):
                self.keyboard.send(Keycode.LEFT_ARROW)
            for r in range(len(str(sec))):
                self.keyboard.send(Keycode.BACKSPACE)

        for i in range(sec, -1, -1):
            self.kbLayout.write(str(i))
            time.sleep(1)
            for r in range(len(str(i))):
                self.keyboard.send(Keycode.BACKSPACE)
        self.kbLayout.write("0")
        if back > 0:
            self.keyboard.send(Keycode.END)
            self.keyboard.send(Keycode.ENTER)

    def __calibrate(self, axe):
        total = 0
        for i in range(50, 0, -1):
            total += axe.pin.value
        return int(round(total/50, 0))

# min - 264
# 0   - 32992
# max - 65520
