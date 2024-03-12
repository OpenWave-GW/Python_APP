# Name: dso_channel.py
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

class Channel():
    """This module can control the Channel Vertical function on your DSO
    """
    def __init__(self, parent, vernier:bool=False) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

        self.is_support = parent.is_ch_support
        self.vernier = vernier

    def is_on(self, ch:int) -> bool:
        if self.is_support(ch):
            cmd=':CHAN%d:DISP?\n'%ch
            ret = self.query(cmd)
            if('ON' in ret):
                return True
            else:
                return False
        else:
            return False

    def set_on(self, ch:int):
        """Set channel to ON

        Args:
            ch (int): channel number
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHAN%d:DISP ON\n'%ch
        self.write(cmd)

    def set_off(self, ch:int):
        """Set channel to OFF

        Args:
            ch (int): channel number
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHAN%d:DISP OFF\n'%ch
        self.write(cmd)

    def get_scale(self, ch:int) -> float:
        """Get channel scale

        Args:
            ch (int): channel number

        Returns:
            float: scale value
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd=':CHAN%d:SCAL?\n'%ch
        ret = self.query(cmd)
        return float(ret)

    def set_scale(self, ch:int, scale:float):
        """Set channel scale

        Args:
            ch (int): channel number
            scale (float): scale value
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHAN%d:SCAL %f\n'%(ch,scale)
        self.write(cmd)

    def get_pos(self, ch:int) -> float:
        """Get channel position

        Args:
            ch (int): channel number

        Returns:
            float: position
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd=':CHAN%d:POS?\n'%ch
        ret = self.query(cmd)
        return float(ret)     

    def set_pos(self, ch:int, vpos:float):
        """Set channel position

        Args:
            ch (int): channel number
            vpos (float): position
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHAN%d:POS %f\n'%(ch,vpos)
        self.write(cmd)

    def get_bandwidth(self, ch:int):
        """Get channel bandwidth

        Args:
            ch (int): channel number

        Returns:
            str or float: bandwidth
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd=':CHANnel%d:BWLimit?\n'%(ch)
        ret = self.query(cmd)
        if 'FULL' in ret:
            return ret
        else:
            return float(ret)

    def set_bandwidth(self, ch:int, value):
        """Set channel bandwidth

        Args:
            ch (int): channel number
            value (str or float): FULL or bandwidth value
        """
        if self.is_support(ch):
            pass
        else:
            return
        if(isinstance(value,str)):
            cmd=':CHANnel%d:BWLimit %s\n'%(ch,value)
        else:
            cmd=':CHANnel%d:BWLimit %f\n'%(ch,value)
        self.write(cmd)

    def get_deskew(self, ch:int) -> float:
        """Get channel deskew

        Args:
            ch (int): channel number

        Returns:
            float: deskew
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd=':CHANnel%d:DESKew?\n'%(ch)
        ret = self.query(cmd)
        return float(ret)

    def set_deskew(self, ch:int, value:float):
        """Set channel deskew

        Args:
            ch (int): channel number
            value (float): deskew
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHANnel%d:DESKew %f\n'%(ch, value)
        self.write(cmd)

    def get_probe_ratio(self, ch:int) -> float:
        """Get channel probe ratio

        Args:
            ch (int): channel number

        Returns:
            float: probe ratio
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd=':CHAN%d:PROB:RAT?\n'%ch
        ret = self.query(cmd)
        return float(ret)

    def set_probe_ratio(self, ch:int, ratio:float):
        """Set channel probe ratio

        Args:
            ch (int): channel number
            ratio (float): probe ratio
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHAN%d:PROB:RAT %f\n'%(ch,ratio)
        self.write(cmd)

    def get_probe_type(self, ch:int) -> str:
        """

        Args:
            ch (int): channel number

        Returns:
            str: voltage or current
        """
        cmd=':CHAN%d:PROB:TYP?\n'%ch
        ret = self.query(cmd)
        return ret

    def set_probe_type(self, ch:int, type:str):
        """

        Args:
            ch (int): channel number
            type (str): voltage or current
        """
        cmd=':CHAN%d:PROB:TYP %s\n'%(ch,type)
        self.write(cmd)

    def get_coupling(self, ch:int) -> str:
        """

        Args:
            ch (int): channel number

        Returns:
            str: DC, AC or GND
        """
        cmd=':CHAN%d:COUP?\n'%ch
        ret = self.query(cmd)
        return ret

    def set_coupling(self, ch:int, mode:str):
        """

        Args:
            ch (int): channel number
            mode (str): DC, AC or GND
        """
        cmd=':CHAN%d:COUP %s\n'%(ch,mode)
        self.write(cmd)

    def get_expend(self, ch:int) -> str:
        """Queries the Expand status of a channel.

        Args:
            ch (int): channel number

        Returns:
            str: Expand status of a channel
        """
        cmd = ':CHANnel%d:EXPand?\n'%(ch)
        ret = self.query(cmd)
        return ret
    
    def set_expend(self, ch:int, expend:str):
        """Sets Expand from ground or from center for a channel.

        Args:
            ch (int): channel number
            expend (str):

                GND : Expand by ground
                
                CENTer : Expand by center
        """
        cmd = ':CHANnel%d:EXPand %s\n'%(ch, expend)
        self.write(cmd)

    def get_impedance(self, ch:int) -> int:
        """Get channel impedance

        Args:
            ch (int): channel number

        Returns:
            int: impedance value
        """
        if self.is_support(ch):
            pass
        else:
            return 0
        cmd = ':CHANnel%d:IMPedance?\n'%(ch)
        ret = self.query(cmd)
        return int(float(ret))

    def set_impedance(self, ch:int, value:float):
        """Set channel impedance

        Args:
            ch (int): channel number
            value (float): impedance value
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd = ':CHANnel%d:IMPedance %f\n'%(ch, value)
        self.write(cmd)

    def is_invert(self, ch:int) -> bool:
        if self.is_support(ch):
            pass
        else:
            return False
        cmd = ':CHANnel%d:INVert?\n'%(ch)
        ret = self.query(cmd)
        if 'ON' in ret:
            return True
        else:
            return False

    def set_invert_on(self, ch:int):
        """Set channel invert to ON

        Args:
            ch (int): channel number
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd = ':CHANnel%d:INVert ON\n'%(ch)
        self.write(cmd)

    def set_invert_off(self, ch:int):
        """Set channel invert to OFF

        Args:
            ch (int): channel number
        """
        if self.is_support(ch):
            pass
        else:
            return
        cmd = ':CHANnel%d:INVert OFF\n'%(ch)
        self.write(cmd)

    def is_vernier(self, ch:int) -> bool:
        """Check the adjustment mode of vertical scale.

        .. note:: Invalid in some models.

        Args:
            ch (int): channel number

        Raises:
            ValueError: Invalid for this model

        Returns:
            bool: True or False
        """
        if self.vernier:
            pass
        else:
            raise ValueError('Invalid for this model.')
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHANnel%d:VERNier?\n'%ch
        ret = self.query(cmd)
        if 'ON' in ret:
            return True
        else:
            return False

    def set_vernier_on(self, ch:int) -> bool:
        """Set the adjustment mode of vertical scale to ON.

        .. note:: Invalid in some models.

        Args:
            ch (int): channel number

        Raises:
            ValueError: Invalid for this model

        Returns:
            bool: True or False
        """
        if self.vernier:
            pass
        else:
            raise ValueError('Invalid for this model.')
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHANnel%d:VERNier ON\n'%ch
        self.write(cmd)

    def set_vernier_off(self, ch:int) -> bool:
        """Set the adjustment mode of vertical scale to OFF.

        .. note:: Invalid in some models.

        Args:
            ch (int): channel number

        Raises:
            ValueError: Invalid for this model

        Returns:
            bool: True or False
        """
        if self.vernier:
            pass
        else:
            raise ValueError('Invalid for this model.')
        if self.is_support(ch):
            pass
        else:
            return
        cmd=':CHANnel%d:VERNier OFF\n'%ch
        self.write(cmd)