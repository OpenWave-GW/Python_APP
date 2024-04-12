# Name: usb_power_supply_ctrl_ex3.py
#
# Description: This Python example script demonstrates the utilization of the  
#   "serial" module to establish communication with a DC power supply via USB 
#   interface.
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
import sys

PSW_NAME = 'PSW160-14.4'# Device name
#PSW_NAME = 'PPX-1005'# Device name
ACM_MAX = '9'  # Search device from ACM0 to ACM_MAX

def ACM_Connect(device_name, device_sn=False):
    global acm
    numACMMAX = int(ACM_MAX)
    numACM = 0
    while(True):
        if numACM > numACMMAX:
            print('%s not found!' % (device_name))
            sys.exit()
        ttystr = '/dev/ttyACM' + str(numACM)
        print('Searching...',ttystr)
        try:
            acm = serial.Serial(ttystr, baudrate=115200, timeout=3)
        except:
            print('Serial Connection Error!')
            sys.exit()

        acm.write('*idn?\n')
        str1 = acm.read(100).decode().split(',')
        if len(str1) > 1:
            if device_sn != False:
                if str1[1] == device_name and str1[2] == device_sn:
                    print('Connected with ', str1[1], str1)
                    break
            else:
                if str1[1] == device_name:
                    print('Connected with ', str1[1], str1)
                    break
        numACM += 1
    return acm

if __name__ == '__main__':
    ACM_MAX = '9'# Search device from ACM0 to ACM_MAX
    device = ACM_Connect(PSW_NAME) # Connected with external device
    device.write('*idn?\n')
    str = device.read(100).decode().split(',')
    print(str[1])
