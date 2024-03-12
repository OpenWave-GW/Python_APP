# Name: dso_awg.py
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

class Awg():
    """This module can control the AWG function on your DSO
    """
    def __init__(self,parent) -> None:
        self.write = parent.write
        self.query = parent.query

    def is_on(self, ch:int) -> bool:
        """

        Args:
            ch (int): AWG number

        Returns:
            bool: True or False
        """
        cmd = ':AWG%d:OUTPut:STATe?\n'%ch
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_on(self, ch:int, wave:str=None, freq:float=None, amp:float=None, offset:float=None):
        """Set AWG ON

        Args:
            ch (int): AWG number
            wave (str, optional): ARBitrary | SINE | SQUAre | PULSe | RAMP | DC | NOISe | SINC | GAUSsian | LORENtz | EXPRise | EXPFall | HAVERSINe | CARDIac. Defaults to None is do not change.
            freq (float, optional): waveform frequency. Defaults to None is do not change.
            amp (float, optional): waveform amplitude. Defaults to None is do not change.
            offset (float, optional): waveform offset. Defaults to None is do not change.
        """
        cmd = ':AWG%d:OUTPut:STATe ON\n'%(ch)
        self.write(cmd)
        if wave is not None:
            cmd = ':AWG%d:FUNCtion %s'%(ch, wave)
            self.write(cmd)
        if freq is not None:
            cmd = ':AWG%d:FREQuency %f'%(ch, freq)
            self.write(cmd)
        if amp is not None:
            cmd = ':AWG%d:AMPlitude %f'%(ch, amp)
            self.write(cmd)
        if offset is not None:
            cmd = ':AWG%d:OFFSet %f'%(ch, offset)
            self.write(cmd)

    def set_off(self, ch:int):
        """Set AWG OFF

        Args:
            ch (int): AWG number
        """
        cmd = ':AWG%d:OUTPut:STATe OFF\n'%(ch)
        self.write(cmd)
    
    def wave(self, ch:int) -> str:
        """Now waveform.

        Args:
            ch (int): AWG number

        Returns:
            str: waveform
        """
        cmd = ':AWG%d:FUNCtion?'%(ch)
        ret = self.query(cmd)
        return ret

    def freq(self, ch:int) -> float:
        """Now frequency

        Args:
            ch (int): AWG number

        Returns:
            float: frequency value
        """
        cmd = ':AWG%d:FREQuency?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def amp(self, ch:int) -> float:
        """Now amplitude

        Args:
            ch (int): AWG number

        Returns:
            float: amplitude value
        """
        cmd = ':AWG%d:AMPlitude?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def offset(self, ch:int) -> float:
        """Now offset

        Args:
            ch (int): AWG number

        Returns:
            float: offset value
        """
        cmd = ':AWG%d:OFFSet?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def load(self, ch:int) -> str:
        """Now load

        Args:
            ch (int): AWG number

        Returns:
            str: FIFTY or HIGHZ
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance?'%(ch)
        ret = self.query(cmd)
        return ret
    
    def set_load_50ohm(self, ch:int):
        """Set load to 50 ohm

        Args:
            ch (int): AWG number
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance FIFTY'%(ch)
        self.write(cmd)

    def set_load_highz(self, ch:int):
        """Set load to HighZ

        Args:
            ch (int): AWG number
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance HIGHZ'%(ch)
        self.write(cmd)

    def set_phase(self, ch:int, value:float):
        """Sets the channel phase

        Args:
            ch (int): AWG number
            value (float): channel phase

        """
        cmd = ':AWG%d:PHAse %f'%(ch, value)
        self.write(cmd)

    def phase(self, ch:int) -> float:
        """Returns the channel phase.

        Args:
            ch (int): AWG number

        Returns:
            float: channel phase
        """
        cmd = ':AWG%d:pHAse?'%(ch)
        ret = self.query(cmd)
        return float(ret)
    