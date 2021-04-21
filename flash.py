from machine import Pin
import time

import Buttons

btn = Buttons.button()

btn.loadButtons()

# matrix = [[
#     Pin(5, Pin.IN, Pin.PULL_DOWN),
#     Pin(4, Pin.IN, Pin.PULL_DOWN),
#     Pin(3, Pin.IN, Pin.PULL_DOWN),
#     Pin(2, Pin.IN, Pin.PULL_DOWN)
# ],[
#     Pin(13, Pin.IN, Pin.PULL_DOWN),
#     Pin(12, Pin.IN, Pin.PULL_DOWN),
#     Pin(11, Pin.IN, Pin.PULL_DOWN),
#     Pin(10, Pin.IN, Pin.PULL_DOWN)
# ]]


# while True:
#     x = 0
#     y = 0
#     for i in matrix:
#         x = x + 1
#         for j in i:
#             y = y + 1
#             if (j.value()):
#                 print('button: ' + str(x) + str(y))
# #     if(pin11.value()):
# #         print('pin11')
#     time.sleep(0.1)