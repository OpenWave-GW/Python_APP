# Name: mpo_dso_ctrl_ex1.py
#
# Description: This Python example script demonstrates the utilization of the 
#   "gds_info" module to establish communication with the MPO via internal socket 
#   connection. And perform basic settings for the oscilloscope.
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
        dso.channel.set_on(ch=1)                     # Turn on CH1.
    
    # Set the probe ratio, probe type, vertical scale, vertical position of CH1.
    dso.channel.set_probe_ratio(ch=1, ratio=10)      # Set the probe attenuation ration to 10x.
    dso.channel.set_probe_type(ch=1, type='VOLTAGE') # Set the probe type to voltage probe.
    dso.channel.set_scale(ch=1, scale=1)             # Set the vertical scale to 1V/div.
    dso.channel.set_pos(ch=1, vpos=0.0)              # Set the vertical position to 0V.
    
    # Set sampling mode and waveform length.
    dso.acquire.set_average(16)                      # Set the acquisition mode to average, and set the average number to 16.
    dso.acquire.set_length(100000)                   # Set the waveform length to 100k pts.
    
    # Set the horizontal scale.
    dso.timebase.set_timebase(hdiv=2e-04)            # Set the horizontal scale to 200us/div.
    
    # Set the trigger mode, trigger level.
    dso.trigger.set_mode(mode='AUTo')                # Set the trigger mode to auto trigger.
    dso.trigger.set_level(value=1.0)                 # Set the trigger level to 1V.
    
    # Close the socket connection
    dso.close()
