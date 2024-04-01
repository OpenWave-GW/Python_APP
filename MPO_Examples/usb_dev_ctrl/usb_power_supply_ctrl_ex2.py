# Name: usb_power_supply_ctrl_ex2.py
#
# Description: This Python example script demonstrates the utilization of the  
#   "psw" module to establish communication with a DC power supply via USB 
#   interface. It illustrates the process of setting the output to ON and 
#   incrementing the output voltage from 0V to 10.0V.
#
# Author: GW Instek
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import psw
import time
import sys

PSW_SN = 'GEW192100' # Device serial number
volt=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

if __name__ == '__main__':
    inst = psw.Psw()
    try:
        inst.connect(PSW_SN)
        print(inst.idn())
    except:
        print('Please check the interface connection!')
        sys.exit()        # Terminate the program.
    
    inst.set_voltage(0.0) # Set the output voltage value to 0V.
    inst.set_ocp(1.0)     # Set the over current protection value to 1A.
    inst.set_on()         # Set the output to ON.
    time.sleep(0.5)
    for i in range(10):
        voltage=volt[i]
        inst.set_voltage(voltage)
        time.sleep(0.5)
    inst.set_off()
    inst.close()