# Name: mpo_awg_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to configure the 
#   arbitrary waveform generator using the DSO module.
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

if __name__ == '__main__':
    dso=gds.Dso() # Open a socket connection with MPO.
    dso.connect()
    
    # Set to the default settings.
    dso.default()
    
    # Turn on CH1
    if not dso.channel.is_on(ch=1):
        dso.channel.set_on(ch=1)
    
    # Activate the AWG(channel 1), and set waveform, frequency, amplitude, offset at the same time. 
    if not dso.awg.is_on(ch=1): 
        dso.awg.set_on(ch=1,wave='SINE',freq=1e5,amp=2.5e-1,offset=0e0) 

    # Set the load to HighZ. 
    dso.awg.set_load_highz(ch=1) 

    # Set the load to 50 ohm. 
    dso.awg.set_load_50ohm(ch=1) 

    # Set the phase to 0.0. 
    dso.awg.set_phase(ch=1,value=0.0) 

    # Deactivate the AWG(channel 1). 
    #if dso.awg.is_on(ch=1): 
    #    dso.awg.set_off(ch=1)     

    # Close the socket connection
    dso.close()
