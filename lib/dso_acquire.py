# Name: dso_acquire.py
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

class Acquire():
    """This module can control the Acquire function on your DSO
    """
    def __init__(self, parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

        self.is_ch_support = parent.is_ch_support

    def is_average(self) -> bool:
        """Is now average mode?

        Returns:
            bool: True or False
        """
        cmd=':ACQ:MOD?\n'
        ret = self.query(cmd)
        if 'AVERage'.upper() in ret:
            return True
        else:
            return False

    def average_times(self) -> int:
        """Now average times

        Returns:
            int: average times
        """
        cmd = ':ACQuire:AVERage?\n'
        ret = self.query(cmd)
        return int(ret)

    def set_average(self, value:int=0):
        """Set DSO to Average mode.

        Args:
            value (int, optional): average times. Defaults to 0 is do not change.
        """
        self.write(':ACQ:MOD AVERage')
        if value > 0:
            cmd = ':ACQuire:AVERage %d\n'%value
            self.write(cmd)
    
    def is_peak_detect(self) -> bool:
        """Is now peak detect mode?

        Returns:
            bool: True or False
        """
        cmd=':ACQ:MOD?\n'
        ret = self.query(cmd)
        if 'PDETect'.upper() in ret:
            return True
        else:
            return False
    
    def set_peak_detect(self):
        """Set DSO to PDETect mode.
        """
        self.write(':ACQ:MOD PDETect')
    
    def is_sample(self) -> bool:
        """Is now sample mode?

        Returns:
            bool: True or False
        """
        cmd=':ACQ:MOD?\n'
        ret = self.query(cmd)
        if 'SAMPle'.upper() in ret:
            return True
        else:
            return False
    
    def set_sample(self):
        """Set DSO to Sample mode.
        """
        self.write(':ACQ:MOD SAMPle')

    def mode(self) -> str:
        """Now acquire mode

        Returns:
            str: acquire mode
        """
        cmd=':ACQ:MOD?\n'
        ret = self.query(cmd)
        return ret
    
    def length(self) -> int:
        """Now acquire length

        Returns:
            int: acquire length
        """
        cmd=':ACQ:RECO?\n'
        ret = self.query(cmd)
        return int(float(ret))

    def set_length(self, value:float):
        """Set acquire length

        Args:
            value (float): acquire length
        """
        cmd=':ACQ:RECO %d\n'%value
        self.write(cmd)

    def get_state(self, ch:int) -> bool:
        if self.is_ch_support(ch):
            pass
        else:
            return False
        cmd=':ACQuire%d:STATe?\n'%ch
        ret = self.query(cmd)
        if int(ret) == 1:
            return True
        else:
            return False