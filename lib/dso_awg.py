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

    def is_on(self, ch: int = 1) -> bool:
        """

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            bool: True or False
        """
        cmd = ':AWG%d:OUTPut:STATe?'%ch
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_on(self, ch: int = 1, wave: str = None, freq: float = None, amp: float = None, offset: float = None):
        """Set AWG ON

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
            wave (str, optional): ARBitrary | SINE | SQUAre | PULSe | RAMP | DC | NOISe | SINC | GAUSsian | LORENtz | EXPRise | EXPFall | HAVERSINe | CARDIac. Defaults to None is do not change.
            freq (float, optional): waveform frequency. Defaults to None is do not change.
            amp (float, optional): waveform amplitude. Defaults to None is do not change.
            offset (float, optional): waveform offset. Defaults to None is do not change.
        """
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
        cmd = ':AWG%d:OUTPut:STATe ON\n'%(ch)
        self.write(cmd)

    def set_off(self, ch: int = 1):
        """Set AWG OFF

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
        """
        cmd = ':AWG%d:OUTPut:STATe OFF\n'%(ch)
        self.write(cmd)
    
    def wave(self, ch: int = 1) -> str:
        """Now waveform.

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            str: waveform
        """
        cmd = ':AWG%d:FUNCtion?'%(ch)
        ret = self.query(cmd)
        return ret

    def freq(self, ch: int = 1) -> float:
        """Now frequency

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            float: frequency value
        """
        cmd = ':AWG%d:FREQuency?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def amp(self, ch: int = 1) -> float:
        """Now amplitude

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            float: amplitude value
        """
        cmd = ':AWG%d:AMPlitude?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def offset(self, ch: int = 1) -> float:
        """Now offset

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            float: offset value
        """
        cmd = ':AWG%d:OFFSet?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def load(self, ch: int = 1) -> str:
        """Now load

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            str: FIFTY or HIGHZ
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance?'%(ch)
        ret = self.query(cmd)
        return ret
    
    def set_load_50ohm(self, ch: int = 1):
        """Set load to 50 ohm

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance FIFTY'%(ch)
        self.write(cmd)

    def set_load_highz(self, ch: int = 1):
        """Set load to HighZ

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
        """
        cmd = ':AWG%d:OUTPut:LOAd:IMPEDance HIGHZ'%(ch)
        self.write(cmd)

    def set_phase(self, ch: int = 1, value: float = None):
        """Sets the channel phase

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
            value (float): channel phase

        """
        cmd = ':AWG%d:PHAse %f'%(ch, value)
        self.write(cmd)

    def phase(self, ch: int = 1) -> float:
        """Returns the channel phase.

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.

        Returns:
            float: channel phase
        """
        cmd = ':AWG%d:pHAse?'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def set_awg_parameters(self, ch: int = 1, wave: str = None, freq: float = None, amp: float = None, offset: float = None, enable: bool = None) -> None:
        """Sets various parameters for AWG.

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
            wave (str, optional): ARBitrary | SINE | SQUAre | PULSe | RAMP | DC | NOISe | SINC | GAUSsian | LORENtz | EXPRise | EXPFall | HAVERSINe | CARDIac.
            freq (float, optional): waveform frequency.
            amp (float, optional): waveform amplitude.
            offset (float, optional): waveform offset.
            enable (bool, optional): If True, sets AWG output ON. If False, sets AWG output OFF.
        """
        if wave is not None:
            cmd = ':AWG%d:FUNCtion %s' % (ch, wave)
            self.write(cmd)
        if freq is not None:
            cmd = ':AWG%d:FREQuency %f' % (ch, freq)
            self.write(cmd)
        if amp is not None:
            cmd = ':AWG%d:AMPlitude %f' % (ch, amp)
            self.write(cmd)
        if offset is not None:
            cmd = ':AWG%d:OFFSet %f' % (ch, offset)
            self.write(cmd)
        if enable is not None:
            cmd = ':AWG%d:OUTPut:STATe ON' % (ch) if enable else ':AWG%d:OUTPut:STATe OFF' % (ch)
            self.write(cmd)

    def load_arb_waveform(self, ch: int = 1 , source: str = None) -> None:
        """Load the arbitrary waveform.

        Args:
            ch (int, optional): AWG Channel number (1 or 2). Defaults to 1.
            source (str): The waveform file to be loaded. 
                        Must be one of the predefined waveforms {'ARB1', 'ARB2', 'ARB3', 'ARB4'}
                        or a file path such as 'Disk:/xxx.UAW' or 'USB:/xxx.UAW'.
        """
        if source is None:
            raise ValueError("source must be provided.")
        cmd = f':AWG{ch}:ARBitrary:LOAd:WAVEform "{source}"' if ':/' in source else f':AWG{ch}:ARBitrary:LOAd:WAVEform {source}'
        self.write(cmd)
