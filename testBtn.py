import time
import digitalio
import board
import adafruit_character_lcd.character_lcd as characterlcd
from SendKey import SendKey

class LCD:
    def __init__(self):
        self.lcd_rs = digitalio.DigitalInOut(board.D26)
        self.lcd_en = digitalio.DigitalInOut(board.D19)
        self.lcd_d4 = digitalio.DigitalInOut(board.D13)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D5)
        self.lcd_d7 = digitalio.DigitalInOut(board.D11)
        self.lcd_lt = digitalio.DigitalInOut(board.D9)
        self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7, 16, 2, self.lcd_lt)

    def light(self):
        self.lcd.backlight = True

    def dark(self):
        self.lcd.backlight = False

    def clear(self):
        self.lcd.clear()

    def msg(self, msg):
        lcd.message = msg


class Btn:
    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN

    def getVal(self):
        return self.pin.value


key = SendKey()
btn1 = Btn(board.D4)
btn2 = Btn(board.D17)
btn3 = Btn(board.D21)
btn4 = Btn(board.D20)

counter = 0
msg = ""
while True:
    if btn1.getVal():
        print("btn1 pressed")
        key.send(key.S)
        key.release()
    if btn2.getVal():
        print("btn2 pressed")
        key.send(key.W)
        key.release()
    if btn3.getVal():
        print("btn3 pressed")
        key.send(key.A)
        key.release()
    if btn4.getVal():
        print("btn4 pressed")
        key.send(key.D)
        key.release()
    time.sleep(0.01)

















# # Press a
# write_report(NULL_CHAR*2+chr(26)+NULL_CHAR*5)
# # Release keys
# write_report(NULL_CHAR*8)
# # Press SHIFT + a = A
# write_report(chr(32)+NULL_CHAR+chr(4)+NULL_CHAR*5)

# # Press b
# write_report(NULL_CHAR*2+chr(5)+NULL_CHAR*5)
# # Release keys
# write_report(NULL_CHAR*8)
# # Press SHIFT + b = B
# write_report(chr(32)+NULL_CHAR+chr(5)+NULL_CHAR*5)

# # Press SPACE key
# write_report(NULL_CHAR*2+chr(44)+NULL_CHAR*5)

# # Press c key
# write_report(NULL_CHAR*2+chr(6)+NULL_CHAR*5)
# # Press d key
# write_report(NULL_CHAR*2+chr(7)+NULL_CHAR*5)

# # Press RETURN/ENTER key
# write_report(NULL_CHAR*2+chr(40)+NULL_CHAR*5)

# # Press e key
# write_report(NULL_CHAR*2+chr(8)+NULL_CHAR*5)
# # Press f key
# write_report(NULL_CHAR*2+chr(9)+NULL_CHAR*5)

# # Release all keys
# write_report(NULL_CHAR*8)

# # from adafruit_hid.keyboard import keyboard
# # from adafruit_hid.keycode import keycode
