#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

try:
    # Press a
    write_report(chr(20) + NULL_CHAR*2+chr(4)+NULL_CHAR*5)
    # Release keys
    write_report(NULL_CHAR*8)
except:
    # Release all keys
    write_report(NULL_CHAR*8)