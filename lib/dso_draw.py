# Name: dso_draw.py
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

import sys
class Draw():
    """This module can draw or display certain drawing content on your DSO.
    """
    def __init__(self, parent):
        self.write = parent.write
        self.query = parent.query
        
    def __set_py_flag(self, mode):
        cmd = ":PYFLAG '%s'" % mode
        self.write(cmd + '\n')
        self.ChkCommand(":PYFLAG?")

    def ChkCommand(self, cmd:str) -> str:
        time = 0
        while True: 
            info = self.query(cmd + '\n')
            if info == 'ON':
                break
            elif time >= 10:
                #sys.exit(1)
                print('command error!')
                break
            else:
                time += 1

    def get_winid(self) -> int:
        """
        Description
            Returns the ID of a specified widget window.
        Prototype
            def get_winid(self);             
        """        
        cmd = ":PYWID?"
        info = self.query(cmd + '\n')
        return int(info)

    def creat_win(self, x_pos:int, y_pos:int, x_size:int, y_size:int) -> int:
        """
        Description
            Creates a window as a child window.
        Prototype
            def creat_win(self, x_pos:int, y_pos:int, x_size:int, y_size:int) -> int;
        Return value
            Handle for the child window.
        """
        cmd = ":PYWID '%d,%d,%d,%d,'" % (x_pos, y_pos, x_size, y_size)
        self.write(cmd + '\n')
        devid = self.get_winid()
        return devid

    def clear_win(self):
        """
        Description
            Clears the current window.
        Prototype
            def clear_win(self);
        """
        cmd = ":PYCLEARWID"
        self.write(cmd + '\n')

    def del_win(self, wid:int):
        """
        Description
            Deletes a specified window.
        Prototype
            def del_win(self, wid:int);
        """
        cmd = ":PYDELETEWID '%d'" % (wid)
        self.write(cmd + '\n')

    def sel_win(self, wid:int):
        """
        Description
            Sets the active window to be used for drawing operations.
        Prototype
            def sel_win(self, wid:int);
        """
        cmd = ":PYSELECTWID '%d'" % (wid)
        self.write(cmd + '\n')

    def del_allwin(self):
        """
        Description
            Deletes all window.
        Prototype
            def del_win(self, wid:int);
        """
        cmd = ":PYDELALLWID"
        self.write(cmd + '\n')

    def draw_win(self):
        """
        Description
            Redraw all windows
        Prototype
            def draw_win(self);
        """
        cmd = ":PYDRAW"
        self.write(cmd + '\n')
        self.ChkCommand(":PYDRAW?")

    def set_color(self, rad:int, green:int, blue:int):
        """
        Description
            Sets the current foreground color.
        Prototype
            def set_color(self, rad:int, green:int, blue:int);        
        """
        cmd = ":PYSETCOLOR '%d,%d,%d,'" % (rad, green, blue)
        self.write(cmd + "\n")
        self.ChkCommand(":PYSETCOLOR?")

    def set_bkcolor(self, rad:int, green:int, blue:int):
        """
        Description
            Sets the current background color.
        Prototype
            def set_bkcolor(self, rad:int, green:int, blue:int);
        """
        cmd = ":PYSETBKCOLOR '%d,%d,%d,'" % (rad, green, blue)
        self.write(cmd + "\n")
        self.ChkCommand(":PYSETBKCOLOR?")

    def _del_button(self, wid:int):
        """
        Description
            Deletes a specified button.
        Prototype
            def del_button(self, wid:int);
        """
        cmd = ":PYDELBUTTON '%d'" % (wid)
        self.write(cmd+'\n')
    
    def _get_button(self) -> str:
        """
        Description
            Retrieves the text of the specified BUTTON widget.
        Prototype
            def get_button(self) -> str;
        Return value
            Handle for the child button.
        """
        cmd = ":PYBUTTON?"
        info = self.query(cmd+'\n')
        return info

    def _set_button(self, x_pos:int, y_pos:int, x_size:int, y_size:int, idx:str) -> int:
        """
        Description
            Creates a BUTTON widget of a specified size at a specified location.
        Prototype
            def set_button(self, x_pos:int, y_pos:int, x_size:int, y_size:int, idx:str) -> int;
        Return value
            Handle of the created BUTTON widget; 0 if the function fails.
        """        
        cmd = ":PYBUTTON '%d,%d,%d,%d,%s'" % (x_pos, y_pos, x_size, y_size, idx)
        self.write(cmd+'\n')
        return int(self.get_button())

    def draw_point(self, x_pos:int, y_pos:int):
        """
        Description
            Draws a point with the current pen size at a specified position in the current window.
        Prototype
            def draw_point(self, x_pos:int, y_pos:int);"""
        cmd = ":PYPOINT '%d,%d,'" % (x_pos, y_pos)
        self.write(cmd + '\n')
        self.ChkCommand(":PYPOINT?")

    def draw_line(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int):
        """
        Description
            Draws a line from a specified starting point to a specified endpoint in the current window(absolute coordinates).
        Prototype
            def draw_line(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int);
        """        
        cmd = ":PYLINE '%d,%d,%d,%d,'" % (x0_pos, y0_pos, x1_pos, y1_pos)
        self.write(cmd + '\n')
        self.ChkCommand(":PYLINE?")

    def draw_rect(self, x_pos:int, y_pos:int, x_size:int, y_size:int):
        """
        Description
            Draws a rectangle at a specified position in the current window.
        Prototype
            def draw_rect(self, x_pos:int, y_pos:int, x_size:int, y_size:int);  
        """   
        cmd = ":PYRECT '%d,%d,%d,%d,'" % (x_pos, y_pos, x_size, y_size)
        self.write(cmd + '\n')
        self.ChkCommand(":PYRECT?")

    def draw_fillrect(self, x_pos:int, y_pos:int, x_size:int, y_size:int):
        """
        Description
            Draws a filled rectangular area at a specified position in the current window.
        Prototype
            def draw_fillrect(self, x_pos:int, y_pos:int, x_size:int, y_size:int);        
        """
        cmd = ":PYFILLRECT '%d,%d,%d,%d,'" % (x_pos, y_pos, x_size, y_size)
        self.write(cmd + '\n')
        self.ChkCommand(":PYFILLRECT?")

    def draw_poly(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int, x2_pos:int, y2_pos:int):
        """
        Description
            Draws the outline of a polygon defined by a list of points in the current window.
        Prototype
            def draw_poly(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int, x2_pos:int, y2_pos:int);
        """        
        cmd = ":PYPOLY '%d,%d,%d,%d,%d,%d,'" % (x0_pos, y0_pos, x1_pos, y1_pos, x2_pos, y2_pos)
        self.write(cmd + '\n')
        self.ChkCommand(":PYPOLY?")

    def draw_fillpoly(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int, x2_pos:int, y2_pos:int):
        """
        Description
            Draws a filled polygon defined by a list of points in the current window.
        Prototype
            def draw_fillpoly(self, x0_pos:int, y0_pos:int, x1_pos:int, y1_pos:int, x2_pos:int, y2_pos:int);
        """
        cmd = ":PYFILLPOLY '%d,%d,%d,%d,%d,%d,'" % (x0_pos, y0_pos, x1_pos, y1_pos, x2_pos, y2_pos)
        self.write(cmd + '\n')
        self.ChkCommand(":PYFILLPOLY?")

    def draw_ellipse(self, x_pos:int, y_pos:int, rx:int, ry:int):
        """
        Description
            Draws the outline of an ellipse of specified dimensions, at a specified position in the current window.
        Prototype
            def draw_ellipse(self, x_pos:int, y_pos:int, rx:int, ry:int);
        """
        cmd = ":PYELLIPSE '%d,%d,%d,%d,'" % (x_pos, y_pos, rx, ry)
        self.write(cmd + '\n')
        self.ChkCommand(":PYELLIPSE?")

    def draw_fillellipse(self, x_pos:int, y_pos:int, rx:int, ry:int):
        """
        Description
            Draws a filled ellipse of specified dimensions at a specified position in the current window.
        Prototype
            def draw_fillellipse(self, x_pos:int, y_pos:int, rx:int, ry:int);
        """
        cmd = ":PYFILLELLIPSE '%d,%d,%d,%d,'" % (x_pos, y_pos, rx, ry)
        self.write(cmd + '\n')
        self.ChkCommand(":PYFILLELLIPSE?")

    def draw_text(self, x_pos:int, y_pos:int, str:str):
        """
        Description
            Displays the string passed as parameter at a specified position in the current window using the current font.
        Prototype
            def draw_text(self, x_pos:int, y_pos:int, str:str);
        """
        text = ""
        for i in range(len(str)):
            num = ord(str[i])
            if(num>127):
                text += ("{%s}" % (chr(num-127)))
            else:
                text += str[i]
        cmd = ":PYTEXT '%d,%d,%s'" % (x_pos, y_pos, text)
        self.write(cmd + '\n')
        self.ChkCommand(":PYTEXT?")

    def draw_poptext(self, str:str):
        """
        Description
            Displays the string passed as a parameter at the specified position in the popup message using the current font.
        Prototype
            def draw_text(self, x_pos:int, y_pos:int, str:str);
        """
        tmp = ''
        for i in range(0,len(str)):
            if(str[i] == '\n'):
                tmp += "\x7F"
            else:
                tmp += str[i]
        cmd = ":PYPOPTEXT '%s'" % (tmp)
        self.write(cmd + '\n')
        self.ChkCommand(":PYPOPTEXT?")