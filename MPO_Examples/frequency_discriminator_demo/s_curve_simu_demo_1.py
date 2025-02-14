# Name: s_curve_simu_demo_1.py
#
# Description:  
# This Python script simulates an experiment to measure the S-curve of a demodulator
# (e.g., MC1496) using the AWG and oscilloscope on the MPO-2000. The script controls
# AWG channel 1 to generate DC levels corresponding to various demodulator outputs, 
# while the oscilloscope sequentially measures the DC value at the AWG output. A 
# GUI library then plots the frequency vs. amplitude characteristic curve on the 
# screen, illustrating the simulated response of the demodulator.
#
# Author: Kevin Meng
# Date: SEP.03.2024
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import os
import time
import sys
import gc

param = {
    "output_filename" : 'f_v_data',
    "freq_start": 4500000,
    "freq_end": 5500000,
    "points_num": 101,
    "draw_curve": True,
}

awg_dc_output=[0.370, 0.370, 0.365, 0.360, 0.355, 0.347, 0.342, 0.334, 0.326, 0.319,
               0.311, 0.303, 0.293, 0.285, 0.278, 0.267, 0.257, 0.247, 0.237, 0.226,
               0.216, 0.206, 0.198, 0.190, 0.185, 0.180, 0.180, 0.188, 0.201, 0.219,
               0.247, 0.283, 0.329, 0.380, 0.440, 0.512, 0.586, 0.668, 0.745, 0.817,
               0.882, 0.936, 0.979, 1.013, 1.044, 1.062, 1.074, 1.080, 1.080, 1.077,
               1.072, 1.062, 1.049, 1.038, 1.026, 1.013, 1.000, 0.990, 0.977, 0.966,
               0.954, 0.946, 0.936, 0.925, 0.918, 0.907, 0.900, 0.889, 0.884, 0.876,
               0.869, 0.861, 0.856, 0.848, 0.843, 0.838, 0.830, 0.828, 0.823, 0.817,
               0.812, 0.807, 0.805, 0.799, 0.797, 0.792, 0.789, 0.787, 0.781, 0.779,
               0.776, 0.774, 0.771, 0.769, 0.763, 0.761, 0.758, 0.756, 0.756, 0.753,
               0.751]

def instrument_init():
    dso.default()
    dso.opc()
    
def freq_vout_chart_init():
    size = gds.Screen()
    gds_color = gds.Theme(True)
    gui = dso_gui.DrawObject()

    gui.draw_fillrect_ex(0,0,size.width-1,size.height-1,gds_color.bg_color)
    gui.draw_rect_ex(0,0,size.width-1,size.height-1,gds_color.grid_color)

    draw_f_t = gui.Plot(120, 50, 650, 350, dark_mode=True)

    gui.draw_text(250, 10, 'Frequency Discriminator (Simulated Data)', color=gds_color.text_color)
    gui.draw_text(360, 445, 'Frequency(MHz)', color=gds_color.text_color)
    gui.draw_text(25, 280, 'Vo(V)', rol=270, color=gds_color.text_color)
    return draw_f_t

def calc_dc_value_from_waveform(ch, v_div):
    dso.gonogo.output_on()  # Set gonogo IO to output low.(debugging)
    waveform=dso.get_waveform_num(ch, real_value=False, pos_consider=False)
    dso.gonogo.output_off() # Set gonogo IO to output high.(debugging)
    num=len(waveform)
    wave_sum=sum(waveform)
    return (float(wave_sum)*v_div)/(num*25)

def simu_awg_arb_output(ch):
    arb_wave = 'awg_arb_simu.CSV'
    dso.write(':AWG%d:ARB:LOAD:WAVE "Disk:/%s"'%(ch, arb_wave))
    dso.opc()
    dso.write(':AWG%d:FUNC ARB'%ch)
    dso.write(':AWG%d:FREQ 500'%ch) # 500Hz
    dso.write(':AWG%d:AMP 1.0'%ch)  # AWG amplitude 1V
    dso.write(':AWG%d:OFFS 0.6'%ch) # AWG offset 600mV
    dso.write(':AWG%d:OUTP:STAT ON'%ch)
    dso.opc()

def simu_awg_dc_output(ch, dcv):
    dso.write(':AWG%d:FUNC DC'%ch)
    dso.write(':AWG%d:OFFS %f'%(ch, dcv))
    dso.write(':AWG%d:OUTP:STAT ON'%ch)
    dso.opc()

def frequency_discriminator(save_waveform:bool, save_vo_freq:bool, save_image:bool):
    freq_step = (param['freq_end'] - param['freq_start']) / (param['points_num'] - 1)
    frequencies = [round(param['freq_start'] + i * freq_step) for i in range(param['points_num'])]
    dso_ch = 1
    dso_timebase = 5e-4  # 500us/div
    awg_ch = 1

    if save_vo_freq:
        filename = f"{param['output_filename']}.csv"
        file = open('/mnt/disk/' + filename, 'w')
        file.write('Frequency(MHz), Vo(V),\n')

    #if param['draw_curve']:
    #    draw_f_t = freq_vout_chart_init()

    #dso.awg.set_load_50ohm(ch=awg_ch)  #  Load: 50 ohm
    dso.awg.set_load_highz(ch=awg_ch)   #  Load: 1M ohm
    dso.timebase.set_timebase(dso_timebase) # Set timebase to 500 us/div.
    simu_awg_arb_output(1)
    dso.opc()
    time.sleep(0.5)

    dso.write(':AUTORSET:MOD ACP')  # Autoset with AC priority ON.
    dso.autoset()
    dso.opc()
    dso.timebase.set_timebase(dso_timebase) # Set timebase to 500 us/div.

    ch_vdiv = dso.channel.get_scale(dso_ch)
    ch_vpos = dso.channel.get_pos(dso_ch)
    print('Scale: %.2f V, Position: %.2f V'%(ch_vdiv, ch_vpos))
    time.sleep(0.5)

    if param['draw_curve']:
        draw_f_t = freq_vout_chart_init()

    dso.timebase.set_timebase(1e-5) # Set timebase to 10 us/div
    dso.stop()
    item_num=len(frequencies)
    dso.write(':AWG%d:FREQ %f'%(awg_ch, frequencies[0]))
    simu_awg_dc_output(1, awg_dc_output[0])
    time.sleep(0.5)
    print('num=', len(awg_dc_output))
    for i in range(item_num):
        dso.single() # Set single trigger(acquisition starting)
        dso.force()  # Set force trigger.(fast than auto trigger)
        #vo = float(dso.meas.get_mean(dso_ch))
        vo=calc_dc_value_from_waveform(dso_ch, ch_vdiv)
        freq=frequencies[i]
        f=freq/1000000.0  # Change unit to MHz.

        if save_vo_freq:
            file.write('%.3f, %.3f\n'%(freq, vo))

        if freq == param['freq_start']: 
            print('\nFrequency(MHz) - Vo(V)')
        print('%.3f MHz - %.3f V'%(f, vo))
        
        # Set AWG output DC level.
        if(i < (item_num-1)):
            #print('i=', i)
            dso.write(':AWG%d:OFFS %f'%(1, awg_dc_output[i+1]))

        if param['draw_curve']:
            draw_f_t.plot(f, vo, color=color.LTGREEN)
        else:
            time.sleep(0.5)
        gc.collect()     
    dso.awg.set_off(ch=awg_ch)

    if param['draw_curve'] and save_image :
        dso.hardcopy.hard_copy(mode='IMAGe')

    if save_vo_freq:
        file.close()    

if __name__ == '__main__':
    os.chdir(sys.path[0])
    from dso_const import *
    try:
        import gds_info as gds
    except ImportError:
        import dso2kp as gds
    import dso_gui
    import dso_colors as color

    dso = gds.Dso()
    dso.connect()
    
    instrument_init()
    frequency_discriminator(save_waveform=False, save_vo_freq=False, save_image=False)

    dso.dsodraw.draw_poptext("Complete!")
    dso.run()
    dso.close()
