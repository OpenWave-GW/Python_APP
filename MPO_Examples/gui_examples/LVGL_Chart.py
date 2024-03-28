
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
    #           Draw a Chart          #
    ###################################
    
    # Create a chart
    chart = lv.chart(lv.scr_act())
    chart.set_size(400,300)
    chart.align(lv.ALIGN.CENTER,0,0)
    chart.set_type(lv.chart.TYPE.LINE)
    
    # Add data series
    ser=chart.add_series(lv.color_hex(0xFF0000), lv.chart.AXIS.PRIMARY_Y)

    # Set the number of points, default is 10
    chart.set_point_count(3)

    # Set points on ser
    ser.y_points = [25, 75, 50]

    # Update the chart
    chart.refresh()

    time.sleep(0.5)