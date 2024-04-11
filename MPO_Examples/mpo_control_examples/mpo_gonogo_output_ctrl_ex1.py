# Name: mpo_gonogo_output_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to utilize the DSO 
#   module to control the Go-NoGo output port on the MPO. Please note that the 
#   Go-NoGo output terminal adopts an open collector output port. A resistor (
#   such as 10k ohm) needs to be connected in series with the output terminal 
#   to a reference voltage (such as 5 volts).
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

    # Set the probe ratio, vertical scale, timebase, horizontal position of CH1.
    dso.channel.set_probe_ratio(ch=1, ratio=10)      # Set the probe attenuation ration to 10x.
    dso.channel.set_scale(ch=1, scale=2)             # Set the vertical scale to 2V/div.
    dso.trigger.set_mode(mode='NORMAL')              # Set the trigger mode to normal trigger.
    dso.trigger.set_level(value=1.0)                 # Set the trigger level to 1V.
    dso.timebase.set_timebase(hdiv=2e-01)            # Set the horizontal scale to 200ms/div.
    dso.timebase.set_hposition(hpos=8e-01)           # Set the horizontal position to 800ms.
    dso.opc()                                        # opc() is used to ensure that preceding configuration commands have been executed.
    time.sleep(0.2)                                  # Pre-trigger acquisition time delay for oscilloscope.

    for i in range(10):
        dso.gonogo.output_on()  # Turn on the output.
        time.sleep(0.1)
        dso.gonogo.output_off() # Turn off the output.
        time.sleep(0.05)
    
    # Close the socket connection
    dso.close()
