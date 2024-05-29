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
        """Queries the trigger frequency.

        Returns:
            float: frequency
        """
        ret = self.query(':TRIGger:FREQuency?')
        return float(ret)

    def type(self) -> str:
        """Queries the trigger type.

        Returns:
            str: EDGE|DELAY|PULSEWIDTH|VIDEO|RUNT|RISEFALL|LOGIC|BUS|TIMEOUT
        """
        cmd=':TRIG:TYP?\n'
        ret = self.query(cmd)
        return ret

    def set_type(self, type:str):
        """Sets the trigger type.

        Args:
            type (str): EDGe|DELay|PULSEWidth|VIDeo|RUNT|RISEFall|LOGic|BUS|TIMEOut
        """
        cmd=':TRIG:TYP %s\n'%type
        self.write(cmd)

    def source(self) -> str:
        """Queries the trigger source.

        Returns:
            str: CH1|CH2|CH3|CH4|EXT|LINE|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15
        """
        cmd=':TRIG:SOUR?\n'
        ret = self.query(cmd)
        return ret

    def set_source(self, src:str):
        """Sets the trigger source.

        Args:
            src (str): CH1|CH2|CH3|CH4|EXT|LINe|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15
        """
        cmd=':TRIG:SOUR %s\n'%src
        self.write(cmd)

    def mode(self) -> str:
        """Queries the trigger mode.

        Returns:
            str: AUTO|NORMAL
        """
        cmd=':TRIG:MOD?\n'
        ret = self.query(cmd)
        return ret

    def set_mode(self, mode:str):
        """Sets the trigger mode.

        Args:
            mode (str): AUTo|NORMal
        """
        cmd=':TRIG:MOD %s\n'%mode
        self.write(cmd)

    def coupling(self) -> str:
        """Queries the trigger coupling.

        Returns:
            str: DC|AC|HF|LF
        """
        cmd=':TRIG:COUP?\n'
        ret = self.query(cmd)
        return ret

    def set_coupling(self, mode:str):
        """Sets the trigger coupling.

        Args:
            mode (str): DC|AC|HF|LF
        """
        cmd=':TRIG:COUP %s\n'%mode
        self.write(cmd)


    def slope(self) -> str:
        """Queries the edge/delay/rise&fall trigger slope.

        Returns:
            str: RISE|FALL|EITHER
        """
        trig_type = self.type()
        if trig_type.lower() in ['edge', 'delay', 'risefall']:
            cmd=':TRIG:%s:SLOP?\n'%trig_type
            ret = self.query(cmd)
            return ret
        else:
            return 'Unsupported trigger type for slope query: %s' % trig_type

    def set_slope(self, type:str):
        """Sets the edge/delay/rise&fall trigger slope.

        Args:
            type (str): RISe|FALL|EITher
        """
        trig_type = self.type()
        if trig_type.lower() in ['edge', 'delay', 'risefall']:
            cmd=':TRIG:%s:SLOP %s\n'%(trig_type,type)
            self.write(cmd)

    def polarity(self) -> str:
        """Queries the pulse width/runt/video trigger polarity.

        Returns:
            str: POSITIVE|NEGATIVE
        """
        trig_type = self.type()
        if trig_type.lower() in ['pulsewidth', 'runt', 'video']:
            cmd=':TRIG:%s:POL?\n'%trig_type
            ret = self.query(cmd)
            return ret
        else:
            return 'Unsupported trigger type for polarity query: %s' % trig_type

    def set_polarity(self, type:str):
        """Sets the pulse width/runt/video trigger polarity.

        Args:
            type (str): POSitive|NEGative
        """
        trig_type = self.type()
        if trig_type.lower() in ['pulsewidth', 'runt', 'video']:
            cmd=':TRIG:%s:POL %s\n'%(trig_type,type)
            self.write(cmd)

    def level(self) -> float:
        """Queries the trigger level.        
           Note: Not applicable to Pulse Runt and Rise & Fall triggers.

        Returns:
            float: trigger level
        """
        cmd=':TRIG:LEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_level(self, value:float):
        """Sets the trigger level.
           Note: Not applicable to Pulse Runt and Rise & Fall triggers.

        Args:
            value (float): trigger level
        """
        cmd=':TRIG:LEV %f\n'%value
        self.write(cmd)


    def hlevel(self) -> float:
        """Queries the high trigger level.        
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Returns:
            float: trigger high level
        """
        cmd=':TRIG:HLEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_hlevel(self, value:float):
        """Sets the high trigger level.
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Args:
            value (float): trigger high level
        """
        cmd=':TRIG:HLEV %f\n'%value
        self.write(cmd)
        
    def llevel(self) -> float:
        """Queries the low trigger level.        
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Returns:
            float: trigger low level
        """
        cmd=':TRIG:LLEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_llevel(self, value:float):
        """Sets the low trigger level.
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Args:
            value (float): trigger low level
        """
        cmd=':TRIG:LLEV %f\n'%value
        self.write(cmd)


    def external_probe_ratio(self) -> float:
        """Queries the external probe ratio.

        Returns:
            float: external probe ratio
        """
        cmd=':TRIG:EXTER:PROB:RAT?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_external_probe_ratio(self, value:float):
        """Sets the external probe ratio.

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
        """Sets noise rejection on.
        """
        cmd = ':TRIGger:NREJ ON'
        self.write(cmd)

    def set_noise_rejection_off(self):
        """Sets noise rejection off.
        """
        cmd = ':TRIGger:NREJ OFF'
        self.write(cmd)

    def holdoff(self) -> float:
        """Queries the holdoff time.

        Returns:
            float: holdoff time
        """
        cmd = ':TRIGger:HOLDoff?'
        ret = self.query(cmd)
        return float(ret)

    def set_holdoff(self, value:float):
        """Sets the holdoff time.

        Args:
            value (float): holdoff time
        """
        cmd = ':TRIGger:HOLDoff %f'%(value)
        self.write(cmd)
