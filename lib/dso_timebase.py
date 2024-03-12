# Name: dso_timebase.py
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

class TimeBase():
    """This module can control the Horizontal function on your DSO
    """
    def __init__(self, parent, vernier:bool=False) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

        self.vernier = vernier

    def get_timebase(self) -> float:
        """Get the DSO TimeBase value

        Returns:
            float: TimeBase value
        """
        cmd=':TIM:SCAL?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_timebase(self, hdiv:float):
        """Change the DSO TimeBase value

        Args:
            hdiv (float): TimeBase value
        """
        cmd=':TIM:SCAL %f\n'%hdiv
        self.write(cmd)

    def get_windowtimebase(self) -> float:
        """Get the DSO Timebase Windowzoom value

        Returns:
            float: Window Timebase Windowzoom value
        """
        cmd=':TIM:WIND:SCAL?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_windowtimebase(self, hdiv:float):
        """Change the DSO Timebase Windowzoom value

        Args:
            hdiv (float): Timebase Windowzoom value
        """
        cmd=':TIM:WIND:SCAL %f\n'%hdiv
        self.write(cmd)

    def get_hposition(self) -> float:
        """Get the DSO Horizontal Position

        Returns:
            float: Horizontal Position value
        """
        cmd=':TIM:POS?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_hposition(self, hpos:float):
        """Change the DSO Horizontal Position

        Args:
            hpos (float): Horizontal Position value
        """
        cmd=':TIM:POS %f\n'%hpos
        self.write(cmd)

    def get_mode(self) -> str:
        """Get Horizontal mode.

        Returns:
            str: Horizontal mode
        """
        cmd=':TIMebase:MODe?\n'
        ret=self.query(cmd)
        return ret

    def set_mode(self, mode:str):
        """Set Horizontal mode.

        Args:
            mode (str): MAIN, WINDow or XY
        """
        cmd=':TIMebase:MODe %s\n'%(mode)
        self.write(cmd)