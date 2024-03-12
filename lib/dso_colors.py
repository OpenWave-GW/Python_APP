# Name: dso_colors.py
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

import lvgl as lv

# Code can be portable between 4-bit and other drivers by calling create_color
def MWRGB(r, g, b):
    idx = (r<<16) + (g<<8) + b
    return lv.color_hex(idx)

BLACK=MWRGB( 0  , 0  , 0   )#lv.color_black()
BLUE=MWRGB( 0  , 0  , 128 )
GREEN=MWRGB( 0  , 128, 0   )
CYAN=MWRGB( 0  , 128, 128 )
RED=MWRGB( 128, 0  , 0   )
MAGENTA=MWRGB( 128, 0  , 128 )
BROWN=MWRGB( 128, 64 , 0   )
LTGRAY=MWRGB( 192, 192, 192 )
#GRAY=MWRGB( 128, 128, 128 )
GRAY=MWRGB(  88,  88,  88 )
LTBLUE=MWRGB( 0  , 0  , 255 )
LTGREEN=MWRGB( 0  , 255, 0   )
LTCYAN=MWRGB( 0  , 255, 255 )
LTRED=MWRGB( 255, 0  , 0   )
LTMAGENTA=MWRGB( 255, 0  , 255 )
YELLOW=MWRGB( 255, 255, 0   )
WHITE=MWRGB( 255, 255, 255 )#lv.color_white()
'''other common colors'''
MIDGRAY=MWRGB( 100, 100, 100 )
DKGRAY=MWRGB( 32,  32,  32  )
ORANGERED=MWRGB( 255, 65 , 0   )

TRANSPARENT=MWRGB( 255, 255, 232 )
TRANSPARENT_1=MWRGB(  80,  80, 112 )#background
TRANSPARENT_2=MWRGB( 255, 128, 128 )#red
TRANSPARENT_3=MWRGB( 112, 124, 144 )#blue
TRANSPARENT_4=MWRGB( 255, 251, 240 )#graticule use only!!