# Name: dso2kp.py
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

import dso_basic
import dso_channel
import dso_timebase
import dso_trigger
import dso_acquire
import dso_ref
import dso_hardcopy
import dso_draw
import dso_awg
import dso_meas
import dso_math
import dso_spectrum
import dso_dmm
import dso_display
import dso_gonogo
import dso_power_supply
try:
    import dso_colors as color
except:
    pass

class Dso(dso_basic.DsoBasic):
    """This module can control MPO2000

    The general control functions can be found in :class:`.DsoBasic`

    **Extend methods as below:**
    """
    def __init__(self):
        super().__init__()
        self.channel=dso_channel.Channel(self)
        """Find Channel Vertical control in :class:`.Channel`
        """
        self.timebase=dso_timebase.TimeBase(self)
        """Find Horizontal control in :class:`.TimeBase`
        """
        self.trigger=dso_trigger.Trigger(self)
        """Find Trigger control in :class:`.Trigger`
        """
        self.acquire=dso_acquire.Acquire(self)
        """Find Acquire control in :class:`.Acquire`
        """
        self.ref=dso_ref.Ref(self)
        """Find Reference control in :class:`.Ref`
        """
        self.hardcopy=dso_hardcopy.HardCopy(self)
        """Find HardCopy control in :class:`.HardCopy`
        """
        self.meas = dso_meas.Measure(self)
        """Find Measure control in :class:`.Measure`
        """
        self.math = dso_math.Math(self)
        """Find Math control in :class:`.Math`
        """
        self.sa = dso_spectrum.Spectrum(self, max_instances=2)
        """Find Spectrum control in :class:`.Spectrum`
        """
        self.dmm = dso_dmm.Dmm(self)
        """Find Dmm control in :class:`.Dmm`
        """
        self.display = dso_display.Display(self)
        """Find Display control in :class:`.Display`
        """
        self.gonogo = dso_gonogo.GoNoGo(self)
        """Find GoNoGo control in :class:`.GoNoGo`
        """
        self.dsodraw=dso_draw.Draw(self)#:It's :class:`.Draw`
        self.awg=dso_awg.Awg(self)#:The AWG control is in :class:`.Awg`
        
        self.power=dso_power_supply.PowerSupply(self)
        """Find Power Supply control in :class:`.PowerSupply`
        """
        

class Screen(dso_basic.ScreenBasic):
    """This DSO's screen information.
    """
    def __init__(self) -> None:
        super().__init__()

class Theme(dso_basic.ThemeBasic):
    """This DSO's color theme.
    """
    def __init__(self, dark_mode=True) -> None:
        super().__init__()
        try:
            if dark_mode:
                self.bg_color = color.DKGRAY
                self.grid_color = color.GRAY
                self.text_color = color.LTGRAY
            else:
                self.bg_color = color.WHITE
                self.grid_color = color.BLACK
                self.text_color = color.BLACK
        except:
            pass

