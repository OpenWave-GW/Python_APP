# Name: dso_ref.py
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

class Ref():
    """This module can control the Reference function on your DSO

    .. important:: You need to get the reference waveform before these operations.
    """
    def __init__(self, parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

    def is_on(self, ref:int) -> bool:
        cmd = ':REF%d:DISPlay?'%(ref)
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_on(self, ref:int):
        """Set reference ON.

        Args:
            ref (int): reference number
        """
        cmd = ':REF%d:DISPlay ON'%(ref)
        self.write(cmd)

    def set_off(self, ref:int):
        """Set reference OFF.

        Args:
            ref (int): reference number
        """
        cmd = ':REF%d:DISPlay OFF'%(ref)
        self.write(cmd)

    def get_v_pos(self, ref:int) -> float:
        """Get reference vertical position.

        Args:
            ref (int): reference number

        Returns:
            float: position value
        """
        cmd = ':REF%d:OFFSet?'%(ref)
        ret = self.query(cmd)
        return float(ret)

    def set_v_pos(self, ref:int, pos:float):
        """Set reference vertical position.

        Args:
            ref (int): reference number
            pos (float): position value
        """
        cmd = ':REF%d:OFFSet %f'%(ref, pos)
        self.write(cmd)

    def get_v_scale(self, ref:int) -> float:
        """Get reference vertical scale.

        Args:
            ref (int): reference number

        Returns:
            float: scale value
        """
        cmd = ':REF%d:SCALe?'%(ref)
        ret = self.query(cmd)
        return float(ret)

    def set_v_scale(self, ref:int, scale:float):
        """Set reference vertical scale.

        Args:
            ref (int): reference number
            scale (float): scale value
        """
        cmd = ':REF%d:SCALe %f'%(ref, scale)
        self.write(cmd)

    def get_h_pos(self, ref:int) -> float:
        """Get reference horizontal position.

        Args:
            ref (int): reference number

        Returns:
            float: position value
        """
        cmd = ':REF%d:TIMebase:POSition?'%(ref)
        ret = self.query(cmd)
        return float(ret)

    def set_h_pos(self, ref:int, pos:float):
        """Set reference horizontal position.

        Args:
            ref (int): reference number
            pos (float): position value
        """
        cmd = ':REF%d:TIMebase:POSition %f'%(ref, pos)
        self.write(cmd)

    def get_h_scale(self, ref:int) -> float:
        """Get reference horizontal scale.

        Args:
            ref (int): reference number

        Returns:
            float: scale value
        """
        cmd = ':REF%d:TIMebase:SCALe?'%(ref)
        ret = self.query(cmd)
        return float(ret)

    def set_h_scale(self, ref:int, scale:float):
        """Set reference horizontal scale.

        Args:
            ref (int): reference number
            scale (float): scale value
        """
        cmd = ':REF%d:TIMebase:SCALe %f'%(ref, scale)
        self.write(cmd)