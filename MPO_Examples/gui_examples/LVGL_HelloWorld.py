
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

    # Create the display buffer
    disp_buf = lv.disp_draw_buf_t()
    
    # Set the size of the display buffer
    buf = bytes(screen_width*screen_height*3)
    
    # Initialize the display buffer in 32-bit units
    disp_buf.init(buf, None, len(buf)//4)
    
    # Register FB display driver
    disp_drv = lv.disp_drv_t()
    disp_drv.init()
    disp_drv.draw_buf = disp_buf
    disp_drv.flush_cb = fb.flush
    disp_drv.hor_res = screen_width
    disp_drv.ver_res = screen_height
    disp_drv.register()
    
    
    ####################################
    #           Hello World            #
    ####################################

    # Create a label object
    label = lv.label(lv.scr_act())
    
    # Set the font style of the label to font_montserrat with a size of 48 pixels
    label.set_style_text_font(lv.font_montserrat_48, 0)
    
    # Align the label to the center of the screen
    label.align(lv.ALIGN.CENTER, 0, 0)
    
    # Set the text of the label
    label.set_text('Hello World')




