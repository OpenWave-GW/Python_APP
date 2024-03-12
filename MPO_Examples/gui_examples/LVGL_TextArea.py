
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
    #            Text Area            #
    ###################################

    LV_HOR_RES = 780
    LV_VER_RES = 450
    
    # Create the text area
    ta = lv.textarea(lv.scr_act())
    ta.set_text("A text in a Text Area")
    ta.set_one_line(False)
    ta.align(lv.ALIGN.OUT_TOP_LEFT, 5, 20)
    ta.set_size(LV_HOR_RES, LV_VER_RES // 2)
    ta.add_state(lv.STATE.FOCUSED)   # To be sure the cursor is visible
    ta.set_max_length(10000)  # The maximum number of characters

    # Create a label above the text box 
    label = lv.label(lv.scr_act())
    label.set_text("Text Area")
    label.align(lv.ALIGN.OUT_TOP_LEFT, 5, 0)

    # Create a keyboard 
    kb = lv.keyboard(lv.scr_act())
    kb.set_size(LV_HOR_RES, LV_VER_RES // 2)
    kb.align(lv.ALIGN.OUT_TOP_LEFT, 5, LV_VER_RES // 2 + 20)
    kb.set_textarea(ta)


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
    #        Keyboard Device          #
    ###################################
    
    # Registering a keyboard input device
    import dso_evdev
    indev_kb = lv.indev_drv_t()
    indev_kb.init()
    indev_kb.type = lv.INDEV_TYPE.KEYPAD
    kb_dev = dso_evdev.kb_indev()
    indev_kb.read_cb = kb_dev.kb_read
    indev_kb.register()


    ###################################
    #      Keyboard Input Handle      #
    ###################################

    # Read keyboard input and display corresponding text or perform corresponding operations in the textarea
    while True:
        key = kb_dev.get_keycode_mods()
        if key["keycode"]:
            keychar = kb_dev.key_to_char(key['shift'],key['keycode'])
            keyname = kb_dev.get_key_name(key["keycode"])
            if keychar is None:
                if keyname == 'KEY_BACKSPACE':
                    lv.textarea.del_char(ta)
                elif keyname == 'KEY_DELETE':
                    lv.textarea.del_char_forward(ta)
                elif keyname == 'KEY_UP':
                    lv.textarea.cursor_up(ta)
                elif keyname == 'KEY_LEFT':
                    lv.textarea.cursor_left(ta)
                elif keyname == 'KEY_RIGHT':
                    lv.textarea.cursor_right(ta)
                elif keyname == 'KEY_DOWN':
                    lv.textarea.cursor_down(ta)
            else:
                lv.textarea.add_text(ta, keychar)

