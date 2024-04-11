# Name: usb_to_rs232_ctrl_ex2.py
#
# Description: This Python example script demonstrates how to use the "serial"
#   module to establish communication via the USB interface of the MPO-2000 using 
#   a USB to RS232 converter cable. Through the RS232 interface of a DMM, the 
#   script communicates with the DMM to retrieve its "*IDN?" information.
#   Please note that the baud rate setting of the USB to RS232 cable in the script 
#   must match the RS232 interface setting on the DMM. Additionally, we currently 
#   only support drivers for the FT232RL and PL2303 chips.
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
USB_MAX = '9'  # Search device from USB0 to USB_MAX
GDM_NAME = 'GDM8261A'  # Device name

def USB_Connect(device_name, device_sn=False):
    global usb
    numUSBMAX = int(USB_MAX)
    numUSB = 0
    while(True):
        if numUSB > numUSBMAX:
            print('%s not found!' % (device_name))
            sys.exit()
        ttystr = '/dev/ttyUSB' + str(numUSB)
        print('Searching...',ttystr)
        try:
            usb = serial.Serial(ttystr, baudrate=9600, timeout=3)
        except:
            print('Serial Connection Error!')
            sys.exit()
        usb.write('*idn?\n')
        str1 = usb.read(100).decode().split(',')
        if len(str1) > 1:
            if device_sn != False:
                if str1[1] == device_name and str1[2] == device_sn:
                    print('Connect to', str1[1], str1)
                    break
            else:
                if str1[1] == device_name:
                    print('Connect to', str1[1], str1)
                    break
        numUSB += 1
    return usb

if __name__ == '__main__':
    device = USB_Connect(GDM_NAME) #Connect to Instrument
    device.write('*idn?\n')
    str = device.read(100).decode().split(',')
    print(str[1])
    device.close()
