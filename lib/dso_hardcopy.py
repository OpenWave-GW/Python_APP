# Name: dso_hardcopy.py
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

class HardCopy():
    """This module can use the hardcopy function on your DSO.
    """
    def __init__(self,parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI
        
    def hard_copy(self, ifmt:str='PNG', ink_saver:str='OFF', wfmt:str='LSF', mode:str='IMAGe'):
        """Hardcopy on your DSO.

        Args:
            ifmt (str, optional): Image save file type PNG or BMP. Defaults to 'PNG'.
            ink_saver (str, optional): Inksaver ON or OFF. Defaults to 'OFF'.
            wfmt (str, optional): Waveform File Format, including LSF, DCSV and FCSV. Defaults to 'LSF'
            mode (str, optional): IMAGe, WAVEform, SETUp or ALL. Defaults to 'IMAGe'.
        """
        self.write(':HARDcopy:MODe SAVE')
        if mode == 'IMAGe' or mode == 'ALL':
            self.write(':HARDcopy:SAVEFORMat '+ifmt)
            self.write(':HARDcopy:SAVEINKSaver '+ink_saver)
        if mode == 'WAVEform' or mode == 'ALL':
            self.write(':SAVe:WAVEform:FILEFormat '+wfmt)
        self.write(':HARDcopy:ASSIGN '+mode)        
        self.write(':HARDcopy:START')