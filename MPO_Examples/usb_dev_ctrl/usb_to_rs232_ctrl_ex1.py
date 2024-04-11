# Name: usb_to_rs232_ctrl_ex1.py
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

if __name__=='__main__':
    ttystr = '/dev/ttyUSB0'  # External USB device location
    try:
        usb = serial.Serial(ttystr, baudrate=9600, timeout=3)
        usb.write('*idn?\n')
        str1 = usb.read(100).decode().split(',')
        print(str1)
    except:
        print('Serial Connection Error!')
    usb.close()