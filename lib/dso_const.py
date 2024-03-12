# Name: dso_const.py
#
# Description: Define some useful DSO parameters.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

"""Definition of some useful DSO parameters.

These parameters are referenced by DSO-related modules when needed.

Typical usage example:
    from dso_const import *
    
"""

kCH1, kCH2, kCH3, kCH4 = range(1, 5)
kREF1, kREF2, kREF3, kREF4 = range(10, 14)
kMATH1 = 20
try: 
    from micropython import const
    kMATH1 = const(20)
except ImportError:
    pass

kANALOGx = { kCH1 : 'CH1', kCH2 : 'CH2', kCH3 : 'CH3', kCH4 : 'CH4' }
kREFx = { kREF1 : 'REF1', kREF2 : 'REF2', kREF3 : 'REF3', kREF4 : 'REF4' }
kMATHx = { kMATH1 : 'MATH', } 

kANALOGx_DEF = kANALOGx[ kCH1 ]
kREFx_DEF = kREFx[ kREF1 ]
kMATHx_DEF = kMATHx[ kMATH1 ]