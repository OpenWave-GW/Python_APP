
import lvgl as lv
import fb

if __name__ == '__main__':

    ###################################
    #       GUI Initialization        #
    ###################################
    
    # Initialize LVGL and Framebuffer
    lv.init()
    fb.init()

    # Set screen width and height
    screen_width = 800
    screen_height = 480

    # Initialize display buffer
    disp_buf = lv.disp_draw_buf_t()
    buf = bytes(screen_width*screen_height*3)
    disp_buf.init(buf, None, len(buf)//4)
    
    # Register FB display driver
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf
    disp_drv.flush_cb = fb.flush
    disp_drv.hor_res = screen_width
    disp_drv.ver_res = screen_height
    disp_drv.register()


    ###################################
    #        Create a Button          #
    ###################################

    def event_handler(evt):         
        event_type = evt.get_code()
        target = evt.get_target()
        list_onoff = {True: "On", False: "Off"}

        if event_type == lv.EVENT.CLICKED:
            btn_toggle.clear_state(lv.STATE.CHECKED)
            label_btn_toggle.set_text(list_onoff[btn_toggle.has_state(lv.STATE.CHECKED)])
            sw.clear_state(lv.STATE.CHECKED)
            label_sw.set_text(list_onoff[sw.has_state(lv.STATE.CHECKED)])
        elif event_type == lv.EVENT.VALUE_CHANGED:
            if type(target) == type(btn_toggle):
                state = target.has_state(lv.STATE.CHECKED)                
                label_btn_toggle.set_text(list_onoff[state])
            elif type(target) == type(sw):
                state = target.has_state(lv.STATE.CHECKED)
                label_sw.set_text(list_onoff[state])

    # Create a simple button
    btn_simple = lv.btn(lv.scr_act())
    btn_simple.add_event_cb(event_handler, lv.EVENT.CLICKED, None)
    btn_simple.set_height(40)
    btn_simple.set_width(80)
    btn_simple.align(lv.ALIGN.CENTER, 0,-100)
    label_btn_simple = lv.label(btn_simple)
    label_btn_simple.center()
    label_btn_simple.set_text("Default")
    
    # Create a toggle button
    btn_toggle = lv.btn(lv.scr_act())
    btn_toggle.add_event_cb(event_handler, lv.EVENT.VALUE_CHANGED, None)
    btn_toggle.add_flag(lv.obj.FLAG.CHECKABLE)
    btn_toggle.set_height(40)
    btn_toggle.set_width(80)
    btn_toggle.align(lv.ALIGN.CENTER, 0, 100)
    label_btn_toggle = lv.label(btn_toggle)
    label_btn_toggle.center()
    label_btn_toggle.set_text("Off")

    # Create a switch
    sw = lv.switch(lv.scr_act())
    sw.add_event_cb(event_handler, lv.EVENT.VALUE_CHANGED, None)
    sw.center()
    label_sw=lv.label(sw)
    label_sw.center()
    label_sw.set_text("Off")


    ###################################
    #          Mouse Device           #
    ###################################
    
    # Registering a mouse input device
    import evdev
    indev_mouse = lv.indev_drv_t()
    indev_mouse.init()    
    indev_mouse.type = lv.INDEV_TYPE.POINTER
    indev_mouse.read_cb = evdev.mouse_indev().mouse_read
    indev_mouse.register()

    while True:
        #lv.tick_inc(100)
        pass
