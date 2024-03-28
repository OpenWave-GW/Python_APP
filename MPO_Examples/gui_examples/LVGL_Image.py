
import lvgl as lv
import fb
import os
import sys
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
    #          Display image          #
    ###################################

    # Set the background color
    obj = lv.scr_act()
    style = lv.style_t()
    style.init()
    obj.add_style(style, 0)
    style.set_bg_color(lv.color_hex(0x000000))

    # Set the current working directory to the directory where the script is located
    os.chdir(sys.path[0])

    # Read the image file and display it on the screen
    with open('LVGL_Image.png','rb') as f:
      # Read the PNG data from the file
      png_data = f.read()

    # Create an image descriptor
    png_img_dsc = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data 
    })

    # Create an image object and set the image
    img = lv.img(lv.scr_act())
    img.align(lv.ALIGN.CENTER, 0, 0)
    img.set_src(png_img_dsc)
    
    
    # Process LVGL tasks
    #while True:
    #    lv.task_handler()
    time.sleep(0.5)


    
    

