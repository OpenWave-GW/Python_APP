# Name: dso_dmm.py
#
# Description: Perform DMM operations on the DSO.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import time
class Dmm():
    """This module can control the DMM function on your DSO

    """
    def __init__(self, parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

    def is_on(self) -> bool:
        """Is DMM's state on?

        Returns:
            bool: True or False
        """
        cmd = ':DMM:STATE?\n'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_on(self):
        """Set DMM ON

        """
        cmd = ':DMM:STATE ON\n'
        self.write(cmd)

    def set_off(self):
        """Set DMM OFF
        """
        cmd = ':DMM:STATE OFF\n'
        self.write(cmd)


    def set_mode_ACV(self, range=None):
        """Set DMM's mode as ACV

        Args:
            range (int or str): Set measurement range as 5,50,750 or AUTO
        """
        cmd = ':DMM:MODe ACV\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' %range
            else:
                cmd = ':DMM:MODe:RANGe %d\n' %range
            self.write(cmd)

    def set_mode_DCV(self, range=None):
        """Set DMM's mode as DCV

        Args:
            range (int or str): Set measurement range as 5,50,500,1000 or AUTO
        """
        cmd = ':DMM:MODe DCV\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %d\n' % range
            self.write(cmd)

    def set_mode_ACmV(self, range=None):
        """Set DMM's mode as ACmV

        Args:
            range (float or str): Set measurement range as 0.5,0.05 or AUTO
        """
        cmd = ':DMM:MODe ACMV\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %f\n' % range
            self.write(cmd)

    def set_mode_DCmV(self, range=None):
        """Set DMM's mode as DCmV

        Args:
            range (float or str): Set measurement range as 0.5,0.05 or AUTO
        """
        cmd = ':DMM:MODe DCMV\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %f\n' % range
            self.write(cmd)

    def set_mode_ACmA(self, range=None):
        """Set DMM's mode as ACmA

        Args:
            range (float or str): Set measurement range as 0.5,0.05 or AUTO
        """
        cmd = ':DMM:MODe ACMA\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %f\n' % range
            self.write(cmd)

    def set_mode_DCmA(self, range=None):
        """Set DMM's mode as DCmA

        Args:
            range (float or str): Set measurement range as 0.5,0.05 or AUTO
        """
        cmd = ':DMM:MODe DCMA\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %f\n' % range
            self.write(cmd)

    def set_mode_ACA(self):
        """Set DMM's mode as ACA

        """
        cmd = ':DMM:MODe ACA\n'
        self.write(cmd)

    def set_mode_DCA(self):
        """Set DMM's mode as DCA

        """
        cmd = ':DMM:MODe DCA\n'
        self.write(cmd)

    def set_mode_ohm(self, range=None):
        """Set DMM's mode as ohm

        Args:
            range (int or str): Set measurement range as 50,500,5000,50000,500000,5000000,50000000 or AUTO
        """
        cmd = ':DMM:MODe OHM\n'
        self.write(cmd)
        time.sleep_ms(100)
        if range is not None:
            if (isinstance(range, str)):
                cmd = ':DMM:MODe:RANGe %s\n' % range
            else:
                cmd = ':DMM:MODe:RANGe %d\n' % range
            self.write(cmd)

    def set_mode_diode(self):
        """Set DMM's mode as diode

        """
        cmd = ':DMM:MODe DIODE\n'
        self.write(cmd)

    def set_mode_beep(self):
        """Set DMM's mode as beep

        """
        cmd = ':DMM:MODe BEEP\n'
        self.write(cmd)

    def set_mode_temperature(self, type:str=None, units:str=None, sim:float=None):
        """Set DMM's mode as temperature

        Args:
            type (str): TYPEB, TYPEE, TYPEJ, TYPEK, TYPEN, TYPER, TYPES, TYPET
            units (str): The unit of temperature display. C or F.
            sim (float): Set the measurement temperature.
        """
        cmd = ':DMM:MODe TEMPerature\n'
        self.write(cmd)
        time.sleep_ms(100)
        if type is not None:
            cmd = ':DMM:TEMPerature:TYPe %s\n' % type
            self.write(cmd)
        if units is not None:
            cmd = ':DMM:TEMPerature:UNITs %s\n' % units
            self.write(cmd)
        if sim is not None:
            cmd = ':DMM:TEMPerature:SIM %f\n' % sim
            self.write(cmd)

    def set_maxmin_on(self):
        """Set max/min function on.

        """
        cmd = ':DMM:MMIN ON\n'
        self.write(cmd)

    def set_maxmin_off(self):
        """Set max/min function off.

        """
        cmd = ':DMM:MMIN OFF\n'
        self.write(cmd)

    def set_hold_on(self):
        """Set DMM hold on.

        """
        cmd = ':DMM:HOLD ON\n'
        self.write(cmd)

    def set_hold_off(self):
        """Set DMM hold off.

        """
        cmd = ':DMM:HOLD OFF\n'
        self.write(cmd)

    def is_hold(self) -> bool:
        """Is DMM hold on?

        Returns:
            bool: True or False
        """
        cmd = ':DMM:HOLD?\n'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def get_value(self) :
        """Get the DMM's measurement result.

        Returns:
            float or str: The measurement value, 'OL' or '-OL'.
        """
        cmd = ':DMM:VALue?\n'
        ret = self.query(cmd)
        try:
            return float(ret)
        except:
            return ret

