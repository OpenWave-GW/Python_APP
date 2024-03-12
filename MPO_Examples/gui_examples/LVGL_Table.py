
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
    #              Table              #
    ###################################

    # Set the background color
    obj = lv.scr_act()
    scr_style = lv.style_t()
    scr_style.init()
    obj.add_style(scr_style, 0)
    scr_style.set_bg_color(lv.color_hex(0x000000))

    # Create the table
    table = lv.table(lv.scr_act())
    table.set_col_cnt(3)
    table.set_row_cnt(4)
    table.set_size(480,230)
    table.align(lv.ALIGN.CENTER, 0, 0)
 
    # Set column widths
    table.set_col_width(0,120)
    table.set_col_width(1,120)
    table.set_col_width(2,120)

    # Set cell values
    table.set_cell_value(0, 0, "Product")
    table.set_cell_value(1, 0, "Quantity")
    table.set_cell_value(2, 0, "Price")
    table.set_cell_value(3, 0, "Total")

    table.set_cell_value(0, 1, "Apple")
    table.set_cell_value(1, 1, "30")
    table.set_cell_value(2, 1, "10")
    table.set_cell_value(3, 1, "300")
    
    table.set_cell_value(0, 2, "Banana")
    table.set_cell_value(1, 2, "15")
    table.set_cell_value(2, 2, "5")
    table.set_cell_value(3, 2, "75")
    
    table.set_cell_value(0, 3, "Orange")
    table.set_cell_value(1, 3, "20")
    table.set_cell_value(2, 3, "3")
    table.set_cell_value(3, 3, "60")
    
    # Apply style to the table
    style = lv.style_t()
    style.init()
    style.set_border_side(lv.BORDER_SIDE.LEFT | lv.BORDER_SIDE.RIGHT |
                          lv.BORDER_SIDE.TOP | lv.BORDER_SIDE.BOTTOM)
    style.set_border_color(lv.color_hex(0x000000))
    style.set_bg_color(lv.color_hex(0xFFFFFF))
    table.add_style(style, lv.STATE.DEFAULT | lv.PART.ITEMS)

