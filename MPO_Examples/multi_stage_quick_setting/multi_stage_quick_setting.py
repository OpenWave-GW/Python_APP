# File Name: multi_stage_quick_setting.py
#
# Description:
# This Python script can be executed directly on the MPO-2000 oscilloscope. It
# features 10 customizable functions (expandable), allowing users to input 
# specific oscilloscope configuration scripts for different measurement purposes
# into each function. The program structure and GUI framework are pre-built, 
# enabling users to execute single configurations sequentially and quickly.
# This is particularly beneficial for complex and long-duration oscilloscope 
# operations, significantly improving efficiency. Additionally, by selecting the 
# 'AutoRun' button, the script will automatically execute configurations starting 
# from the first set. After completing each configuration, it will delay for a 
# user-defined period to allow observation of the captured waveform on the 
# oscilloscope before proceeding to the next set. This process repeats sequentially
# for all 10 configurations and can be set to run in a continuous loop. Users can
# use this script as a foundation to further expand it into a more versatile 
# testing tool.
#
# Author: Kevin Meng
# Date: Dec.27.2024
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
BOX_WIDTH  = 70
BOX_HEIGHT = 32

DESCRIPTION = 0
FUNCTION    = 1
DELAY_TIME  = 2

# Insert your custom code into the designated user functions below.
def func1():
    dso.channel.set_on(1)  # Set CH1 on.
    dso.channel.set_off(2)
    dso.channel.set_off(3)
    dso.channel.set_off(4)
    dso.trigger.set_source('CH1')
    dso.opc() # A sync command to ensure previous instructions are all executed.
    dso.single()
    print('func1() settings applied')

def func2():
    dso.channel.set_off(1)
    dso.channel.set_on(2)
    dso.channel.set_off(3)
    dso.channel.set_off(4)
    dso.trigger.set_source('CH2')
    dso.opc() # A sync command to ensure previous instructions are all executed.
    dso.single()
    print('func2() settings applied')

def func3():
    dso.channel.set_off(1)
    dso.channel.set_off(2)
    dso.channel.set_on(3)
    dso.channel.set_off(4)
    dso.trigger.set_source('CH3')
    dso.opc() # A sync command to ensure previous instructions are all executed.
    dso.single()
    print('func3() settings applied')

def func4():
    dso.channel.set_off(1)
    dso.channel.set_off(2)
    dso.channel.set_off(3)
    dso.channel.set_on(4)
    dso.trigger.set_source('CH4')
    dso.opc() # A sync command to ensure previous instructions are all executed.
    dso.single()
    print('func4() settings applied')

def func5():
    dso.channel.set_on(3)
    dso.channel.set_on(2)
    dso.channel.set_on(1)
    dso.opc() # A sync command to ensure previous instructions are all executed.
#    dso.write(':PYCLOSE') # Exit the Python script execution process.
    print('func5() settings applied')

def func6():
    print('func6() settings applied')

def func7():
    print('func7() settings applied')

def func8():
    print('func8() settings applied')

def func9():
    print('func9() settings applied')

def func10():
    print('func10() settings applied')

# Custom function table, delay time and descriptions.
description_and_function_list = [  # description, function name, delay time(in sec)
    [' 1. CH1 ON only, Trig: CH1, Single', func1, 1],
    [' 2. CH2 ON only, Trig: CH2, Single', func2, 1],
    [' 3. CH3 ON only, Trig: CH3, Single', func3, 1],
    [' 4. CH4 ON only, Trig: CH4, Single', func4, 1],
    [' 5. CH1/2/3/4 ON, and then Exit',    func5, 0.5],
    [' 6. Test I',   func6, 0.5],
    [' 7. Test II',  func7, 0.5],
    [' 8. Test III', func8, 0.5],
    [' 9. Test IV',  func9, 0.5],
    ['10. Test V',  func10, 0.5]]

# Callback function for handling mouse interactions with the dropdown.
def dropdown_event_handler(evt):
    global selected_index, dropdown, table_loaded_flag
    code = evt.get_code()
    obj  = evt.get_target()
    
    if type(obj) != type(lv.dropdown()):
        return
    
    if code == lv.EVENT.VALUE_CHANGED:
        selected_index = dropdown.get_selected()
        description_and_function_list[selected_index][FUNCTION]() # Execute custom function
    elif code == lv.EVENT.CLICKED:
        if(not table_loaded_flag):  # if the dropdown is first pressed
            load_dropdown_option_table() # Load table for dropdown
            dropdown.open()

# Callback function for handling mouse interactions with the 'Next' button.
def next_cb(evt):
    global selected_index, auto_run_flag, table_loaded_flag
    if(auto_run_flag): # Disable the 'Next' button after the auto run enabled. 
        return

    if(not table_loaded_flag):  # if 'Next' hard key is first pressed
        load_dropdown_option_table() # Load table for dropdown
        dropdown.set_selected(selected_index)
        description_and_function_list[selected_index][FUNCTION]() # Execute custom function
        return
    
    selected_index = dropdown.get_selected()
    if(dropdown.is_open()):
        dropdown.close()
        description_and_function_list[selected_index][FUNCTION]() # Execute custom function
    else:
        selected_index += 1
        if(selected_index >= dropdown_item_num):
            selected_index = 0
        dropdown.set_selected(selected_index)
        description_and_function_list[selected_index][FUNCTION]() # Execute custom function

# Callback function for handling mouse interactions with the 'AutoRun' button.
def auto_run_cb(evt):
    global selected_index, label_autorun, auto_run_flag
    if(dropdown.is_open()):
        dropdown.close()
    if(auto_run_flag):
        auto_run_flag = False  # Change flag, stop auto run.
        label_autorun.set_text('AutoRun')
    else:              # Auto run start.
        if(not table_loaded_flag):  # if 'AutoRun' hard key is first pressed
            load_dropdown_option_table() # Load function tables to dropdown.
        auto_run_flag = True
        selected_index = 0 # Set index to the first step
        label_autorun.set_text('Stop')

# Callback function for handling mouse interactions with the 'Single' checkbox.
def checkbox_cb(e):
    global selected_index, single_flag
    selected_index = 0      # Set to the first step
    if(dropdown.is_open()):
        dropdown.close()
    obj = e.get_target()
    if obj.has_state(lv.STATE.CHECKED):
        single_flag = True  # Single run
    else:
        single_flag = False # Continuous run

def load_dropdown_option_table():
    global table_loaded_flag
    table_loaded_flag = True
    items = []
    for i in range(dropdown_item_num):
        items.append(description_and_function_list[i][DESCRIPTION])
    dropdown.set_options("\n".join(items))
    dropdown.set_selected(0)

def init():
    global kb_dev, dropdown, label_autorun, checkbox
    global selected_index, dropdown_item_num
    global table_loaded_flag, auto_run_flag, single_flag
    
    auto_run_flag = False
    single_flag = False
    table_loaded_flag = False
    selected_index = 0

    lv.init()
    fb.init()  # Frame buffer initialization.

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
    lv.scr_act().clear_flag(lv.obj.FLAG.SCROLLABLE) # Disable scrollable
    style.set_bg_color(color.TRANSPARENT) # Set background to transparent.

    # Initialize mouse driver
    indev_mouse = lv.indev_drv_t()
    indev_mouse.init()
    indev_mouse.type = lv.INDEV_TYPE.POINTER
    indev_mouse.read_cb = evdev.mouse_indev().mouse_read
    mouse = indev_mouse.register()

    # Initialize mouse cursor
    img = lv.img(lv.scr_act())
    img.set_src(lv.SYMBOL.PLAY)
    mouse.set_cursor(img)

    # Connect dso control panel
    kb_dev = evdev.dev_kb_indev(dso)
    
    # Create a dropdown
    dropdown_style = lv.style_t()
    dropdown_style.init()
    dropdown_style.set_bg_opa(lv.OPA.COVER)
    dropdown_style.set_bg_color(color.LTGRAY)
    dropdown_style.set_text_color(lv.color_black())
    dropdown_style.set_radius(0)
#    dropdown_style.set_text_font(font)
    dropdown = lv.dropdown(lv.scr_act())
    dropdown.set_size(500, BOX_HEIGHT)
    dropdown.set_dir(lv.DIR.BOTTOM)
    dropdown.add_style(dropdown_style, 0)
    dropdown.set_style_bg_color(color.TRANSPARENT_1, lv.PART.ITEMS)  # set option's bg color
    dropdown_item_num = len(description_and_function_list)
    dropdown.set_options_static('-- Please select one --') # Function table is empty here.
    dd_list = dropdown.get_list()
    dd_list.set_style_max_height(400, 0) # Set dropdown max height
    dropdown.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)
    dropdown.add_event_cb(dropdown_event_handler,lv.EVENT.ALL, None)

    # Create container for buttons and checkbox.
    container = lv.obj(lv.scr_act())
    container.set_size(280, BOX_HEIGHT+4)  # Set container's size
    container.set_style_bg_color(color.LTGRAY, lv.PART.MAIN)
    container.align(lv.ALIGN.BOTTOM_RIGHT, -10, 0)
    container.clear_flag(lv.obj.FLAG.SCROLLABLE) # Disable scrollable for the container.

    btn_next = lv.btn(container)  # Create 'Next' button
    btn_next.set_size(BOX_WIDTH, BOX_HEIGHT)
    btn_next.align(lv.ALIGN.BOTTOM_RIGHT, 10, 20)
    label_next = lv.label(btn_next)
    label_next.set_text('Next')
    label_next.align(lv.ALIGN.CENTER, 0, 0)
    btn_next.add_event_cb(next_cb, lv.EVENT.CLICKED, None)

    btn_autorun = lv.btn(container)  # Create 'AutoRun' button
    btn_autorun.set_size(BOX_WIDTH, BOX_HEIGHT)
    btn_autorun.align_to(btn_next, lv.ALIGN.OUT_LEFT_BOTTOM, -25, 0)
    label_autorun = lv.label(btn_autorun)
    label_autorun.set_text('AutoRun')
    label_autorun.align(lv.ALIGN.CENTER, 0, 0)
    btn_autorun.add_event_cb(auto_run_cb, lv.EVENT.CLICKED, None)

    checkbox = lv.checkbox(container) # Create checkbox for 'Single' selection
    checkbox.set_text('Single')
    checkbox.align_to(btn_autorun, lv.ALIGN.OUT_LEFT_BOTTOM, -25, -5)
    checkbox.add_event_cb(checkbox_cb, lv.EVENT.VALUE_CHANGED, None)
    checkbox.add_state(lv.STATE.CHECKED)

#def instrument_init():
#    dso.channel.set_probe_ratio(1, 1) # Set probe rate to x1
#    dso.channel.set_scale(1, 2)       # Set CH1 2V/div
#    dso.channel.set_pos(1, -4)        # Set CH1 position at -4V
#    dso.timebase.set_timebase(2)      # Timebase: 2 s/div
#    dso.trigger.set_mode('AUTO')      # Set auto trigger
#    dso.opc()
#    dso.run()
#    dso.gonogo.output_on()            # Set gonogo IO to output low.(debugging)

if __name__ == '__main__':
#    os.chdir(sys.path[0])
    if not sys.implementation.name == "micropython":
       raise ValueError('This script can only be used on DSO')
    from dso_const import *

    try:
        import gds_info as gds
    except ImportError:
        import dso2kp as gds

    dso = gds.Dso()
    dso.connect()
    init()
#    instrument_init()

    while(1):
        key,cnt = kb_dev.kb_read()
        if(auto_run_flag): # Auto run(single or continuous run)
            if(key[1] == 'KEY_B6'): # if the 'Stop' hard key is pressed.
                auto_run_cb(0)
            else:
                if(selected_index != dropdown.get_selected()):
                    dropdown.set_selected(selected_index)
                description_and_function_list[selected_index][FUNCTION]()  # Execute custom function
                time.sleep(description_and_function_list[selected_index][DELAY_TIME]) # Custom time delay
                selected_index += 1
                if(selected_index >= dropdown_item_num):
                    if(single_flag == True): # if single run
                        selected_index = dropdown_item_num-1  # Stop at the final stage.
                        auto_run_cb(0)
                    else:
                        selected_index = 0   # Reset index to the first stage.
        else:
            if(key[1] == 'KEY_B7'):  # if the 'Next' hard key is pressed.
                next_cb(0)        # Next step
            elif(key[1] == 'KEY_B6'):# if the 'AutoRun' hard key is pressed.
                auto_run_cb(0)    # Auto run Start/Stop
            elif(key[1] == 'KEY_B5'): # if the 'Single' hard key is pressed.
                if checkbox.has_state(lv.STATE.CHECKED):
                    checkbox.clear_state(lv.STATE.CHECKED)
                else:
                    checkbox.add_state(lv.STATE.CHECKED)
                lv.event_send(checkbox, lv.EVENT.VALUE_CHANGED, None)
            elif(key[1] == 'KEY_B1' or key[1] == 'KEY_B2' or key[1] == 'KEY_B3' or key[1] == 'KEY_B4'):
                if(not table_loaded_flag): # if dropdown(B1 hard key) is first pressed
                    load_dropdown_option_table() # Load table for dropdown
                dropdown.open() # Open the dropdown menu.
            elif(key[1] == 'KEY_VARIABLE'): # if the variable knob is rotated.
                if(dropdown.is_open()):
                    selected_index = dropdown.get_selected()
                    selected_index += cnt
                    if(selected_index >= dropdown_item_num):
                        selected_index = dropdown_item_num-1
                    elif(selected_index < 0):
                        selected_index = 0
                    dropdown.set_selected(selected_index)
            elif(key[1] == 'KEY_SELECT'): # if the 'Select' hard key is pressed.
                if(dropdown.is_open()):
                    dropdown.close()
                    description_and_function_list[selected_index][FUNCTION]() # Execute custom function
            time.sleep(0.1)
