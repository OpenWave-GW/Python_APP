
import lvgl as lv
import fb
import time

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
    #          Create a Bar           #
    ###################################

    def event_handler(evt):         
        event_type = evt.get_code()
        target = evt.get_target()

        if event_type == lv.EVENT.VALUE_CHANGED:
            value = target.get_value()
            label_slider.set_text(str(value))

    # Create a bar
    bar = lv.bar(lv.scr_act())
    bar.set_size(200, 20)
    bar.align(lv.ALIGN.CENTER, 0, 50)
    bar.set_range(0, 100)
    bar.set_value(0, lv.ANIM.OFF)
    bar.set_start_value(0, lv.ANIM.OFF)    
    label_bar = lv.label(lv.scr_act())
    label_bar.set_text(str(bar.get_value()))
    label_bar.align(lv.ALIGN.CENTER, bar.get_x_aligned(), bar.get_y_aligned())
    
    # Create a slider
    slider = lv.slider(lv.scr_act())
    slider.add_event_cb(event_handler, lv.EVENT.VALUE_CHANGED, None)
    slider.set_width(200)
    slider.set_range(0, 100)
    slider.set_value(50, lv.ANIM.OFF)
    slider.align(lv.ALIGN.CENTER,0, -50)
    label_slider = lv.label(lv.scr_act())
    label_slider.set_text(str(slider.get_value()))
    label_slider.align(lv.ALIGN.CENTER, slider.get_x_aligned(), slider.get_y_aligned())


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


    ###################################
    #          Progress Bar           #
    ###################################
    
    def progress_bar():
        if bar.get_mode() == lv.bar.MODE.NORMAL:
            for value in range(0, 101):
                bar.set_value(value, lv.ANIM.OFF)
                label_bar.set_text(str(bar.get_value()))
                time.sleep(0.02)
        else:
            for value in range(0, 121):
                bar.set_start_value(value-20, lv.ANIM.ON)
                bar.set_value(value, lv.ANIM.ON)
                label_bar.set_text("")
                time.sleep(0.02)
        time.sleep(1)
    
    while True:        
        bar.set_mode(lv.bar.MODE.NORMAL)
        progress_bar()
        bar.set_mode(lv.bar.MODE.RANGE)
        progress_bar()

