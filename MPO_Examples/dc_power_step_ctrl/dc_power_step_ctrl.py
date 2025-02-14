# File Name: dc_power_step_ctrl.py
#
# Description:
# This Python script can be executed directly on the MPO-2000 oscilloscope. This
# script controls the MPO-2000's built-in DC power supply to automatically set 
# and switch through 10 sets of 'voltage and time duration' configurations. It 
# uses LVGL's `lv_timer` software timer for scheduled switching, so the execution
# time accuracy is limited. It is recommended that the execution time interval 
# for each step be set with 0.5 seconds as the minimum unit. Users can operate 
# the Run/Stop function using a USB mouse or Soft Key 'B7'.
#
# Author: Kevin Meng
# Date: Dec.18.2024
# License: GW Python APP License
# Copyright (c) 2024 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt
import lvgl as lv
import fb
import time, sys, os
import gc
import dso_colors as color
import dso_evdev as evdev

WINDOWWIDTH  = 800
WINDOWHEIGHT = 480
BOX_WIDTH = 64
BOX_HEIGHT = 32
STEP_CNT_MAX = 10

# Timer period offset use for command processing time adjust.
PWR_1ST_OFF2ON_DELAY_CNT =  141  # PWR first off to on delay offset
PWR_OFF2ON_DELAY_CNT     =  150  # PWR off to on delay offset
PWR_OFF_DELAY_CNT        = -170  # PWR on to off delay offset

VOLTAGE = 0
DURATION = 1
PERIOD = 2

# Voltage: 1.0 ~ 20.0V, time duration: 0.5 sec ~ 86400 sec
settings = [ # Voltage, time duration(for display), timer period(in ms)
    [ 1.0, 0.5,  500],
    [ 2.0, 1.5, 1500],
    [ 3.0, 2.0, 2000],
    [ 4.0, 2.5, 2500],
    [ 0.0, 0.5,  500],
    [ 6.0, 2.5, 2500],
    [ 7.0, 2.0, 2000],
    [ 8.0, 1.5, 1500],
    [ 9.0, 1.0, 1000],
    [10.0, 0.5,  500]]

DC_PWR_CH = 1  # Channel 1. Define channel number of MPO's DC power supply.
MAX_CYCLE_CNT = 1 # 1 for one cycle, 2 for two cycles, ...,  -1 for infinite cycles

# Load voltage and time duration table from file.
def loadfile(sour, values):
    try:
        with open(sour,'r') as f:
            i=0
            for line in f:
                if line[0] != '#' and len(line.split()) != 0:
                    items = line.split(',')
                    values[i][VOLTAGE] = float(items[0].strip())
                    values[i][DURATION] = float(items[1].strip())
                    values[i][PERIOD] = int(values[i][DURATION]*1000)
                    i += 1
    except:
        pass

def set_voltage_and_update_message():
    global current_index, old_index, v0_flag
    volt = float(settings[current_index][VOLTAGE])
    t_duration = settings[current_index][DURATION]
    period = settings[current_index][PERIOD]
    if(volt < 1): # If the current setting is 0V
        period += PWR_OFF_DELAY_CNT
        dso.power.set_off(DC_PWR_CH)
        dso.gonogo.output_on()  # Set gonogo IO to output low.(debugging)
        dso.gonogo.output_off() # Set gonogo IO to output high.(debugging)
        v0_flag = True
    else:
        dso.power.set_voltage(DC_PWR_CH, volt)
        dso.gonogo.output_on()  # Set gonogo IO to output low.(debugging)
        dso.gonogo.output_off() # Set gonogo IO to output high.(debugging)
        if(v0_flag): # If the last step is 0V and current setting is not 0V.
            period += PWR_OFF2ON_DELAY_CNT
            dso.power.set_on(DC_PWR_CH)
        # else:   Both last and next steps are not 0V.
        v0_flag = False
    timer1.set_period(period)
    #timer1.reset()
    timer1.resume()
    print('  %.2f s'%(time.time()-start_time))
    print('  step %d period:%d'%(current_index+1, period))

    # change current box's bg color
    style_box[current_index].set_bg_color(color.LTMAGENTA)
    label_box[current_index].set_text('%.1f V\n%.1f s'%(volt, t_duration))
    # reset previous box's bg color
    volt = float(settings[old_index][VOLTAGE])
    t_duration = settings[old_index][DURATION]
    style_box[old_index].set_bg_color(color.LTGRAY)
    label_box[old_index].set_text('%.1f V\n%.1f s'%(volt, t_duration))

# lv timer handler
def setup_next_step_cb(timer):
    global current_index, old_index, running, cycle_cnt, v0_flag
    old_index = current_index
    current_index += 1
    if(current_index >= STEP_CNT_MAX):
        cycle_cnt += 1
        if(cycle_cnt == MAX_CYCLE_CNT): # Final cycle.
            dso.power.set_off(DC_PWR_CH)
            dso.gonogo.output_on() # Set gonogo IO to output low.(debugging)
            timer1.pause()
            print('  %.2f s'%(time.time()-start_time))
            print('power off')
            if(MAX_CYCLE_CNT == 1):
                run_stop_label.set_text("Run")
            else:
                run_stop_label.set_text("%d\nRun"%cycle_cnt)
            running = False
            # change final box's bg color
            volt = float(settings[old_index][VOLTAGE])
            t_duration = settings[old_index][DURATION]
            style_box[old_index].set_bg_color(color.LTGRAY)
            label_box[old_index].set_text('%.1f V\n%.1f s'%(volt, t_duration))
            current_index = 0
            old_index = 0
            cycle_cnt = 0
            time.sleep(0.5)
            dso.stop()
        else:
            if(cycle_cnt > 65536):
                cycle_cnt = 65536
            current_index = 0
            if(MAX_CYCLE_CNT == 1):
                run_stop_label.set_text("Stop")
            else:
                run_stop_label.set_text("%d\nStop"%cycle_cnt)
            set_voltage_and_update_message()
    else:
        set_voltage_and_update_message()

def init():
    global kb_dev, timer1, running, current_index, old_index
    global v_t_label, style_box, label_box, run_stop_label
    global v0_flag, cycle_cnt

    lv.init()
    fb.init()  # Frame buffer initialization.

    running = False
    current_index = 0
    old_index = 0
    cycle_cnt = 0
    v0_flag = False  # If 0V is set(initial state is also 0V) => let v0_flag = True
    
    loadfile('dc_power_step_ctrl.txt', settings) # Load configuration file.

    # Allocate buffer for LVGL.
    disp_buf = lv.disp_draw_buf_t()
    buf1 = bytearray(WINDOWWIDTH*WINDOWHEIGHT*3)
    disp_buf.init(buf1, None, len(buf1)//4)

    # Initialize display driver
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf
    disp_drv.flush_cb = fb.flush
    disp_drv.hor_res = WINDOWWIDTH
    disp_drv.ver_res = WINDOWHEIGHT
    disp_drv.register()

    # Create a style for the screen
    style = lv.style_t()
    style.init()
    lv.scr_act().add_style(style, 0)
    style.set_bg_color(color.TRANSPARENT) # Set background to transparent.

    # Initialize mouse driver
    indev_mouse = lv.indev_drv_t()
    indev_mouse.init()
    indev_mouse.type = lv.INDEV_TYPE.POINTER
    indev_mouse.read_cb = evdev.mouse_indev().mouse_read
    mouse = indev_mouse.register()

    # Connect dso control panel
    kb_dev = evdev.dev_kb_indev(dso)
    
    # Initialize mouse cursor
    img = lv.img(lv.scr_act())
    img.set_src(lv.SYMBOL.PLAY)
    mouse.set_cursor(img)
    
    # Create labes for text info
    v_t_label = lv.label(lv.scr_act())
    v_t_label.set_text('V:\n t:')
    v_t_label.align(lv.ALIGN.BOTTOM_LEFT, 5, -3)
    style = lv.style_t()
    style.set_bg_color(color.LTGRAY)
    style.set_bg_opa(lv.OPA.COVER)
    v_t_label.add_style(style, lv.PART.MAIN)
    
    # Create 10 setup boxes(text label)
    style_box = []
    label_box = []
    for i in range(STEP_CNT_MAX):
        style =lv.style_t()
        style_box.append(style)
        style_box[i].init()
        style_box[i].set_bg_color(color.LTGRAY)
        style_box[i].set_bg_opa(lv.OPA.COVER)
        style_box[i].set_height(BOX_HEIGHT)
        style_box[i].set_width(BOX_WIDTH)
        
        volt = float(settings[i][VOLTAGE])
        t_duration = float(settings[i][DURATION])
        box = lv.label(lv.scr_act())
        label_box.append(box)
        label_box[i].set_text('%.1f V\n%.1f s'%(volt, t_duration))
        label_box[i].set_pos((BOX_WIDTH+5)*i+ 25, 445)
        label_box[i].add_style(style_box[i], lv.PART.MAIN)
        
    # Create an lv_timer for step time duration counting.
    period = int(settings[0][PERIOD]+PWR_1ST_OFF2ON_DELAY_CNT)
    timer1 = lv.timer_create(setup_next_step_cb, period, None)
    timer1.set_repeat_count(-1)
    timer1.reset()
    timer1.pause()
    
    # Run/Stop button
    run_stop_btn = lv.btn(lv.scr_act())
    run_stop_btn.set_size(80, 32)
    run_stop_btn.align(lv.ALIGN.BOTTOM_RIGHT, -5, -2)
    run_stop_label = lv.label(run_stop_btn)
    run_stop_label.set_text("Run")
    run_stop_label.align(lv.ALIGN.CENTER, 0, 0)
    run_stop_btn.add_event_cb(toggle_run_cb, lv.EVENT.CLICKED, None)

def instrument_init():
    dso.channel.set_probe_ratio(1, 1) # Set probe rate to x1
    dso.channel.set_scale(1, 2)       # Set CH1 2V/div
    dso.channel.set_pos(1, -4)        # Set CH1 position at -4V
    dso.timebase.set_timebase(2)      # Timebase: 2 s/div
    dso.trigger.set_mode('AUTO')      # Set auto trigger
    dso.opc()
    dso.run()
    dso.gonogo.output_on()            # Set gonogo IO to output low.(debugging)

# Run/Stop button's callback function
def toggle_run_cb(event):
    global running, current_index, old_index
    global v0_flag, cycle_cnt, start_time
    if running: # RUN to STOP
        timer1.pause()
        dso.power.set_off(DC_PWR_CH)
        dso.gonogo.output_on() # Set gonogo IO to output low.(debugging)
        running = False
        v0_flag = True
        print('stop')
        if(MAX_CYCLE_CNT == 1):
            run_stop_label.set_text("Run")
        else:
            run_stop_label.set_text("%d\nRun"%cycle_cnt)
    else:       # STOP to RUN
        dso.run()
        if(old_index != 0): # If the previous steps are interrupted.
            time.sleep(0.5)
            volt = float(settings[current_index][VOLTAGE])
            t_duration = settings[current_index][DURATION]
            style_box[current_index].set_bg_color(color.LTGRAY)
            label_box[current_index].set_text('%.1f V\n%.1f s'%(volt, t_duration))
        current_index = 0
        old_index = 0
        cycle_cnt = 0
        running = True
        print('PWR #%d'%DC_PWR_CH)
        volt = float(settings[current_index][VOLTAGE])
        t_duration = settings[current_index][DURATION]
        dso.power.set_voltage(DC_PWR_CH, volt)
        dso.power.set_on(DC_PWR_CH)
        period = settings[current_index][PERIOD]+PWR_1ST_OFF2ON_DELAY_CNT
        timer1.set_period(period)
        timer1.reset()
        timer1.resume()
        dso.gonogo.output_off() # Set gonogo IO to output high.(debugging)
        start_time = time.time()
        print('start_time', start_time)
        print('  step 1 period:', period)
        v0_flag = False
        run_stop_label.set_text("%d\nStop"%cycle_cnt)
        style_box[current_index].set_bg_color(color.LTMAGENTA)
        label_box[current_index].set_text('%.1f V\n%.1f s'%(volt, t_duration))

if __name__ == '__main__':
    os.chdir(sys.path[0])
    if not sys.implementation.name == "micropython":
       raise ValueError('This Demo can only be used on DSO')
    from dso_const import *

    try:
        import gds_info as gds
    except ImportError:
        import dso2kp as gds

    dso = gds.Dso()
    dso.connect()
    init()
    instrument_init()

    while(1):
        key,cnt = kb_dev.kb_read()
        if(key[1] == 'KEY_B7'):
            toggle_run_cb(0)
        time.sleep(0.3)
