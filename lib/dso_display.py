# Name: dso_display.py
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

class Display():
    """This module controls the display function on the DSO.
    """
    def __init__(self,parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI
    
    def set_persis_infi(self):
        """Sets the persistence to infinite        
        """
        cmd=':DISPlay:PERSistence INFInite'
        self.write(cmd)
    
    def set_persis_off(self):
        """Sets the persistence off
        """
        cmd=':DISPlay:PERSistence OFF'
        self.write(cmd)
    
    def persis_clear(self):
        """Clear the persistence of the displayed waveform
        """
        cmd=':DISPlay:PERSistence:CLEAR'
        self.write(cmd)

    def set_persis_time(self, t:float):
        """Sets the waveform persistence level

           Args:
               t(float): persistence time
               range: 16E-3, 30E-3, 60E-3, 120E-3, 240E-3, 500E-3, 1, 2, 4
        """
        cmd=f':DISPlay:PERSistence {t}'
        self.write(cmd)

    def get_persis_time(self):
        """Quries the waveform persistence level

        Returns:
            str or float: persistence time
        """
        cmd=':DISPlay:PERSistence?'
        ret=self.query(cmd)
        if 'INFInite'.upper() in ret:
            return ret
        elif 'OFF' in ret:
            return ret
        else:
            return float(ret)