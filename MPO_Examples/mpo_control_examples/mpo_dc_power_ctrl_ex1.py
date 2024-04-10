# Name: mpo_dc_power_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to utilize the DSO 
#   module to control the DC power supply on the MPO.
#
# Author: GW Instek
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import gds_info as gds # Import the DSO module
import time
voltage=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

if __name__ == '__main__':
    dso=gds.Dso() # Open a socket connection with MPO.
    dso.connect()
    
    # Set to the default settings.
    dso.default()

    # Set the probe ratio, probe type, vertical scale, vertical position of CH1.
    dso.channel.set_probe_ratio(ch=1, ratio=10)      # Set the probe attenuation ration to 10x.
    dso.channel.set_probe_type(ch=1, type='VOLTAGE') # Set the probe type to voltage probe.
    dso.channel.set_scale(ch=1, scale=2)             # Set the vertical scale to 2V/div.
    dso.channel.set_pos(ch=1, vpos=-4.0)             # Set the vertical position to -4V.
    
    # Set 0V on channel 1.
    dso.power.set_voltage(ch=1, volt=0)

    # Turn on the power supply.
    if not dso.power.is_on(1):
        dso.power.set_on(1)
            
    length=len(voltage)
    for i in range(length):
        # Reconfigure the power supply when OCP occurred on channel 1.
        if(dso.power.check_ocp(1)):
            dso.power.clear_ocp(1)
        
        dso.power.set_voltage(ch=1, volt=voltage[i])
        time.sleep(1)
    
    # Turn off the power supply.
    if dso.power.is_on(1):
        dso.power.set_off(1)
    
    # Close the socket connection
    dso.close()
