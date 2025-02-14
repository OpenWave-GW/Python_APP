# File Name: gw_calculator.py
#
# Description:
# This Python script can be executed directly on the MPO-2000 oscilloscope. This
# is a simple calculator implemented in Python. Please use a mouse to operate 
# it. Users can build upon this script to extend its functionality with more 
# complex calculations.
#
# Author: Kevin Meng
# Date: Dec.02.2024
# License: GW Python APP License
# Copyright (c) 2024 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import lvgl as lv
import fb
import math
#import dso_evdev as evdev
import evdev
import time

SCR_WIDTH = 400
SCR_HEIGHT = 400

# Buttons mapping
btnm_map = [
    "7", "8", "9", "/", "\n",
    "4", "5", "6", "*", "\n",
    "1", "2", "3", "-", "\n",
    "0", ".", "C", "+", "\n",
    "sin", "cos", "tan", "=", ""
]

def textarea_event_handler(e, ta):
    print("Text: " + ta.get_text())

# Call back handler for buttons
def btnm_event_handler(evt, ta):
    obj = evt.get_target()
    txt = obj.get_btn_text(obj.get_selected_btn())
    if txt == '=':
        result = evaluateExpression(ta.get_text())
        ta.set_text(result)
        print('result=', result)
    elif txt == "C":
        ta.set_text('')
    else:
        ta.add_text(txt)

# Evaluate expression.
def evaluateExpression(expression):
    try:
        if "sin" in expression:
            return str(math.sin(math.radians(float(expression.replace("sin", "")))))
        elif "cos" in expression:
            return str(math.cos(math.radians(float(expression.replace("cos", "")))))
        elif "tan" in expression:
            return str(math.tan(math.radians(float(expression.replace("tan", "")))))
        else:
            print('expression:', expression)
            return str(eval(expression))
    except Exception as e:
        return "Error"

def init():
    lv.init()
    fb.init()  # Frame buffer initialization.

    # Allocate buffer for LVGL.
    disp_buf1 = lv.disp_draw_buf_t()
    buf1_1 = bytearray(SCR_WIDTH*SCR_HEIGHT*3)
    disp_buf1.init(buf1_1, None, len(buf1_1)//4)
    # Initialize display driver
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf1
    disp_drv.flush_cb = fb.flush
    disp_drv.hor_res = SCR_WIDTH
    disp_drv.ver_res = SCR_HEIGHT
    disp_drv.register()
    # Initialize mouse driver
    indev_drv = lv.indev_drv_t()
    indev_drv.init()
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = evdev.mouse_indev().mouse_read # Kevin Meng 2024.11.12
    mouse_indev = indev_drv.register()
    # Init mouse cursor
    img = lv.img(lv.scr_act())
#    img.set_src(lv.SYMBOL.ARROW_POINTER)
    img.set_src(lv.SYMBOL.PLAY)
    mouse_indev.set_cursor(img)

    # Create text area for expression.
    ta = lv.textarea(lv.scr_act())
    ta.set_one_line(True)
    ta.align(lv.ALIGN.TOP_MID, 0, 10)
    ta.set_width(300)
    ta.set_style_text_font(lv.font_montserrat_24, 0)
    ta.add_event_cb(lambda e:textarea_event_handler(e,ta),lv.EVENT.READY, None)
    ta.add_state(lv.STATE.FOCUSED) # To be sure the cursor is visible

    # Create button matrix.
    btnm = lv.btnmatrix(lv.scr_act())
    btnm.set_size(300, 300)
    btnm.align(lv.ALIGN.CENTER, 0, 15)
    btnm.set_style_text_font(lv.font_montserrat_24, 0)
    btnm.add_event_cb(lambda e:btnm_event_handler(e,ta), lv.EVENT.VALUE_CHANGED, None)
    btnm.clear_flag(lv.obj.FLAG.CLICK_FOCUSABLE) #To keep the text area focused on button clicks
    btnm.set_map(btnm_map)

if __name__ == "__main__":
    init()
    while(1):
        time.sleep(0.1)  # Kevin Meng 2024.11.12
    