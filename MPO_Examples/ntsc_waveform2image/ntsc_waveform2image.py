# File Name: ntsc_waveform2image.py
#
# Description:
# This Python script can be executed directly on the MPO-2000 oscilloscope. It
# converts the NTSC video signal measured by the oscilloscope into an image 
# displayed on the oscilloscope screen. Since the amplitude and range of the 
# actual video signal may vary, adjustments to the vertical scale and trigger 
# level may be required. To achieve better image quality, the waveform should be
# adjusted to occupy the full screen for optimal sampling.
#
# Author: Kevin Meng
# Date: Jan.22.2025
# License: GW Python APP License
# Copyright (c) 2024 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import lvgl as lv
import time, sys
import gc
import struct

LINE_PERIOD = 63555.56 # In ns, line period = 63.55556us

def lv_gen_color_table():
    for i in range(256):
        color_table.append(lv.color_make(i, i, i))

def instrument_init():
#    dso.default()
#    dso.opc()
    dso.timebase.set_timebase(5e-3)    # Timebase: 5ms/div
    dso.timebase.set_hposition(2.5e-2) # Horizontal position: 25ms
    dso.acquire.set_length(1e6)        # Acquire memory length: 1M pts => sampling period: 50ns
    dso.channel.set_probe_ratio(1, 10) # CH1 probe x10, 200mV/div
#    dso.channel.set_scale(1, 0.2)      # 
#    dso.channel.set_pos(1, -1.248)     # vertical position: -1.248V
    dso.trigger.set_source('CH1')      # Set trigger source: CH1, level: 480mV
#    dso.trigger.set_level(0.48)        # 
    dso.trigger.set_type('VIDEO')      # Set video trigger, NTSC, odd field Line 23
    dso.write(':TRIG:VID:TYP NTSC')    # 
    dso.write(':TRIG:VIDeo:FIELd FIELD1')
    dso.write(':TRIG:VIDeo:LINe 23')
    dso.write(':TRIG:VIDeo:POL NEGATIVE')
    dso.opc()
    
# Get x pts only. 
def __read_block2(num):
    num *= 2             # x pts => 2*x bytes
    info = dso.s.recv(1)
    if (info == b'#'):
        head = dso.s.recv(1)
        head_d = int(head.decode('utf-8'))
        cnt = 0
        buf = b''
        while True:
            buf += dso.s.recv(1)
            cnt = len(buf)
            #print("#part:%d/%d"%(cnt,head_d))
            if(cnt == head_d):
                length = buf.decode('utf-8')
                break
        length = int(length) + 1
        cnt = 0
        buf = bytearray()
        while (1):
            buffer=dso.s.recv(8192)
            if(cnt < num):
                buf.extend(buffer)
            cnt += len(buffer)
            #print("data:%d/%d"%(cnt,length))
            if (cnt == length):
                break
    else:
        buf = None
    del buffer
    gc.collect()
    return buf[0:num]

def __read_block_waveform2(num):
    buf = __read_block2(num)
    data_out_size = int(len(buf) / 2)
    data_out=list(struct.unpack(f'>{data_out_size}h', buf))
    del buf
    gc.collect()
    return data_out

def get_acqdata2(ch, num):
    dso.write(':ACQ%d:MEM?'% ch) # Send command to get waveform data.
    
    header_buffer = b''
    while True:
        info_b = dso.s.recv(1)
        header_buffer += info_b
        if (info_b == b'\n'):
            data_out = __read_block_waveform2(num) # read block data waveform
            break
    gc.collect()
    return data_out

def search_ntsc_sync_edge(buf):
    search_offset = 10
    search_max = 2 * search_offset
    v_scale=dso.channel.get_scale(1) # Get channel 1 vertical scale
    v_pos=dso.channel.get_pos(1)     # Get channel 1 vertical position
    trig_level=dso.trigger.level()   # Get trigger level
    trig_level_crossing_ref=128+int((v_pos+trig_level)*25/v_scale)
#    print('trig_ADC', trig_level_ADC_mapping_value)
    index = int(263*LINE_PERIOD/50)-search_offset
    offset = int(200 + 263*LINE_PERIOD/50)
    for i in range(search_max):
        value=buf[index+i]
        if(value < trig_level_crossing_ref): # Check for the edge crossing 
            print('Sync edge found: ', i)
            return (offset - search_offset + i - 1)
    print('Sync edge not found!')
    return offset

if __name__ == '__main__':
    start_time = time.time()
    color_table = []
    import dso_gui
    import gds_info as gds

    dso = gds.Dso()
    dso.connect()
    instrument_init()
    
    gui = dso_gui.DrawObject()
    gui.clear()
    lv_gen_color_table()
    data=[]
    for j in range(30):
        if(dso.acquire.get_state(1)): # Waiting for data acquisition
            print('Data acquired!')
            data=get_acqdata2(1, 650000) # Get 650k pts (maybe a little more)
            print('Num: ', len(data))
            break
        else:
            time.sleep(0.05)
    if(j >= 29):
        print('Data not ready, please check signal!')
        sys.exit()

    dest_index = 0
    for i in range(240): # Used to process data from the odd field
        index = int(200 + (i*LINE_PERIOD)/50) # Index for the data of next line
#        print('%d, index: %d'%(i, index))
        for j in range(500):
            data[dest_index] = data[index + 2*j] # Reassemble image data stream
            dest_index += 1
    
    offset = search_ntsc_sync_edge(data) # Searching for synch edge(line 23 of even field)
    for i in range(240): # Used to process data from the even field
        index = int(offset + (i*LINE_PERIOD)/50) # Index for the data of next line
        for j in range(500):
            data[dest_index] = data[index + 2*j] # Reassemble image data stream
            dest_index += 1
    del data[dest_index : ]
    print('Pixel num:', len(data))

    val_min=min(data)
    val_max=max(data)
    print('min, max', val_min, val_max)
    # Show the image on screen(500 * 480 pixels)
    offset=240*500
    for y in range(240):
        index1 = y*500
        index2 = index1 + offset
        y2 = 2*y
        for x in range(500):
            value=data[index1+x]-val_min
            if(value > 255):
                value = 255
            gui.canvas.set_px(x, y2, color_table[value])
            value=data[index2+x]-val_min
            if(value > 255):
                value = 255
            gui.canvas.set_px(x, y2+1, color_table[value])

    print('%.2f s'%(time.time()-start_time))
    del data
    gc.collect()
    time.sleep(1)
