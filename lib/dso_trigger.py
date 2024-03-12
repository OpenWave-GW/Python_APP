# Name: dso_trigger.py
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

class Trigger():
    """This module can control the Trigger function on your DSO
    """
    def __init__(self, parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

    def freq(self) -> float:
        """Current frequency counter.

        Returns:
            float: frequency
        """
        ret = self.query(':TRIGger:FREQuency?')
        return float(ret)

    def type(self) -> str:
        """Current trigger type.

        Returns:
            str: edge, delay, pulse, video, runt, risefall, bus, logic or timeout
        """
        cmd=':TRIG:TYP?\n'
        ret = self.query(cmd)
        return ret

    def set_type(self, type:str):
        """Set trigger type.

        Args:
            type (str): edge, delay, pulse, video, runt, risefall, bus, logic or timeout
        """
        cmd=':TRIG:TYP %s\n'%type
        self.write(cmd)

    def source(self) -> str:
        """Current trigger source.

        Returns:
            str: trigger source
        """
        cmd=':TRIG:SOUR?\n'
        ret = self.query(cmd)
        return ret

    def set_source(self, src:str):
        """Set trigger source

        Args:
            src (str): CH1|CH2|CH3|CH4|EXT|LINe|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15
        """
        cmd=':TRIG:SOUR %s\n'%src
        self.write(cmd)

    def mode(self) -> str:
        """Current trigger mode.

        Returns:
            str: AUTo|NORMal
        """
        cmd=':TRIG:MOD?\n'
        ret = self.query(cmd)
        return ret

    def set_mode(self, mode:str):
        """Set trigger mode.

        Args:
            mode (str): AUTo|NORMal
        """
        cmd=':TRIG:MOD %s\n'%mode
        self.write(cmd)

    def coupling(self) -> str:
        """Current trigger coupling

        Returns:
            str: DC|AC|HF|LF
        """
        cmd=':TRIG:COUP?\n'
        ret = self.query(cmd)
        return ret

    def set_coupling(self, mode:str):
        """Set trigger coupling.

        Args:
            mode (str): DC|AC|HF|LF
        """
        cmd=':TRIG:COUP %s\n'%mode
        self.write(cmd)

    def level(self) -> float:
        """Current trigger level

        Returns:
            float: trigger level
        """
        cmd=':TRIG:LEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_level(self, value:float):
        """Set trigger level

        Args:
            value (float): trigger level
        """
        cmd=':TRIG:LEV %f\n'%value
        self.write(cmd)

    def external_probe_ratio(self) -> float:
        """Current external probe ratio

        Returns:
            float: external probe ratio
        """
        cmd=':TRIG:EXTER:PROB:RAT?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_external_probe_ratio(self, value:float):
        """Set external probe ratio

        Args:
            value (float): external probe ratio
        """
        cmd=':TRIG:EXTER:PROB:RAT %f\n'%value
        self.write(cmd)

    def is_noise_rejection(self) -> bool:
        cmd = ':TRIGger:NREJ?'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_noise_rejection_on(self):
        """Set trigger noise rejection ON.
        """
        cmd = ':TRIGger:NREJ ON'
        self.write(cmd)

    def set_noise_rejection_off(self):
        """Set trigger noise rejection OFF.
        """
        cmd = ':TRIGger:NREJ OFF'
        self.write(cmd)

    def holdoff(self) -> float:
        """Current holdoff time.

        Returns:
            float: holdoff time
        """
        cmd = ':TRIGger:HOLDoff?'
        ret = self.query(cmd)
        return float(ret)

    def set_holdoff(self, value:float):
        """Set holdoff time.

        Args:
            value (float): holdoff time
        """
        cmd = ':TRIGger:HOLDoff %f'%(value)
        self.write(cmd)