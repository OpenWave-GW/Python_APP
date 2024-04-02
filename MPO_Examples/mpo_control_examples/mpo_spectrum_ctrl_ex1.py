# Name: mpo_spectrum_ctrl_ex1.py
#
# Description: This Python example script demonstrates how to configure the 
#   spectrum analysis function using the DSO module.
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

    # Activate the spectrum mode.
    if not dso.sa.is_spectrum_mode():
        dso.sa.set_spectrum_mode('ON')

    # Activate the input source.
    if not dso.sa.get_state(_id=1):
        dso.sa.set_state(state='ON',_id=1)

    # Activate the spectrum trace.
    if not dso.sa.is_spectrum_trace(trace_type='NORMAL',_id=1):
        dso.sa.set_spectrum_trace(trace_type='NORMAL',state='ON',_id=1)

    # set the center frequency to 25 MHz.
    dso.sa.set_freq(freq=25e6,_id=1)
    # Get the center frequency.
    freq_cent=dso.sa.get_freq(_id=1)
    print('Center frequency: %f'%freq_cent)
    
    # Set the span frequency to 25 MHz.
    dso.sa.set_span(freq=25e6,_id=1)
    # Get the span frequency.
    freq=dso.sa.get_span(_id=1)
    print('Span frequency: %.2f'%freq)

    # Set the start frequency to 12.5 MHz.
    dso.sa.set_start(freq=12.5e6,_id=1)
    # Get the start frequency.
    freq=dso.sa.get_start(_id=1)
    print('Start frequency: %.2f'%freq)
    
    # Set the stop frequency to 37.5 MHz.
    dso.sa.set_stop(freq=37.5e6,_id=1)
    # Get the stop frequency.
    freq=dso.sa.get_stop(_id=1)
    print('Stop frequency: %.2f'%freq)
    
    # Set the RBW value in the manual mode.
    dso.sa.set_RBW_Manual(rbw=2.5e4, _id=1)
    
    # Set the "Span:RBW" in the auto-RBW mode.
    dso.sa.set_Span2RBW_Ratio(ratio='RATIO_1K',_id=1)
    
    # Set the window type.
    dso.sa.set_window(window=2,_id=1)
    
    # Set the vertical scale and unit.
    dso.sa.set_scale(scale=2.0e1,unit=0,_id=1)
    
    # Set the zero level position.
    dso.sa.set_position(position=3.0e0,_id=1)
    
    # Deactivate the spectrum mode.
    if dso.sa.is_spectrum_mode():
        time.sleep(2)
        dso.sa.set_spectrum_mode('OFF')
    