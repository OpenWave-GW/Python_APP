# Name: dso_gonogo.py
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

class GoNoGo():
    """This module can control the GoNoGo function on your DSO

    """
    def __init__(self,parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

    def clear(self):
        """Clears the Go/NoGo counter.

        """
        cmd = ':GONogo:CLEar\n'
        self.write(cmd)

    def is_execute(self) -> bool:
        """Is Go/NoGo execute?

        Returns:
            bool: True or False
        """
        cmd = ':GONogo:EXECute?\n'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def execute_on(self):
        """Enables Go/NoGo.

        """
        cmd = ':GONogo:EXECute ON\n'
        self.write(cmd)

    def execute_off(self):
        """Disables Go/NoGo.

        """
        cmd = ':GONogo:EXECute OFF\n'
        self.write(cmd)

    def function_initial(self):
        """Initializes the Go/NoGo APP. This must be run after the Go/NoGo APP has been started.

        """
        cmd = ':GONogo:FUNCtion\n'
        self.write(cmd)

    def ngcount(self) -> str:
        """
        Returns:
            str: the Go/NoGo counter.
        """
        cmd = 'GONogo:NGCount?\n'
        ret = self.query(cmd)
        return ret  
    
    def when(self) -> str:
        """Now Go/NoGo “When” conditions.

        Returns: 
            str: EXITs|ENTers
        """
        cmd = ':GONogo:NGDefine?\n'
        ret = self.query(cmd)
        return ret

    def set_when_exits(self):
        """Sets exits as the when condition of Go/NoGo.

        """
        cmd = ':GONogo:NGDefine EXITs\n'
        self.write(cmd)

    def set_when_enters(self):
        """Sets enters as the when condition of Go/NoGo.

        """
        cmd = ':GONogo:NGDefine ENTers\n'
        self.write(cmd)

    def source(self) -> str:
        """Now the source for the Go/NoGo signal.

        Returns:
            str: CH1|CH2|CH3|CH4
        """
        cmd = ':GONogo:SOURce?\n' 
        ret = self.query(cmd)
        return ret

    def set_source(self, ch:int):
        """Sets the source for the Go/NoGo signal.

        Args:
            ch (int): 1:CH1, 2:CH2, 3:CH3, 4:CH4.
        """
        cmd = ':GONogo:SOURce CH%d\n' %ch
        ret = self.write(cmd)

    def violation(self) -> str:
        """Now action for the Go/NoGo violation.

        Returns:
            str: STOP|STOP_Beep|CONTinue|CONTINUE_Beep
        """
        cmd = ':GONogo:VIOLation?\n'
        ret = self.query(cmd)
        return ret

    def set_violation(self, action:str):
        """Sets action for the Go/NoGo violation.

        Args:
            action (str): STOP|STOP_Beep|CONTinue|CONTINUE_Beep
        """
        cmd = ':GONogo:VIOLation %s\n' %action
        self.write(cmd)  
             
    def is_script_on(self) -> bool:
        """Is Go/NoGo APP on?

        Returns:
            bool: True or False
        """
        cmd = ':GONogo:SCRipt?\n'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_script_on(self):
        """Activates Go/NoGo APP.

        """
        cmd = ':GONogo:SCRipt ON\n'
        self.write(cmd)


    def set_script_off(self):
        """Deactivates Go/NoGo APP.

        """
        cmd = ':GONogo:SCRipt OFF\n'
        self.write(cmd)        

    def template_mode(self) -> str:
        """Now Go/NoGo template mode.

        Returns: 
            str: MAXimum|MINimum|AUTO
        """
        cmd = ':TEMPlate:MODe?\n'
        ret = self.query(cmd)
        return ret

    def set_template_mode(self, mode:str):
        """Sets the Go/NoGo template mode.

        Args:
            mode (str): MAXimum|MINimum|AUTO
        """
        cmd = ':TEMPlate:MODe %s\n' %mode
        self.write(cmd)

    def template_maximum(self) -> str:
        """Queries which waveform memory (REF1 or W1~W20) is set to the maximum template. 

        Returns:
            str: REF1|W1~W20
        """
        cmd = ':TEMPlate:MAXimum?\n'
        ret = self.query(cmd)
        return ret

    def set_template_maximum(self, waveform:str):
        """Defines which waveform memory (REF1 or W1~W20) is set to the maximum template.

        Args:
            waveform (str): REF1|W1~W20
        """   
        cmd = ':TEMPlate:MAXimum %s\n' %waveform
        self.write(cmd)

    def template_minimum(self) -> str:
        """Queries which waveform memory (REF1 or W1~W20) is set to the minimum template. 

        Returns:
            str: REF2|W1~W20
        """
        cmd = ':TEMPlate:MINimum?\n'
        ret = self.query(cmd)
        return ret

    def set_template_minimum(self, waveform:str):
        """Defines which waveform memory (REF1 or W1~W20) is set to the minimum template.

        Args:
            waveform (str): REF2|W1~W20
        """   
        cmd = ':TEMPlate:MINimum %s\n' %waveform
        self.write(cmd)    

    def get_template_position_maximum(self) -> str:
        """Queries the position of the maximum template. 

        Returns:
            str: Desired template position (-12.0 ~ +12.0 divisions)
        """
        cmd = ':TEMPlate:POSition:MAXimum?\n'
        ret = self.query(cmd)
        return ret

    def set_template_position_maximum(self, position:float):
        """Sets the position of the maximum template.

        Args:
            position (float): Desired template position (-12.0 ~ +12.0) divisions
        """
        cmd = ':TEMPlate:POSition:MAXimum %f\n' %position
        self.write(cmd)

    def get_template_position_minimum(self) -> str:
        """Queries the position of the minimum template. 

        Returns:
            str: Desired template position (-12.0 ~ +12.0 divisions)
        """
        cmd = ':TEMPlate:POSition:MINimum?\n'
        ret = self.query(cmd)
        return ret

    def set_template_position_minimum(self, position:float):
        """Sets the position of the minimum template.

        Args:
            position (float): Desired template position (-12.0 ~ +12.0) divisions
        """
        cmd = ':TEMPlate:POSition:MINimum %f\n' %position
        self.write(cmd)

    def save_template_maximum(self):
        """Saves the maximum template.

        """
        cmd = ':TEMPlate:SAVe:MAXimum\n'
        self.write(cmd)

    def save_template_minimum(self):
        """Saves the minimum template.
        
        """
        cmd = ':TEMPlate:SAVe:MINimum\n'
        self.write(cmd)
        
    def get_template_tolerance(self) -> str:
        """Queries the tolerance as a percentage.

        Returns:
            str: The auto tolerance range (0.4% ~ 40%)
        """
        cmd = ':TEMPlate:TOLerance?\n'
        ret = self.query(cmd)
        return ret

    def set_template_tolerance(self, tolerance:float):
        """Sets the tolerance as a percentage.

        Args:
            tolerance (float): The auto tolerance range (0.4 ~ 40) %
        """
        cmd = ':TEMPlate:TOLerance %f\n' %tolerance
        self.write(cmd)

    def save_template_auto(self):
        """Saves the AUTO template.

        """
        cmd = ':TEMPlate:SAVe:AUTo\n'
        self.write(cmd)

    def is_output_on(self) -> bool:
        """Is Go/NoGo output on?

        Returns:
            bool: True or False
        """
        cmd = ':GONogo:OUTPut?\n'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def output_on(self):
        """Sets Go/NoGo output on.

        """
        cmd = ':GONogo:OUTPut ON\n'
        self.write(cmd)

    def output_off(self):
        """Sets Go/NoGo output off.

        """
        cmd = ':GONogo:OUTPut OFF\n'
        self.write(cmd)