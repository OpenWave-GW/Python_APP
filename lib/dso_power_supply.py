# Name: dso_power_supply.py
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

class PowerSupply():
    """This module can control the Power Supply function on your DSO
    
    """
    def __init__(self,parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI
        
    def is_on(self, ch:int) -> bool:
        """Check the Power Supply output# is ON or not.

        Args:
            ch (int): Power Supply output#

        Returns:
            bool: True or False
        """
        cmd=':POWERSupply:OUTPut%d?'%ch
        ret=self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False
    
    def set_on(self, ch:int):
        """Set Power Supply output# ON

        Args:
            ch (int): Power Supply output#
        """
        cmd=':POWERSupply:OUTPut%d ON'%ch
        self.write(cmd)

    def set_off(self, ch:int):
        """Power Supply output# OFF

        Args:
            ch (int): Power Supply output#
        """
        cmd=':POWERSupply:OUTPut%d OFF'%ch
        self.write(cmd)

    def get_voltage(self, ch:int) -> float:
        """Get Power Supply output# voltage

        Args:
            ch (int): Power Supply output#

        Returns:
            float: voltage
        """
        cmd=':POWERSupply:OUTPut%d:VOLTage?'%ch
        ret=self.query(cmd)
        return float(ret)

    def set_voltage(self, ch:int, volt:float):
        """Set Power Supply output# voltage

        Args:
            ch (int): Power Supply output#
            volt (float): voltage
        """
        cmd=':POWERSupply:OUTPut%d:VOLTage %f'%(ch,volt)
        self.write(cmd)
        
    def check_ocp(self, ch:int) -> bool:
        """Returns the power supply OCP status.
        
        Args:
            ch (int): Power Supply output#
        
        Returns:
            bool: True or False
        """
        cmd=f':POWERSupply:OUTPut{ch}:OCP?'
        ret=self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def clear_ocp(self, ch:int):
        """Reconfigure the power supply when OCP occured

        Args:
            ch (int): Power Supply output#
        """
        cmd=f':POWERSupply:OUTPut{ch}:RECONFigure ON'
        self.write(cmd)
