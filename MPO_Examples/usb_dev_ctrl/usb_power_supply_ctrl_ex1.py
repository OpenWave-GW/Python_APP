# Name: usb_power_supply_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to use the "serial"
#   module to establish communication with a DC power supply via USB interface 
#   and retrieve its identification information using the "*IDN?" command.
#
# Author: GW Instek
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import serial

if __name__=='__main__':
    ttystr = '/dev/ttyACM0'  # External USB device location
    try: 
        acm = serial.Serial(ttystr, baudrate=115200, timeout=3)
        acm.write('*idn?\n')
        str1 = acm.read(100).decode().split(',')
        print(str1)
    except:
        print('Serial Connection Error!')
    acm.close()