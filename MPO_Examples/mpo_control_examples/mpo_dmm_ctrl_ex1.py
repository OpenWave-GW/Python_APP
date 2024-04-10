# Name: mpo_dmm_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to utilize the DSO 
#   module to control the digital multimeter on the MPO.
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

if __name__ == '__main__':
    dso=gds.Dso() # Open a socket connection with MPO.
    dso.connect()
    
    # Set to the default settings.
    dso.default()
    
    # Activate the DMM. 
    if not dso.dmm.is_on():
        dso.dmm.set_on()

    #dso.dmm.set_mode_ACV(range='AUTO')  # Set DMM's mode as ACV.
    #dso.dmm.set_mode_DCA()              # Set DMM's mode as DCA.
    dso.dmm.set_mode_DCV()              # Set DMM's mode as DCV.
    #dso.dmm.set_mode_temperature(type='TYPEK', units='C', sim=23) # Set DMM's mode as temperature.
    
    time.sleep(2)
    for i in range(10):
        value=dso.dmm.get_value() # Get the DMM's measurement result.
        if(isinstance(value, str)):
            print(value)
        else:
            print('value=%.2f'%value)
        time.sleep(1)
    
    # Deactivate the DMM.
    if dso.dmm.is_on():
        dso.dmm.set_off()
    
    # Close the socket connection
    dso.close()
