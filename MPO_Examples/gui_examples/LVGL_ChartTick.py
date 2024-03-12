
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
    #        Create a Chart           #
    ###################################
    
    # create a chart and set points
    chart = lv.chart(lv.scr_act())
    chart.set_size(400,300)
    chart.align(lv.ALIGN.CENTER,0,0)
    chart.set_type(lv.chart.TYPE.LINE)
    ser=chart.add_series(lv.color_hex(0xFF0000), lv.chart.AXIS.PRIMARY_Y)
    ser.y_points = [30, 44, 26, 78, 24, 75, 22, 34, 13, 75]

    ###################################
    #     Set the ticks and texts     #
    ###################################

    chart.set_axis_tick(
        lv.chart.AXIS.PRIMARY_X,  #Choose to set the x or y-axis
        10,  # Set the length of the major tick
        5,  # Set the length of the minor tick
        10,  # Set the total number of major ticks on the x-axis
        2,  # Set the number of intervals between major tick on the x-axis
        True, # Set whether to display tick labels
        50  # Set the length of the tick label
    )
    
    chart.set_axis_tick(
        lv.chart.AXIS.PRIMARY_Y,  #Choose to set the x or y-axis
        10,  # Set the length of the major tick
        5,  # Set the length of the minor tick
        5,  # Set the total number of major ticks on the y-axis
        5,  # Set the number of intervals between major tick on the y-axis
        True, # Set whether to display tick labels
        50  # Set the length of the tick label
    )
    
    # Update the chart
    chart.refresh()
    
    
    ###################################
    #           Chart title           #
    ###################################

    # Create a label object
    label = lv.label(lv.scr_act())

    # Set the position of the label
    label.set_pos(360, 60)

    # Set the text of the label
    label.set_text('Chart Title')
