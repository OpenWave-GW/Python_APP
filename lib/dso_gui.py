# Name: dso_gui.py
#
# Description: 
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

'''
.. note:: This mudule can only be used on DSO! 
'''
import sys
import time
import gc
try:
    import gds_info as gds
except ImportError:
    import dso2kp as gds
try:
    import lvgl as lv
    import fb
    import fs_driver
except ImportError:
    pass

import dso_colors as color

try:
    font = lv.gds_ttfb_16
except:
    font = lv.font_montserrat_16

class __INIT():
    def __init__(self) -> None:
        self.bg_color = color.TRANSPARENT#color.DKGRAY
        self.canvas_bg_color = self.bg_color#color.TRANSPARENT 
        size = gds.Screen()
        self.screen_width = size.width
        self.screen_height = size.height
        self.canvas_buf = bytearray(3 * size.width * size.height)
        self.canvas = lv.canvas(lv.scr_act())
        self.canvas.set_pos(0, 0)
        self.canvas.set_buffer(self.canvas_buf, self.screen_width, self.screen_height, lv.img.CF.TRUE_COLOR)
        self.canvas.fill_bg(self.canvas_bg_color, lv.OPA.COVER)
        obj = lv.scr_act()
        style = lv.style_t()
        style.init()
        style.set_bg_color(self.bg_color)#TRANS
        style.set_bg_opa(lv.OPA.COVER)
        obj.add_style(style, 0)
        gc.collect()

class __Gui_Init(__INIT):
    def __init__(self) -> None:
        #self.bg_color = color.DKGRAY
        #self.canvas_bg_color = color.DKGRAY
        size = gds.Screen()
        self.width = size.width
        self.height = size.height
        lv.init()
        fb.init()
        # Register FB display driver
        disp_buf1 = lv.disp_draw_buf_t()
        buf1_1 = bytes(self.width*self.height*3)
        disp_buf1.init(buf1_1, None, len(buf1_1)//4)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf1
        disp_drv.flush_cb = fb.flush
        disp_drv.hor_res = self.width
        disp_drv.ver_res = self.height
        disp_drv.offset_x = 0#disp_area_offset[0]
        disp_drv.offset_y = 0#disp_area_offset[1]
        disp_drv.antialiasing = False
        disp_drv.rotated = 0#1: 90 rot
        disp_drv.register()
        super().__init__()

class DrawObject(__Gui_Init):
    instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance
    initial = False
    def __init__(self) -> None:
        if DrawObject.initial is False:
            super().__init__()
            DrawObject.initial = True
            self.obj_popup = None
    def clear(self):
        lv.obj.clean(lv.scr_act())
        self.canvas_bg_color = self.bg_color#color.TRANSPARENT 
        self.canvas = lv.canvas(lv.scr_act())
        self.canvas.set_pos(0, 0)
        self.canvas.set_buffer(self.canvas_buf, self.screen_width, self.screen_height, lv.img.CF.TRUE_COLOR)
        self.canvas.fill_bg(self.canvas_bg_color, lv.OPA.COVER)
        '''
        obj = lv.scr_act()
        style = lv.style_t()
        style.init()
        style.set_bg_color(self.bg_color)#TRANS
        style.set_bg_opa(lv.OPA.COVER)
        obj.add_style(style, 0)
        del style
        '''
    def set_bg_color(self, color):
        self.bg_color = color
        self.canvas.fill_bg(self.bg_color, lv.OPA.COVER)
    def draw_text(self, x, y, str, color=color.WHITE, rol:int=0, font=font):
        style = lv.style_t()
        style.init()
        style.set_bg_opa(lv.OPA.TRANSP)
        style.set_text_color(color)
        style.set_text_font(font)
        #style.set_text_opa(lv.OPA.COVER)
        #style.set_text_decor(False)
        label = lv.label(lv.scr_act())
        label.set_style_transform_angle(int(rol*10), lv.PART.MAIN)
        label.set_pos(int(x), int(y))
        label.add_style(style, 0)
        label.set_style_text_font(font, lv.PART.TICKS)
        label.set_text(str)
        del style
        return label
    def draw_line(self, x1, y1, x2, y2, color=color.WHITE, width=1):
        line_style = lv.style_t()
        line_style.init()
        line_style.set_line_color(color)
        line_style.set_line_width(width)
        line_style.set_line_opa(lv.OPA.COVER)
        line = lv.line(lv.scr_act())
        p = [{"x":x1, "y":y1},{"x":x2, "y":y2}]
        line.set_points(p, len(p))
        line.add_style(line_style, 0)
        del line_style
        return line
    def draw_rect(self, x, y, x_width, y_hight, color=color.WHITE, width=1):
        rect_style = lv.style_t()
        rect_style.init()
        rect_style.set_line_color(color)
        rect_style.set_line_width(width)
        rect_style.set_line_opa(lv.OPA.COVER)
        rect = lv.line(lv.scr_act())
        p = [{"x":int(x), "y":int(y)},{"x":int(x+x_width), "y":int(y)},
            {"x":int(x+x_width), "y":int(y+y_hight)},{"x":int(x), "y":int(y+y_hight)},
            {"x":int(x), "y":int(y)}]
        rect.set_points(p, len(p))
        rect.add_style(rect_style, 0)
        del rect_style
        return rect
    def draw_arc(self, x1, y1, x2, y2, color=color.WHITE, rol=0):
        arc = lv.arc(lv.scr_act())
        arc.set_end_angle(rol)
        arc.set_size(x2, y2)
        arc.set_pos(x1, y1)        
    def draw_line_ex(self, x1, y1, x2, y2, color=color.WHITE, width=1):#canvas
        line_style = lv.draw_line_dsc_t()
        line_style.init()
        line_style.color = color
        line_style.width = width
        p = [{"x":int(x1), "y":int(y1)},
            {"x":int(x2), "y":int(y2)}]
        self.canvas.draw_line(p, len(p), line_style)
        del line_style
    def draw_rect_ex(self, x, y, x_width, y_hight, color=color.WHITE):#canvas
        ''' 
        rect_style = lv.draw_rect_dsc_t()
        rect_style.init()
        #rect_style.bg_color = self.canvas_bg_color
        rect_style.border_color = color
        rect_style.border_width = 1
        self.canvas.draw_rect(x, y, x_width, y_hight, rect_style)
        '''
        line_style = lv.style_t()
        line_style.init()
        line_style.set_line_color(color)
        line_style.set_line_width(1)
        line = lv.line(lv.scr_act())
        p = [{"x":x, "y":y},{"x":x+x_width, "y":y},{"x":x+x_width, "y":y+y_hight},{"x":x, "y":y+y_hight},{"x":x, "y":y}]
        line.set_points(p, len(p))
        line.add_style(line_style, 0)
        del line_style
    def draw_fillrect_ex(self, x, y, x_width, y_hight, color=color.WHITE):#canvas
        rect_style = lv.draw_rect_dsc_t()
        rect_style.init()
        rect_style.bg_color = color
        rect_style.border_color = color
        rect_style.border_width = 1
        self.canvas.draw_rect(x, y, x_width, y_hight, rect_style)
        del rect_style
    def draw_polygon_ex(self, x1, y1, x2, y2, x3, y3, color=color.WHITE):
        line_style = lv.style_t()
        line_style.init()
        line_style.set_line_color(color)
        line_style.set_line_width(1)
        #line_style.set_line_opa(lv.OPA.COVER)
        line = lv.line(lv.scr_act())
        p = [{"x":int(x1), "y":int(y1)},{"x":int(x2), "y":int(y2)},{"x":int(x3), "y":int(y3)},{"x":int(x1), "y":int(y1)}]
        line.set_points(p, len(p))
        line.add_style(line_style, 0)
        del line_style
    def draw_fillpolygon_ex(self, x1, y1, x2, y2, x3, y3, color=color.WHITE):
        polygon_style = lv.draw_rect_dsc_t()
        polygon_style.init()
        polygon_style.bg_color = color
        polygon_style.border_color = color
        polygon_style.border_width = 1
        p = [{"x":int(x1), "y":int(y1)},{"x":int(x2), "y":int(y2)},
            {"x":int(x3), "y":int(y3)}]
        self.canvas.draw_polygon(p, len(p), polygon_style)
        del polygon_style
    def draw_arc_ex(self, x, y, start_angle, end_angle, color=color.WHITE, width=1, radius=10):#canvas
        arc_style = lv.draw_arc_dsc_t()
        arc_style.init()
        arc_style.color = color
        arc_style.width = width
        self.canvas.draw_arc(x, y, radius, start_angle, end_angle, arc_style)
        del arc_style
    def draw_point_ex(self, x, y, color=color.WHITE):#canvas
        self.canvas.set_px_color(int(x), int(y), color)
    def draw_text_ex(self, x, y, str, color=color.WHITE,font=font):#canvas
        text_style = lv.draw_label_dsc_t()
        text_style.init()
        text_style.color = color
        text_style.font = font
        self.canvas.draw_text(x, y, 1000, text_style, str)
        del text_style
    def set_font(self, size=16, fnt_path=None):
        global font
        if fnt_path:
            fs_drv = lv.fs_drv_t()
            fs_driver.fs_register(fs_drv, 'S')
            try:
                font=lv.font_load('S:' + fnt_path)                
            except:
                print('Cannot load font file')
                return None
            finally:
                del fs_drv
        else:
            try:
                font = getattr(lv, f'font_montserrat_{size}')
            except:
                print('Invalid font size')
                return None
        return font
    def draw_png(self, x, y, path):
        try:
            with open(path,'rb') as f:
                anim001_data = f.read()
        except:
            print("Could not find animimg001.png")
            sys.exit()
        imgs = lv.img_dsc_t({
            'data_size': len(anim001_data),
            'data': anim001_data
        })
        img = lv.img(lv.scr_act())
        img.set_src(imgs)
        img.align(lv.ALIGN.RIGHT_MID, x, y)
        time.sleep(0.05)
    def draw_popup(self, str, delay):
        style = lv.style_t()
        style.init()
        style.set_bg_opa(lv.OPA.COVER)
        style.set_bg_color(color.MWRGB(0x4c,0x51,0x57))
        #style.set_bg_opa(lv.OPA.TRANSP)
        style.set_text_color(color.MWRGB(248,248,248))
        style.set_text_font(lv.font_montserrat_14)
        style.set_border_width(3)
        style.set_border_color(color.MWRGB(48,64,72))
        style.set_pad_all(10)
        #style.set_text_opa(lv.OPA.COVER)
        #style.set_text_decor(False)
        try:
            if self.obj_popup == None:
                self.obj_popup = lv.label(lv.scr_act())
                self.obj_popup.center()
                self.obj_popup.add_style(style, 0)
                self.obj_popup.set_style_text_font(font, lv.PART.TICKS)
                self.obj_popup.set_text(str)
            else:
                self.obj_popup.center()
                self.obj_popup.add_style(style, 0)
                self.obj_popup.set_style_text_font(font, lv.PART.TICKS)
                self.obj_popup.set_text(str)
                
            if delay != 0:
                time.sleep(delay)
                self.obj_popup.remove_style_all()
                self.obj_popup.set_text('')
                #self.obj_popup.delect()
                #self.obj_popup = None
        except:
            pass
        del style
        time.sleep(0.01)

    class Draw_A_B():
        def __init__(self, x, y, x_size, y_size, bg_color=gds.Theme(dark_mode=True).bg_color, grid_color=gds.Theme(dark_mode=True).grid_color):
            self.A_B_area = (x_size,y_size)
            self.A_B_pos = (x,y)
            self.bg_color = bg_color
            self.color = grid_color
            self.font = font
            self.style = lv.style_t()
            self.style.init()
            self.style.set_line_color(self.color)
            self.style.set_bg_color(self.bg_color)
            #self.style.set_text_color(self.color)
            self.style.set_border_width(2)
            self.style.set_border_color(self.color)#add border        
            self.style.set_outline_width(1)
            self.style.set_outline_color(color.BLACK)#add outline
            self.style.set_radius(0)
        def get_a_b_type(self):
            return self.A_B.get_type()
        def __get_folat_to_int_num(self,float_type):
            temp = 1
            if float_type==0:
                temp=1
            elif float_type==1:
                temp=10
            elif float_type==2:
                temp=100
            elif float_type==3:
                temp=1000
            return int(temp)
        def __draw_a_b_cb(self,e):
            dsc = lv.obj_draw_part_dsc_t.__cast__(e.get_param())
            if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_X:
                dsc.line_dsc.color = self.color
                try:
                    dsc.label_dsc.color = self.str_color#self.color
                    tmp = int(dsc.value)/self.a_float_to_int
                    if self.a_float_to_int==1000:
                        str = b'%.3f'%(tmp)
                    elif self.a_float_to_int==100:
                        str = b'%.2f'%(tmp)
                    elif self.a_float_to_int==10:
                        str = b'%.1f'%(tmp)
                    else:
                        str = b'%.0f'%(tmp)
                    dsc.text = bytes(str,"ascii")   
                except:
                    pass
            elif dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_Y:
                dsc.line_dsc.color = self.color
                try:
                    dsc.label_dsc.color = self.str_color#self.color
                    tmp = int(dsc.value)/self.b_float_to_int
                    if self.b_float_to_int==1000:
                        str = b'%.3f'%(tmp)
                    elif self.b_float_to_int==100:
                        str = b'%.2f'%(tmp)
                    elif self.b_float_to_int==10:
                        str = b'%.1f'%(tmp)
                    else:
                        str = b'%.0f'%(tmp)
                    dsc.text = bytes(str,"ascii") 
                except:
                    pass
        def set_style_xy(self,x_div=11,y_div=11,x_div_minor=6,y_div_minor=6,str_color=gds.Theme(dark_mode=True).text_color,str_font=font):
            self.A_B = lv.chart(lv.scr_act())
            self.A_B.set_size(self.A_B_area[0], self.A_B_area[1])
            self.A_B.set_pos(self.A_B_pos[0], self.A_B_pos[1])
            self.A_B.add_style(self.style, 0)
            self.A_B.set_style_line_width(1, lv.PART.ITEMS)
            self.A_B.set_style_size(1, 1, lv.PART.INDICATOR)
            self.A_B.set_style_pad_all(0, 0)
            self.A_B.set_div_line_count(y_div, x_div)
            self.A_B.set_type(lv.chart.TYPE.SCATTER)
            self.A_B.set_axis_tick(lv.chart.AXIS.PRIMARY_X, 10, 5, x_div, x_div_minor, True, 100)
            self.A_B.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, y_div, y_div_minor, True, 100)
            self.A_points = []
            self.B_points = []
            self.A_B.set_style_text_font(str_font,lv.PART.TICKS)
            self.a_float_to_int = 0
            self.b_float_to_int = 0
            self.str_color = str_color
            self.A_B.add_event_cb(self.__draw_a_b_cb, lv.EVENT.DRAW_PART_BEGIN, None)  
            self.A_min_max = [0,0]
            self.B_min_max = [0,0]
            self.data_points_max = 0
            self.data_address = 0
            self.limint_minmax_flag = False
        def set_a_b_min_max(self,a_min,a_max,b_min,b_max):
            self.limint_minmax_flag = True
            self.A_min_max = [a_min, a_max]
            self.B_min_max = [b_min, b_max]          
        def __a_b_min_max(self,a_value,b_value):
            if self.limint_minmax_flag == True:
                pass
            elif self.data_points_max == 0:
                self.A_min_max = [int(a_value), int(a_value)]
                self.B_min_max = [int(b_value), int(b_value)]
            else:
                if self.A_min_max[1] < a_value:
                    self.A_min_max[1] = a_value
                if self.B_min_max[1] < b_value:
                    self.B_min_max[1] = b_value
                if self.A_min_max[0] > a_value:
                    self.A_min_max[0] = a_value
                if self.B_min_max[0] > b_value:
                    self.B_min_max[0] = b_value
        def add_a_b_data(self,data_color=color.RED):
            self.ser1 = self.A_B.add_series(data_color, lv.chart.AXIS.PRIMARY_Y)
            self.A_points = []
            self.B_points = []
            self.data_address = 0
            if self.data_points_max != 0:
                for i in range(self.data_points_max):
                    self.A_points.append(0)
                    self.B_points.append(0)
        def draw_a_b_data(self,a_data,b_data,a_float=0,b_float=0,point_num=0):
            self.a_float_to_int = self.__get_folat_to_int_num(a_float)
            self.b_float_to_int = self.__get_folat_to_int_num(b_float)
            if point_num <=1:
                a_value=int(a_data*self.a_float_to_int)
                b_value=int(b_data*self.b_float_to_int)
                if self.data_address < (self.data_points_max):
                    for i in range(self.data_address, self.data_points_max):
                        self.A_points[i] = a_value
                        self.B_points[i] = b_value
                else:
                    self.A_points.append(int(a_value))
                    self.B_points.append(int(b_value))
                self.__a_b_min_max(a_value, b_value)

                if self.data_points_max < len(self.A_points):
                    self.data_points_max = len(self.A_points)
                    self.A_B.set_point_count(self.data_points_max)
                
                if self.limint_minmax_flag == False:
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_X, self.A_min_max[0], self.A_min_max[1])
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_Y, self.B_min_max[0], self.B_min_max[1])
                else:
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_X, int(self.A_min_max[0]*self.a_float_to_int), int(self.A_min_max[1]*self.a_float_to_int))
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_Y, int(self.B_min_max[0]*self.b_float_to_int), int(self.B_min_max[1]*self.b_float_to_int))
                
                self.ser1.x_points = self.A_points
                self.ser1.y_points = self.B_points
                self.data_address += 1
                self.A_B.refresh()
            else:
                for i in range(point_num):
                    self.A_points.append(int(a_data[i]*self.a_float_to_int))
                    self.B_points.append(int(b_data[i]*self.b_float_to_int))
                if self.limint_minmax_flag == False:
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_X, self.A_min_max[0], self.A_min_max[1])
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_Y, self.B_min_max[0], self.B_min_max[1])
                else:
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_X, int(self.A_min_max[0]*self.a_float_to_int), int(self.A_min_max[1]*self.a_float_to_int))
                    self.A_B.set_range(lv.chart.AXIS.PRIMARY_Y, int(self.B_min_max[0]*self.b_float_to_int), int(self.B_min_max[1]*self.b_float_to_int))                    
                #self.data_points_max = int(point_num)
                #self.A_B.set_point_count(self.data_points_max)
                self.A_B.set_point_count(point_num)
                self.ser1.x_points = self.A_points
                self.ser1.y_points = self.B_points
                self.A_B.refresh()
            time.sleep(0.01)

    class Plot():
        """The tool can plot on your DSO.

        Args:
            x (int): x position of figure.
            y (int): y position of figure.
            width (int): Width of figure.
            height (int): Height of figure.
            dark_mode (bool, optional): Is dark mode or not. Defaults to True.

        A simple example is as follows.

        .. code-block::

            import dso_gui
            import gds_info as gds
            import dso_colors as color

            # Initialize the GUI
            gui = dso_gui.DrawObject()
            gui.set_bg_color(gds.Theme().bg_color)

            # Create figure object
            fig = gui.Plot(x=120, y=43, width=630, height=350)
            fig.grid(x_major=12, y_major=10, line_color=gds.Theme().grid_color, bg_color=gds.Theme().bg_color, x_minor=5, y_minor=5)
            fig.set_x_axis_on(text_color=gds.Theme().text_color, line_color=gds.Theme().grid_color, fmt='%d')
            fig.set_y_axis_on(text_color=gds.Theme().text_color, line_color=gds.Theme().grid_color, fmt='%.1f')

            # Add axis labels
            gui.draw_text(400, 440, "Time(h)", gds.Theme().text_color)
            gui.draw_text(30, 300, f"Temperature({chr(176)}C)", gds.Theme().text_color, 270)

            # Add legend
            gui.draw_text(310, 15, "Sample A", gds.Theme().text_color)
            gui.draw_line(270,25,300,25, color.LTGREEN)
            gui.draw_text(460, 15, "Sample B", gds.Theme().text_color)
            gui.draw_line(420,25,450,25, color.YELLOW)

            # Draw data point for Sample A
            valx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            valy = [20.0, 23.4, 26.8, 29.5, 33.2, 37.6, 41.2, 45.7, 50.0, 56.1, 62.7, 62.5, 62.8]
            fig.plot(valx, valy, color=color.LTGREEN)

            # Draw data point for Sample B
            valy = [20.0, 26.2, 32.5, 38.3, 45.7, 52.4, 59.3, 67.8, 75.4, 75.1, 75.2, 75.6, 75.3]
            fig.plot(valx, valy, color=color.YELLOW)

        
        """
        def __init__(self, x:int, y:int, width:int, height:int, dark_mode:bool=True):
            self.dark_mode = dark_mode
            self.fig = lv.chart(lv.scr_act())
            self.fig.set_type(lv.chart.TYPE.SCATTER)
            self.fig.set_size(width, height)
            self.fig.set_pos(x, y)
            self.fig.add_event_cb(self.__plot_cb, lv.EVENT.DRAW_PART_BEGIN, None)
            self.grid()
            self.set_line_width(1)
            self.set_size(1)
            self.set_x_axis_on()
            self.set_y_axis_on()
            self.x_ratio = 0
            self.y_ratio = 0
            self.xlim = False
            self.ylim = False
            self.graph_xlim = [None, None]
            self.graph_ylim = [None, None]
            self.new_ser = True

        def __refresh_ratio_step(self):
            self.x_ratio_step = min(self.x_major*100, 65535)
            self.x_shift_cnt = round(self.x_ratio_step/2)
            self.y_ratio_step = min(self.y_major*100, 65535)
            self.y_shift_cnt = round(self.y_ratio_step/2)

        def __plot_cb(self,e):
            dsc = lv.obj_draw_part_dsc_t.__cast__(e.get_param())
            if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_X:
                dsc.line_dsc.color = self.x_axis_line_color
                try:
                    dsc.label_dsc.color = self.x_axis_text_color
                    tmp = (int(dsc.value)+self.x_shift_cnt)*self.x_ratio
                    tmp = tmp+self.graph_xlim[0]
                    str = self.x_axis_fmt.encode()%(tmp)
                    dsc.text = bytes(str,"ascii")   
                    #print(f'xaxis : {str}, {int(dsc.value)}, {self.graph_xlim[0]}, {self.graph_xlim[1]}, {self.x_ratio}')
                except:
                    pass
            elif dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_Y:
                dsc.line_dsc.color = self.y_axis_line_color
                try:
                    dsc.label_dsc.color = self.y_axis_text_color
                    tmp = (int(dsc.value)+self.y_shift_cnt)*self.y_ratio
                    tmp = tmp+self.graph_ylim[0]
                    str = self.y_axis_fmt.encode()%(tmp)
                    dsc.text = bytes(str,"ascii") 
                    #print(f'yaxis : {str}, {int(dsc.value)}, {self.graph_ylim[0]}, {self.graph_ylim[1]}, {self.b_float_to_int}')
                except:
                    pass

        def get_xlim(self)->float:
            """Return the x-axis view limits.

            Returns:
                float: The current x-axis limits in data coordinates.
            """
            if hasattr(self, 'xmin') and hasattr(self, 'xmax'):
                return self.xmin, self.xmax
            else:
                return 0, 0

        def set_xlim(self, xmin:float, xmax:float):
            """Set the x-axis view limits.

            Args:
                xmin (float): The min xlim in data coordinates.
                xmax (float): The max xlim in data coordinates.
            """
            self.xmin = xmin
            self.xmax = xmax
            self.xlim = True

        def get_ylim(self)->float:
            """Return the y-axis view limits.

            Returns:
                float: The current y-axis limits in data coordinates.
            """
            if hasattr(self, 'ymin') and hasattr(self, 'ymax'):
                return self.ymin, self.ymax
            else:
                return 0, 0

        def set_ylim(self, ymin:float, ymax:float):
            """Set the y-axis view limits.

            Args:
                ymin (float): The min ylim in data coordinates.
                ymax (float): The max ylim in data coordinates.
            """
            self.ymin = ymin
            self.ymax = ymax
            self.ylim = True
        
        def set_x_axis_on(self, **kwargs):
            """Configure and show the x-axis.

            If you change grid's configure, then you have to run it once.

            Keyword Args:
                text_color: The y-axis text color.
                line_color: The y-axis color
                fmt: The y-axis text string format. ex:'%.2f'
            """
            if hasattr(self, 'x_major') and hasattr(self, 'x_minor'):
                pass
            else:
                return
            self.x_axis_text_color = kwargs.get('text_color', gds.Theme(self.dark_mode).text_color)
            self.x_axis_line_color = kwargs.get('line_color', gds.Theme(self.dark_mode).grid_color)
            self.x_axis_fmt = kwargs.get('fmt', '%.2f')
            self.fig.set_axis_tick(lv.chart.AXIS.PRIMARY_X, 10, 5, (self.x_major+1), self.x_minor, True, 100)

        def set_x_axis_off(self):
            """Hide all visual components of the x-axis.
            """
            self.fig.set_axis_tick(lv.chart.AXIS.PRIMARY_X, 10, 5, (1), (1), False, 100)

        def set_y_axis_on(self, **kwargs):
            """Configure and show the y-axis.

            If you change grid's configure, then you have to run it once.

            Keyword Args:
                text_color: The y-axis text color.
                line_color: The y-axis color
                fmt: The y-axis text string format. ex:'%.2f'
            """
            if hasattr(self, 'y_major') and hasattr(self, 'y_minor'):
                pass
            else:
                return
            self.y_axis_text_color = kwargs.get('text_color', gds.Theme(self.dark_mode).text_color)
            self.y_axis_line_color = kwargs.get('line_color', gds.Theme(self.dark_mode).grid_color)
            self.y_axis_fmt = kwargs.get('fmt', '%.2f')
            self.fig.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, (self.y_major+1), self.y_minor, True, 100)

        def set_y_axis_off(self):
            """Hide all visual components of the y-axis.
            """
            self.fig.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, (1), (1), False, 100)
        
        def grid(self, x_major:int=10, y_major:int=10, **kwargs):
            """Configure the grid lines.

            Args:
                x_major (int, optional): The X division number. Defaults to 10.
                y_major (int, optional): The Y division number. Defaults to 10.

            Keyword Args:
                line_color: The grid color.
                bg_color: The grid background color.
                font: The font
                x_minor: The minor X division number.
                y_minor: The minor X division number.
            """
            line_color = kwargs.get('line_color', gds.Theme(self.dark_mode).grid_color)
            bg_color = kwargs.get('bg_color', gds.Theme(self.dark_mode).bg_color)
            str_font = kwargs.get('font', font)

            self.x_minor = kwargs.get('x_minor', 1)
            self.y_minor = kwargs.get('y_minor', 1)
            self.x_major = x_major
            self.y_major = y_major

            self.fig.set_div_line_count((self.y_major+1), (self.x_major+1))
            
            self.fig.set_style_line_color(line_color, lv.PART.MAIN)
            self.fig.set_style_border_color(line_color, lv.PART.MAIN)
            self.fig.set_style_bg_color(bg_color, lv.PART.MAIN)
            self.fig.set_style_text_font(str_font,lv.PART.TICKS)

            self.fig.set_style_outline_color(color.BLACK, lv.PART.MAIN)
            self.fig.set_style_border_width(2, lv.PART.MAIN)
            self.fig.set_style_outline_width(1, lv.PART.MAIN)
            self.fig.set_style_radius(0, lv.PART.MAIN)
            self.fig.set_style_pad_all(0, 0)

            self.bg_color = bg_color
            self.color = line_color
            self.font = str_font

            self.__refresh_ratio_step()

        def set_line_width(self, width:int=1):
            """
            Set the line width, with 0 is only the mark.

            Args:
                width (int, optional): Defaults to 1.
            """
            self.fig.set_style_line_width(width, lv.PART.ITEMS)

        def set_size(self, size:int=1):
            """The marker size in points.

            Args:
                size (int, optional): Defaults to 1.
            """
            self.fig.set_style_size(size, size, lv.PART.INDICATOR)
            
        def __plot_init(self):
            if hasattr(self, 'ser'):
                pass
            else:
                self.ser = []
            if hasattr(self, 'ser_data'):
                pass
            else:
                self.ser_data = []
            if hasattr(self, 'graph_xlim'):
                pass
            else:
                self.graph_xlim = [None, None]
            if hasattr(self, 'graph_ylim'):
                pass
            else:
                self.graph_ylim = [0, 0]

        def plot(self, *args, **kwargs):
            """Plot y versus x as lines or marks.

            Both x and y will be a number or 1-D list

            >>> plot(x, y)        # plot x and y using default color
            >>> plot(y)           # plot y using x as index array 0..N-1
            >>> plot(x, y, color=lv.color_hex(0x000000))        # plot x and y using hex color code

            Keyword Args:
                color: the line color

            """
            line_color = kwargs.get('color', color.RED)

            if len(args) > 2:
                return

            plot_method = 0
            if len(args) == 1:
                # Only ydata input
                ydata = args[0]
                if isinstance(ydata, list):
                    xdata = list(range(len(ydata)))
                    plot_method = 1
                else:
                    xdata = None
            else:
                # Both xdata and ydata input
                xdata = args[0]
                ydata = args[1]
                if isinstance(xdata,list) and isinstance(ydata,list):
                    plot_method = 1
                else:
                    pass
            
            self.__plot_init()
            if plot_method:
                self.ser.append(self.fig.add_series(line_color, lv.chart.AXIS.PRIMARY_Y))
                self.ser_data.append([])
                self.__plot_data(xdata, ydata)
            else:
                if self.new_ser:
                    self.ser.append(self.fig.add_series(line_color, lv.chart.AXIS.PRIMARY_Y))
                    self.ser_data.append([[],[]])
                    self.hold(False)
                self.__plot_data_attach(xdata, ydata)
            
            gc.collect()
            self.fig.refresh()
            time.sleep(0.1)

        def __find_graph_lim(self, data, axis) -> bool:
            limit_change = False
            if axis == 0:
                # X axis
                if self.graph_xlim[0] == None:
                    self.graph_xlim[0] = min(data)
                if self.graph_xlim[1] == None:
                    self.graph_xlim[1] = max(data)

                if self.xlim:
                    self.graph_xlim[0] = self.xmin
                    limit_change = True
                else:
                    if min(data) < self.graph_xlim[0]:
                        self.graph_xlim[0] = min(data)
                        limit_change = True
                
                if self.xlim:
                    self.graph_xlim[1] = self.xmax
                    limit_change = True
                else:
                    if max(data) > self.graph_xlim[1]:
                        self.graph_xlim[1] = max(data)
                        limit_change = True
                #print(f'x : {self.graph_xlim[0]} {self.graph_xlim[1]}')
            elif axis == 1:
                # Y asix
                if self.graph_ylim[0] == None:
                    self.graph_ylim[0] = min(data)
                if self.graph_ylim[1] == None:
                    self.graph_ylim[1] = max(data)
                
                if self.ylim:
                    self.graph_ylim[0] = self.ymin
                    limit_change = True
                else:
                    if min(data) < self.graph_ylim[0]:
                        self.graph_ylim[0] = min(data)
                        limit_change = True

                if self.ylim:
                    self.graph_ylim[1] = self.ymax
                    limit_change = True
                else:
                    if max(data) > self.graph_ylim[1]:
                        self.graph_ylim[1] = max(data)
                        limit_change = True
            return limit_change
        
        def __set_graph_lim(self):
            if self.xlim:
                xlim_1 = (self.xmin-self.graph_xlim[0])/self.x_ratio
                xlim_2 = (self.xmax-self.graph_xlim[0])/self.x_ratio
            else:
                xlim_1 = 0
                xlim_2 = (self.graph_xlim[1]-self.graph_xlim[0])/self.x_ratio

            if self.ylim:
                ylim_1 = (self.ymin-self.graph_ylim[0])/self.y_ratio
                ylim_2 = (self.ymax-self.graph_ylim[0])/self.y_ratio
            else:
                ylim_1 = 0
                ylim_2 = (self.graph_ylim[1]-self.graph_ylim[0])/self.y_ratio

            xlim_1 -= self.x_shift_cnt
            xlim_1 = max(min(xlim_1, 32767), -32768)

            xlim_2 -= self.x_shift_cnt
            xlim_2 = max(min(xlim_2, 32767), -32768)

            self.fig.set_range(lv.chart.AXIS.PRIMARY_X, round(xlim_1), round(xlim_2))

            ylim_1 -= self.y_shift_cnt
            ylim_1 = max(min(ylim_1, 32767), -32768)

            ylim_2 -= self.y_shift_cnt
            ylim_2 = max(min(ylim_2, 32767), -32768)

            self.fig.set_range(lv.chart.AXIS.PRIMARY_Y, round(ylim_1), round(ylim_2))
        
        def __plot_data(self, a_data:list, b_data:list):
            limit_change = [False, False]
            total_series = len(self.ser)
            data_len_1 = len(a_data)
            data_len_2 = len(b_data)
            
            # store original data (float)
            self.ser_data[total_series-1].append(a_data)
            self.ser_data[total_series-1].append(b_data)

            self.fig.set_point_count(data_len_1)

            limit_change[0] = self.__find_graph_lim(self.ser_data[total_series-1][0], 0)
            limit_change[1] = self.__find_graph_lim(self.ser_data[total_series-1][1], 1)
            
            self.x_ratio = (self.graph_xlim[1]-self.graph_xlim[0])/self.x_ratio_step
            self.y_ratio = (self.graph_ylim[1]-self.graph_ylim[0])/self.y_ratio_step

            if self.x_ratio == 0:
                self.x_ratio = 1
            if self.y_ratio == 0:
                self.y_ratio = 1

            if limit_change[0]:
                for i in range(total_series):
                    x_array=[0]*data_len_1
                    for j in range(data_len_1):
                        x_array[j] = int((self.ser_data[i][0][j]-self.graph_xlim[0])/self.x_ratio)
                        x_array[j] -= self.x_shift_cnt
                    self.ser[i].x_points = x_array
            else:
                i = total_series-1
                x_array=[0]*data_len_1
                for j in range(data_len_1):
                    x_array[j] = int((self.ser_data[i][0][j]-self.graph_xlim[0])/self.x_ratio)
                    x_array[j] -= self.x_shift_cnt
                self.ser[i].x_points = x_array

            if limit_change[1]:
                for i in range(total_series):
                    y_array=[0]*data_len_2
                    for j in range(data_len_2):
                        y_array[j] = int((self.ser_data[i][1][j]-self.graph_ylim[0])/self.y_ratio)
                        y_array[j] -=self.y_shift_cnt
                    self.ser[i].y_points = y_array
            else:
                i = total_series-1
                y_array=[0]*data_len_2
                for j in range(data_len_2):
                    y_array[j] = int((self.ser_data[i][1][j]-self.graph_ylim[0])/self.y_ratio)
                    y_array[j] -=self.y_shift_cnt
                self.ser[i].y_points = y_array
            
            del x_array
            del y_array

            self.__set_graph_lim()
            

        def __plot_data_attach(self, xdata, ydata):
            total_series = len(self.ser)
            if len(self.ser_data[total_series-1][0]) >= 65535:
                return
            
            # store original data (float)
            self.ser_data[total_series-1][1].append(ydata)
            data_len_2 = len(self.ser_data[total_series-1][1])

            if xdata is None:
                xdata = data_len_2-1
            
            self.ser_data[total_series-1][0].append(xdata)
            #data_len_1 = len(self.ser_data[total_series-1][0])
            
            p_cnt = 0
            for i in range(total_series):
                p_cnt = max(p_cnt, len(self.ser_data[i][0]))
            self.fig.set_point_count(p_cnt)

            self.__find_graph_lim(self.ser_data[total_series-1][0], 0)
            self.__find_graph_lim(self.ser_data[total_series-1][1], 1)

            self.x_ratio = (self.graph_xlim[1]-self.graph_xlim[0])/self.x_ratio_step
            self.y_ratio = (self.graph_ylim[1]-self.graph_ylim[0])/self.y_ratio_step

            if self.x_ratio == 0:
                self.x_ratio = 1
            if self.y_ratio == 0:
                self.y_ratio = 1

            for i in range(total_series):
                x_array = [0]*p_cnt
                for j in range(p_cnt):
                    try:
                        x_array[j] = int((self.ser_data[i][0][j]-self.graph_xlim[0])/self.x_ratio)
                        x_array[j] -= self.x_shift_cnt
                    except:
                        x_array[j] = x_array[j-1]
                self.ser[i].x_points = x_array

            for i in range(total_series):
                y_array=[0]*p_cnt
                for j in range(p_cnt):
                    try:
                        y_array[j] = int((self.ser_data[i][1][j]-self.graph_ylim[0])/self.y_ratio)
                        y_array[j] -=self.y_shift_cnt
                    except:
                        y_array[j] = y_array[j-1]
                self.ser[i].y_points = y_array

            del x_array
            del y_array

            self.__set_graph_lim()
        
        def hold(self, b:bool=True):
            """
            Set the hold state.

            >>> hold()      # hold is on
            >>> hold(True)  # hold is on
            >>> hold(False) # hold is off

            Args:
                b (bool, optional): Defaults to True.
            """
            self.new_ser = b
