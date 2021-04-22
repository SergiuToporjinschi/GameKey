import json

with open('USBKeyCodes.json', 'r') as j:
    usbKeyCodes = json.load(j)
    for k in usbKeyCodes.keys():
        print('"{0}": {1},'.format(k,hex(usbKeyCodes[k])))