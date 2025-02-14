# Name: asr.py
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

import dso_usb
import time

class Asr():
    """This module can control ASR-2100.

    It supports USB interface to use SCPI.

    It will scan available instruments on your DSO, then require a serial number to specify and connect to it.

    Usage:
    -------
    .. code-block:: python

        import asr
        inst = asr.Asr()
        inst.connect('<Instrument Serial Number>')
        print(inst.idn())
        inst.close()
    
    """
    def __init__(self) -> None:
        self.com = None
        self.ModelName = ''
        self.SerialNumber = ''
        self.scpi_delay = 0.1
        """SCPI delay.
        """

    def set_scpi_delay(self, delay:float) -> None:
        """Set the SCPI delay

        Args:
            delay (float): delay time
        """
        self.scpi_delay = delay
    
    def __fillModelInfo(self) -> None:
        ret = self.query('*idn?')
        self.ModelName = ret.split(',')[1]
        self.SerialNumber = ret.split(',')[2]

    def connect(self, SN:str, baudrate:int=115200, timeout:int=3) -> int:
        """Connect to the ASR.

        Args:
            SN (str): Serial Number is necessary.
            baudrate (int, optional): baudrate. Defaults to 115200.
            timeout (int, optional): timeout. Defaults to 3.

        Returns:
            int: 0 or -1
        """
        com = dso_usb.connect(SN, baudrate, timeout, self.scpi_delay)
        if com is None:
            return -1
        else:
            self.com = com
            self.__fillModelInfo()
            return 0

    def close(self) -> None:
        """
        Close the connection.
        """
        if self.com is None:
            return
        self.com.close()

    def write(self, cmd:str) -> None:
        """Write an SCPI command to the instrument.

        Args:
            cmd (str): SCPI command to be written.
        """
        if self.com is None:
            return
        if cmd[-1] == '\n':
            pass
        else:
            cmd += '\n'
        self.com.write(cmd)

    def readline(self) -> str:
        """Read a line from the instrument's communication port and return it as a string.

        Returns:
            str: The string read from the instrument.
        """
        tmp = b''
        while True:
            if self.com.in_waiting == 0:
                break
            try:
                tmp += self.com.read(1)
                if tmp.endswith(b'\n'):
                    break
            except:
                break
        str=tmp.decode()
        if(str == ''):
            return ''
        elif(str[-1] == '\n'):
            return str[:-1]
        else:
            return str

    def query(self, cmd:str) -> str:
        """Send a query SCPI command to the instrument and return the result.

        Args:
            cmd (str): SCPI command to be queried.

        Returns:
            str: Result of the SCPI command.
        """
        if self.com is None:
            return
        if cmd[-1] == '\n':
            pass
        else:
            cmd += '\n'
        self.write(cmd)
        time.sleep(self.scpi_delay)
        return self.readline()

    def idn(self) -> str:
        return self.query('*idn?')
    
    def opc(self) -> int:
        return self.query('*opc?')
    
    def get_crest_factor(self) -> float:
        """Returns the output current crest factor (CF).
        """
        return float(self.query(":MEASure:SCALar:CURRent:CFACtor?"))

    def get_imax(self) -> float:
        """Returns the output current maximum peak value (Imax) in amps.
        """
        return float(self.query(":MEASure:SCALar:CURRent:HIGH?"))

    def get_imin(self) -> float:
        """Returns the output current minimum peak value (Imin) in amps.
        """
        return float(self.query(":MEASure:SCALar:CURRent:LOW?"))

    def get_irms(self) -> float:
        """Returns the output current RMS (Irms) value in amps.
        """
        return float(self.query(":MEASure:SCALar:CURRent:RMS?"))

    def get_iavg(self) -> float:
        """Returns the output current average value (Iavg) in amps.
        """
        return float(self.query(":MEASure:SCALar:CURRent:AVERage?"))
    
    def get_frequency(self) -> float:
        """Returns the SYNC signal source frequency in Hz. (Only AC+DC-sync or AC-sync Active)
        """
        return float(self.query(":MEASure:SCALar:FREQuency?"))

    def get_apparent_power(self) -> float:
        """Returns the apparent power (S) in VA.
        """
        return float(self.query(":MEASure:SCALar:POWer:AC:APParent?"))

    def get_power_factor(self) -> float:
        """Returns the power factor (PF).
        """
        return float(self.query(":MEASure:SCALar:POWer:AC:PFACtor?"))

    def get_reactive_power(self) -> float:
        """Returns the reactive power (Q) in VAR.
        """
        return float(self.query(":MEASure:SCALar:POWer:AC:REACtive?"))

    def get_active_power(self) -> float:
        """Returns the active power (P) in Watts.
        """
        return float(self.query(":MEASure:SCALar:POWer:AC:REAL?"))

    def get_vrms(self) -> float:
        """Returns the voltage (Vrms).
        """
        return float(self.query(":MEASure:SCALar:VOLTage:RMS?"))

    def get_vavg(self) -> float:
        """Returns the voltage average value (Vavg) in volts.
        """
        return float(self.query(":MEASure:SCALar:VOLTage:AVERage?"))

    def get_vmax(self) -> float:
        """Returns the output voltage maximum peak value (Vmax) in volts.
        """
        return float(self.query(":MEASure:SCALar:VOLTage:HIGH?"))

    def get_vmin(self) -> float:
        """Returns the output voltage minimum peak value (Vmin) in volts.
        """
        return float(self.query(":MEASure:SCALar:VOLTage:LOW?"))

    def is_on(self) -> bool:
        """Get the output state of power source.
        """
        ret = self.query(":OUTPut?")
        if '1' in ret:
            return True
        else:
            return False

    def set_on(self) -> None:
        """Turns the output on.
        """
        self.write(":OUTPut ON")

    def set_off(self) -> None:
        """Turns the output off.

        """
        self.write(":OUTPut OFF")

    def set_output_pon(self, mode: str) -> None:
        """Set the output state at power-on.

            Args:
                mode (int, str): The output state to set at power-on. Acceptable values are:
                    0 or 'OFF' - Disabled
                    1 or 'ON' - Enabled
                    2 or 'SEQ' - Sequence function
                    3 or 'SIM' - Simulate function
        """
        self.write(f":OUTPut:PON {mode}")

    def clear_output_protection(self) -> None:
        """Clear output protection alarms.

            Description:
                This command clears alarms such as Over Current, Over Peak Current,
                Output Over-Power, Output Short, Output Overvoltage, and Sensing Voltage Error.
        """
        self.write(":OUTPut:PROTection:CLEar")

    def set_output_relay(self, state: str) -> None:
        """Sets the output relay of the power source.
        
        Args:
            state (str or int): 'ON' (1) to enable the output relay, 'OFF' (0) to disable.
        """
        self.write(f":OUTPut:RELay {state}")
    
    def set_test_mode(self, mode: str) -> None:
        """Sets the test mode for the power supply.
    
        Args:
            mode (str): The test mode to be set. Acceptable values are:
                - 'CONTinuous' or 0: Continuous mode (normal operating mode).
                - 'SEQuence' or 1: Sequence mode (available for AC+DC-INT, AC-INT, DC-INT modes).
                - 'SIMulation' or 2: Simulation mode (available only for AC+DC-INT mode).
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)
        
        if mode in ['SEQ', 'SEQuence', 1] and output_mode not in ['ACDC-INT', 'AC-INT', 'DC-INT']:
            raise ValueError(f"SEQuence is only allowed in modes: AC+DC-INT, AC-INT or DC-INT. Current output mode: {output_mode}")
        
        if mode in ['SIM', 'SIMulation', 2] and output_mode != 'ACDC-INT':
            raise ValueError(f"SIMulation is only allowed in AC+DC-INT mode. Current output mode: {output_mode}")

        self.write(f":SYSTem:CONFigure:MODE {mode}")

    def set_external_control(self, state: str) -> None:
        """Sets the external control state (on/off).
        
        Args:
            state (str or int): 'ON' (1) to enable external control, 'OFF' (0) to disable.
        """
        self.write(f":SYSTem:CONFigure:EXTio:STATe {state}")

    def err(self) -> str:
        return self.query(":SYST:ERR?")
    
    def set_freeze_hold(self, state: str) -> None:
        """Sets the freeze hold state (on/off).
        
        Args:
            state (str or int): 'ON' (1) to enable freeze hold, 'OFF' (0) to disable.
        """
        self.write(f":SYSTem:HOLD:STATe {state}")

    def set_ipeak_hold_time(self, time_ms: int) -> None:
        """Sets the Ipeak hold time for peak current measurement when output is on.

        Args:
            time_ms (int): The Ipeak hold time in milliseconds (1 to 60,000).
        """
        if not (1 <= time_ms <= 60000):
            raise ValueError("Invalid time_ms: must be between 1 and 60,000 milliseconds.")
        
        self.write(f":SYSTem:IPKhold:TIME {time_ms}")

    def set_slew_mode(self, mode: str) -> None:
        """Sets the slew mode.

        Args:
            mode (str or int): 'TIME' (0) to set the Time mode or 'SLOPe' (1) to set the Slope mode.
        """
        self.write(f":SYSTem:SLEW:MODE {mode}")
    
    def set_voltage_unit(self, unit: str) -> None:
        """Sets the unit of voltage for specific wave shapes (TRI or ARB).

        Args:
            unit (str or int): 'RMS' (0) to set the voltage unit as RMS, or 'P-P' (1) to set it as peak-to-peak (P-P).
        """
        self.write(f":SYSTem:VUNit {unit}")

    def set_IPK_limit(self, high: str = 'MAX', low: str = 'MIN', enable: bool = True) -> None:
        """Set the Ipk high and low limit parameters and enable/disable the limit for continuous operation mode.

            Args:
                high (float, str, optional): Ipk-High Limit in Arms, or 'MAX', 'MIN'.
                low (float, str, optional): Ipk-Low Limit in Arms, or 'MAX', 'MIN'.
                enable (bool, optional): If True, enables the Ipk limit. If False, disables it.
        """
        if high is not None:
            self.write(f":SOURce:CURRent:LIMit:PEAK:HIGH {high}")

        if low is not None:
            self.write(f":SOURce:CURRent:LIMit:PEAK:LOW {low}")

        if enable is not None:
            self.write(":SOURce:CURRent:LIMit:PEAK:MODE ON" if enable else ":SOURce:CURRent:LIMit:PEAK:MODE OFF")

    def set_Irms(self, Irms: str = None, enable: bool = None) -> None:
        """Set the Irms parameter and enable/disable the Irms limit for continuous operation mode.

            Args:
                Irms (float, str, optional): Irms in A., or 'MAX', 'MIN'.
                enable (bool, optional): If True, enables the Irms limit. If False, disables it.
        """
        if Irms is not None:
            self.write(f":SOURce:CURRent:LIMit:RMS {Irms}")

        if enable is not None:
            self.write(":SOURce:CURRent:LIMit:RMS:MODE ON" if enable else ":SOURce:CURRent:LIMit:RMS:MODE OFF")
    
    def set_frequency(self, high: str = None, low: str = None, freq: str = None) -> None:
        """Set the frequency parameters including upper limit, lower limit, and immediate frequency value. (Only AC+DC-INT or AC-INT or AC+DC-ADD or AC-ADD Active)


            Args:
                high (float, str, optional): The upper frequency limit in Hz or 'MIN', 'MAX'.
                low (float, str, optional): The lower frequency limit in Hz or 'MIN', 'MAX'.
                freq (float, str, optional): The immediate frequency value in Hz or 'MIN', 'MAX'.
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)

        if output_mode not in ['ACDC-INT', 'AC-INT', 'ACDC-ADD', 'AC-ADD']:
            raise ValueError(f"Frequency settings are only allowed in modes: AC+DC-INT, AC-INT, AC+DC-ADD, or AC-ADD. Current mode: {output_mode}")
        
        if high is not None:
            self.write(f":SOURce:FREQuency:LIMit:HIGH {high}")
        
        if low is not None:
            self.write(f":SOURce:FREQuency:LIMit:LOW {low}")
        
        if freq is not None:
            self.write(f":SOURce:FREQuency:IMMediate {freq}")

    def set_waveform(self, waveform: str) -> None:
        """Sets the waveform of the power supply. (Not available for DC-INT, AC+DC-EXT, and AC-EXT)

        Args:
            waveform (str): The waveform to set. Can be one of the following:
                - 'ARB1' (0): Arbitrary wave 1
                - 'ARB2' (1): Arbitrary wave 2
                - 'ARB3' (2): Arbitrary wave 3
                - 'ARB4' (3): Arbitrary wave 4
                - 'ARB5' (4): Arbitrary wave 5
                - 'ARB6' (5): Arbitrary wave 6
                - 'ARB7' (6): Arbitrary wave 7
                - 'ARB8' (7): Arbitrary wave 8
                - 'ARB9' (8): Arbitrary wave 9
                - 'ARB10' (9): Arbitrary wave 10
                - 'ARB11' (10): Arbitrary wave 11
                - 'ARB12' (11): Arbitrary wave 12
                - 'ARB13' (12): Arbitrary wave 13
                - 'ARB14' (13): Arbitrary wave 14
                - 'ARB15' (14): Arbitrary wave 15
                - 'ARB16' (15): Arbitrary wave 16
                - 'SIN' (16): Sin wave
                - 'SQU' (17): Square wave
                - 'TRI' (18): Triangle wave
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)

        if output_mode in ['DC-INT', 'ACDC-EXT', 'AC-EXT']:
            raise ValueError(f"Invalid mode: {output_mode}. Waveform setting is not available in DC-INT, ACDC-EXT, or AC-EXT modes.")

        self.write(f":SOURce:FUNCtion:SHAPe:IMMediate {waveform}")

    def set_THD(self, format: str) -> None:
        """Sets the THD format.

        Args:
            format (str, bool): THD format to set. Acceptable values are 'IEC' (0), or 'CSA' (1).
        """
        self.write(f":SOURce:FUNCtion:THD:FORMat {format}")

    def set_output_mode(self, mode: str) -> None:
        """Sets the output mode of the power supply.

        Args:
            mode (str, optional): Output mode to set. Acceptable values are:
                                'ACDC-INT' (0), 
                                'AC-INT' (1),
                                'DC-INT' (2),
                                'ACDC-EXT' (3),
                                'AC-EXT' (4),
                                'ACDC-ADD' (5),
                                'AC-ADD' (6),
                                'ACDC-SYNC' (7),
                                'AC-SYNC' (8).
        """
        self.write(f":SOURce:MODE {mode}")

    def get_output_mode(self) -> str:
        """Queries the output mode of the power supply.

        Returns:
            str: The current output mode. Possible return values are:
                'ACDC-INT' (0),
                'AC-INT' (1),
                'DC-INT' (2),
                'ACDC-EXT' (3),
                'AC-EXT' (4),
                'ACDC-ADD' (5),
                'AC-ADD' (6),
                'ACDC-SYNC' (7),
                'AC-SYNC' (8).
        """
        return self.query(":SOURce:MODE?").strip()

    def set_phase_parameters(self, start_state: str = None, stop_state: str = None, start_phase: float = None, stop_phase: float = None) -> None:
        """Sets the state and phase values for the start and stop phases. (Not available for DC-INT, AC+DC-EXT and AC-EXT)


        Args:
            start_state (str, optional):  State of start phase. Acceptable values are 'FREE', 'FIXED', or 0 (FREE), 1 (FIXED).
            stop_state (str, optional): State of stop phase. Acceptable values are 'FREE', 'FIXED', or 0 (FREE), 1 (FIXED).
            start_phase (float, optional): Start phase value in degrees. Acceptable values are: 0 to 359.9, 'MIN', or 'MAX'.
            stop_phase (float, optional): Stop phase value in degrees. Acceptable values are: 0 to 359.9, 'MIN', or 'MAX'.
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)

        if output_mode in ['DC-INT', 'ACDC-EXT', 'AC-EXT']:
            raise ValueError(f"Phase settings are not allowed in modes: DC-INT, AC+DC-EXT, and AC-EXT. Current mode: {output_mode}")
        
        if start_state is not None:
            self.write(f":SOURce:PHASe:STARt:STATe {start_state}")

        if stop_state is not None:
            self.write(f":SOURce:PHASe:STOP:STATe {stop_state}")

        if start_phase is not None:
            start_state_response = self.query(f":SOURce:PHASe:STARt:STATe?")
            time.sleep(0.2)
            if start_state_response != "FIXED":
                raise ValueError(f"start_phase can only be set when the start state is 'FIXED'. Current state: {start_state_response}")
            self.write(f":SOURce:PHASe:STARt {start_phase}")

        if stop_phase is not None:
            stop_state_response = self.query(f":SOURce:PHASe:STOP:STATe?")
            time.sleep(0.2)
            if stop_state_response != "FIXED":
                raise ValueError(f"stop_phase can only be set when the stop state is 'FIXED'. Current state: {stop_state_response}")
            self.write(f":SOURce:PHASe:STOP {stop_phase}")    

    def set_voltage_parameters(self, 
                            volt_range: str = None, 
                            limit_vrms: str = None, 
                            limit_vpp: str = None, 
                            limit_vpk_h: str = None, 
                            limit_vpk_l: str = None, 
                            vrms: str = None, 
                            offset: str = None) -> None:
        """Sets various voltage parameters for the power supply.

        Args:
            volt_range (str, optional): Voltage range. Acceptable values are:
                100, 200, 'AUTO'. AUTO is only available in AC+DC-INT, AC-INT, DC-INT, AC+DC-SYNC, or AC-SYNC modes.
            limit_vrms (str, optional): RMS voltage limit. Acceptable values are:
                Any valid Vrms value, 'MIN', 'MAX'. Only available in AC-INT, AC-ADD, or AC-SYNC modes.
            limit_vpp (str, optional): Vpp limit. Acceptable values are:
                Any valid Vpp value, 'MIN', 'MAX'. Only available in AC-INT, AC-ADD, or AC-SYNC modes, 
                with specific wave shape(TRI or ARB) and specific voltage Unit(p-p).
            limit_vpk_h (str, optional): Voltage high limit. Acceptable values are:
                Any valid voltage high limit value, 'MIN', 'MAX'. Only available in AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC modes.
            limit_vpk_l (str, optional): Voltage low limit. Acceptable values are:
                Any valid voltage low limit value, 'MIN', 'MAX'. Only available in AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC modes.
            vrms (str, optional): RMS voltage value. Acceptable values are:
                Any valid Vrms value, 'MIN', 'MAX'. Not available in DC-INT, AC+DC-EXT, or AC-EXT modes.
            offset (str, optional): Voltage offset value. Acceptable values are:
                Any valid voltage offset value, 'MIN', 'MAX'. Only available in AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC modes.
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)

        if volt_range is not None:
            self.write(f":SOURce:VOLTage:RANGe {volt_range}")

        if limit_vrms is not None:
            if output_mode not in ['AC-INT', 'AC-ADD', 'AC-Sync']:
                raise ValueError(f"RMS limit can only be set in modes: AC-INT, AC-ADD, or AC-SYNC. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LIMit:RMS {limit_vrms}")  # Vrms Limit

        if limit_vpp is not None:
            if output_mode not in ['AC-INT', 'AC-ADD', 'AC-Sync']:
                raise ValueError(f"Peak limit can only be set in modes: AC-INT, AC-ADD, or AC-SYNC. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LIMit:PEAK {limit_vpp}")  # Vpp Limit

        if limit_vpk_h is not None:
            if output_mode not in ['ACDC-INT', 'DC-INT', 'ACDC-ADD', 'ACDC-Sync']:
                raise ValueError(f"High limit can only be set in modes: AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LIMit:HIGH {limit_vpk_h}")  # VPK+ Limit

        if limit_vpk_l is not None:
            if output_mode not in ['ACDC-INT', 'DC-INT', 'ACDC-ADD', 'ACDC-Sync']:
                raise ValueError(f"Low limit can only be set in modes: AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LIMit:LOW {limit_vpk_l}")  # VPK- Limit

        if vrms is not None:
            if output_mode in ['DC-INT', 'ACDC-EXT', 'AC-EXT']:
                raise ValueError(f"RMS voltage value is not allowed in modes: DC-INT, AC+DC-EXT, or AC-EXT. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LEVel:IMMediate:AMPLitude {vrms}")  # ACV

        if offset is not None:
            if output_mode not in ['ACDC-INT', 'DC-INT', 'ACDC-ADD', 'AC-Sync']:
                raise ValueError(f"Voltage offset can only be set in modes: AC+DC-INT, DC-INT, AC+DC-ADD, or AC+DC-SYNC. Current mode: {output_mode}")
            self.write(f":SOURce:VOLTage:LEVel:IMMediate:OFFSet {offset}")  # DCV

    def set_seq_parameters(self, step: int = None, cparams: dict = None, sparams: dict = None) -> None:
        """Sets the common parameters for the Sequence mode. (Only Sequence Mode Active)

        Args:
            step (int, optional): Current step number (0 to 999).
            cparams (dict, optional): Dictionary containing the parameters. Acceptable keys are:
                - 'step_time' (float): Step time.
                - 'on_phase' (float): On phase value.
                - 'on_phase_st' (str or int): On phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
                - 'off_phase' (float): Off phase value.
                - 'off_phase_st' (str or int): Off phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
                - 'term' (str): Termination settings, can be 'CONTinue', 'END', or 'HOLD'.
                - 'jump_to' (int): Jump step number (0 to 999).
                - 'jump_st' (str or int): Jump state, can be 'ON' (1), or 'OFF' (0).
                - 'jump_cnt' (int): Jump count (0 to 9999).
                - 'sync' (int): Synchronous code for each step, can be 0, 1 , 2 , or 3. (0: LL, 1: LH, 2: HL, 3: HH).
                - 'br1' (int): Branch 1 number (0 to 999).
                - 'br1_st' (str or int): Branch 1 state, can be 'ON' (1), or 'OFF' (0).
                - 'br2' (int): Branch 2 number (0 to 999).
                - 'br2_st' (str or int): Branch 2 state, can be 'ON' (1), or 'OFF' (0).
            sparams (dict, optional): Dictionary containing the step-specific parameters. Acceptable keys are:
                - 'acv' (float): AC voltage setting.
                - 'acv_mode' (str or int): ACV mode, can be 'CONSt' (0), 'KEEP' (1), or 'SWEep' (2).
                - 'dcv' (float): DC voltage setting (not applicable, will be ignored).
                - 'dcv_mode' (str or int): DCV mode, can be 'CONSt' (0), 'KEEP' (1), or 'SWEep' (2).
                - 'freq' (float): Frequency setting.
                - 'freq_mode' (str or int): Frequency mode, can be 'CONSt' (0), 'KEEP' (1), or 'SWEep' (2).
                - 'waveform' (str): Waveform type, can be 'SIN', 'SQU', 'TRI', or 'ARB1' to 'ARB16'.
                - 'phase' (int): Phase angle (fixed to 0).
        """
        if step is not None:
            if not (0 <= step <= 999):
                raise ValueError(f"The step value {step} is out of range. It must be between 0 and 999.")
            self.write(f":SOURce:SEQuence:STEP {step}")

        if cparams is not None:
            required_cparams_keys = ('step_time', 'on_phase', 'on_phase_st', 'off_phase', 'off_phase_st', 'term', 'jump_to', 'jump_st', 'jump_cnt', 'sync', 'br1', 'br1_st', 'br2', 'br2_st')
            if set(cparams.keys()) != set(required_cparams_keys):
                raise ValueError(f"Missing or extra parameters. Required: {required_cparams_keys}")
            cmd_cparam = f":SOURce:SEQuence:CPARameter {cparams['step_time']},{cparams['on_phase']},{cparams['on_phase_st']},"+\
                f"{cparams['off_phase']},{cparams['off_phase_st']},{cparams['term']},"+\
                f"{cparams['jump_to']},{cparams['jump_st']},{cparams['jump_cnt']},{cparams['sync']},"+\
                f"{cparams['br1']},{cparams['br1_st']},{cparams['br2']},{cparams['br2_st']},0"
            self.write(cmd_cparam)
        
        if sparams is not None:
            required_sparams_keys = ('acv', 'acv_mode', 'dcv', 'dcv_mode', 'freq', 'freq_mode', 'waveform', 'phase')
            if set(sparams.keys()) != set(required_sparams_keys):
                raise ValueError(f"Missing or extra step parameters. Required: {required_sparams_keys}")
            cmd_sparam = f":SOURce:SEQuence:SPARameter {sparams['acv']},{sparams['acv_mode']},{sparams['dcv']},{sparams['dcv_mode']}," +\
                        f"{sparams['freq']},{sparams['freq_mode']},{sparams['waveform']},{sparams['phase']}"
            self.write(cmd_sparam)

    def get_seq_cstep(self) -> int:
        """Returns the currently running step number. (Only Sequence Mode Active)

        Returns:
            int: The current step number (positive integer).
        """
        return int(self.query(":SOURce:SEQuence:CSTep?"))

    def get_seq_condition(self) -> int:
        """Queries the current sequence status in Sequence Mode. (Only Sequence Mode Active)

        Returns:
            int: Current sequence status. Possible values are:
                - 0: Idle mode
                - 1: Run mode
                - 2: Hold mode
        """
        return int(self.query(":SOURce:SEQuence:CONDition?"))
    
    def set_seq_execute(self, action: str) -> None:
        """Sets the execution actions in sequence mode. (Only Sequence Mode Active) 

        Args:
            action (str): Action to be executed. Acceptable values are:
                - 'STOP': Stops sequence execution
                - 'STARt': Starts sequence execution
                - 'HOLD': Holds sequence execution
                - 'BRAN1': Jumps to Branch 1 execution
                - 'BRAN2': Jumps to Branch 2 execution
        """
        self.write(f":TRIGger:SEQuence:SELected:EXECute {action}")

    def get_sim_condition(self) -> int:
        """Returns the simulation status. (Only Simulation Mode Active)

        Returns:
            int: Current simulation status. Possible values are:
                - 0: Idle mode
                - 1: Run mode
                - 2: Hold mode
        """
        return int(self.query(":SOURce:SIMulation:CONDition?"))
    
    def set_sim_abnormal(self, code: str = None, freq: str = None, ph_start_st: str = None, 
                         ph_start: str = None, ph_stop_st: str = None, ph_stop: str = None, 
                         time: str = None, volt: str = None) -> None:
        """Sets the abnormal step parameters in Simulation mode. (Only Simulation Mode Active)

        Args:
            code (int or str, optional): External trigger output code, can be 0, 1, 2, 3, 'MINimum', or 'MAXimum'. (0: LL, 1: LH, 2: HL, 3: HH).
            freq (float or str, optional): Frequency of the abnormal step, can be a frequency value, 'MINimum', or 'MAXimum'.
            ph_start_st (str or int, optional): ON phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_start (float or str, optional): ON phase (start phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            ph_stop_st (str or int, optional): OFF phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_stop (float or str, optional): OFF phase (stop phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            time (str, optional): Time value of the abnormal step, can be a time in seconds, 'MINimum', or 'MAXimum'.
            volt (str, optional): Voltage value of the abnormal step, can be a numeric voltage value, 'MINimum', or 'MAXimum'.
        """
        if code is not None:
            self.write(f":SOURce:SIMulation:ABNormal:CODE {code}")
        if freq is not None:
            self.write(f":SOURce:SIMulation:ABNormal:FREQuency {freq}")
        if ph_start_st is not None:
            self.write(f":SOURce:SIMulation:ABNormal:PHASe:STARt:ENABle {ph_start_st}")
        if ph_start is not None:
            self.write(f":SOURce:SIMulation:ABNormal:PHASe:STARt {ph_start}")
        if ph_stop_st is not None:
            self.write(f":SOURce:SIMulation:ABNormal:PHASe:STOP:ENABle {ph_stop_st}")
        if ph_stop is not None: 
            self.write(f":SOURce:SIMulation:ABNormal:PHASe:STOP {ph_stop}")
        if time is not None: 
            self.write(f":SOURce:SIMulation:ABNormal:TIME {time}")
        if volt is not None:
            self.write(f":SOURce:SIMulation:ABNormal:VOLTage {volt}")

    def set_sim_initial(self, code: str = None, freq: str = None, ph_start_st: str = None, 
                        ph_start: str = None, ph_stop_st: str = None, ph_stop: str = None, 
                        volt: str = None) -> None:
        """Sets the initial step parameters in Simulation mode. (Only Simulation Mode Active)

        Args:
            code (int or str, optional): External trigger output code, can be 0, 1, 2, 3, 'MINimum', or 'MAXimum'. (0: LL, 1: LH, 2: HL, 3: HH).
            freq (float or str, optional): Frequency of the initial step, can be a frequency value, 'MINimum', or 'MAXimum'.
            ph_start_st (str or int, optional): ON phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_start (float or str, optional): ON phase (start phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            ph_stop_st (str or int, optional): OFF phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_stop (float or str, optional): OFF phase (stop phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            volt (float or str, optional): Voltage value of the initial step, can be a numeric voltage value, 'MINimum', or 'MAXimum'.
        """
        if code is not None:
            self.write(f":SOURce:SIMulation:INITial:CODE {code}")
        if freq is not None:
            self.write(f":SOURce:SIMulation:INITial:FREQuency {freq}")
        if ph_start_st is not None:
            self.write(f":SOURce:SIMulation:INITial:PHASe:STARt:ENABle {ph_start_st}")
        if ph_start is not None:
            self.write(f":SOURce:SIMulation:INITial:PHASe:STARt {ph_start}")
        if ph_stop_st is not None:
            self.write(f":SOURce:SIMulation:INITial:PHASe:STOP:ENABle {ph_stop_st}")
        if ph_stop is not None:
            self.write(f":SOURce:SIMulation:INITial:PHASe:STOP {ph_stop}")
        if volt is not None:
            self.write(f":SOURce:SIMulation:INITial:VOLTage {volt}")

    def set_sim_normal(self, norm_idx : int, code: str = None, freq: str = None,
                    ph_start_st: str = None, ph_start: str = None,
                    ph_stop_st: str = None, ph_stop: str = None,
                    time: str = None, volt: str = None) -> None:
        """Sets the normal 1 or normal 2 step parameters in simulation mode. (Only Simulation Mode Active)
        
        Args:
            norm_idx  (int): Normal index number, 1 for normal 1, 2 for normal 2.
            code (int or str, optional): External trigger output code, can be 0, 1, 2, 3, 'MINimum', or 'MAXimum'. (0: LL, 1: LH, 2: HL, 3: HH).
            freq (float or str, optional): Frequency of the normal 1 step, can be a frequency value, 'MINimum', or 'MAXimum'.
            ph_start_st (str or int, optional): ON phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_start (float or str, optional): ON phase (start phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            ph_stop_st (str or int, optional): OFF phase state, can be 'FIXED' ('ON') (1), or 'FREE' ('OFF') (0).
            ph_stop (float or str, optional): OFF phase (stop phase) value, can be a value between 0 and 359.9, 'MINimum', or 'MAXimum'.
            time (float or str, optional): Time value of the normal step, can be a time in seconds (0.0001 to 999.9999), 'MINimum', or 'MAXimum'.
            volt (float or str, optional): Voltage value of the normal 1 step, can be a numeric voltage value, 'MINimum', or 'MAXimum'.
        """
        if norm_idx not in [1, 2]:
            raise ValueError(f"Invalid norm_idx: {norm_idx}. Must be 1 (normal 1) or 2 (normal 2).")

        if code is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:CODE {code}")
        if freq is not None:
            if norm_idx == 2:
                raise ValueError(f"freq is only applicable to norm_idx = 1.")
            self.write(f":SOURce:SIMulation:NORMal1:FREQuency {freq}")
        if ph_start_st is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:PHASe:STARt:ENABle {ph_start_st}")
        if ph_start is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:PHASe:STARt {ph_start}")
        if ph_stop_st is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:PHASe:STOP:ENABle {ph_stop_st}")
        if ph_stop is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:PHASe:STOP {ph_stop}")
        if time is not None:
            self.write(f":SOURce:SIMulation:NORMal{norm_idx}:TIME {time}")
        if volt is not None:
            if norm_idx == 2:
                raise ValueError(f"volt is only applicable to norm_idx = 1.")
            self.write(f":SOURce:SIMulation:NORMal1:VOLTage {volt}")

    def set_sim_transition(self, trans_idx: int, time: str = None, code: str = None) -> None:
        """Sets the transition step parameters in Simulation mode. (Only Simulation Mode Active)

        Args:
            trans_idx (int): Transition index number, 1 for transition 1, 2 for transition 2.
            time (float or str, optional): Time value of the transition step, can be a time in seconds (0 to 999.9999), 'MINimum', or 'MAXimum'.
            code (int or str, optional): External trigger output code, can be 0, 1, 2, 3, 'MINimum', or 'MAXimum'. (0: LL, 1: LH, 2: HL, 3: HH).
        """
        if trans_idx not in [1, 2]:
            raise ValueError("Invalid trans_idx: {trans_idx}. Must be 1 (transition 1) or 2 (transition 2).")
        
        if time is not None:
            self.write(f":SOURce:SIMulation:TRANsition{trans_idx}:TIME {time}")
        
        if code is not None:
            self.write(f":SOURce:SIMulation:TRANsition{trans_idx}:CODE {code}")

    def set_sim_repeat(self, count: str = None, enable: str = None):
        """Configures the repeat parameters for the simulation mode. (Only Simulation Mode Active)

        Args:
            count (int or str, optional): Repeat count, can be a value between 0 and 9999 (0 = infinite loop), 'MINimum' or 'MAXimum'.
            enable (int or str, optional): Enables or disables the repeat function, can be 'ON' (1), or 'OFF' (0)..
        """
        if count is not None:
            self.write(f":SOURce:SIMulation:REPeat:COUNt {count}")
        if enable is not None:
            self.write(f":SOURce:SIMulation:REPeat:ENABle {enable}")

    def set_sim_execute(self, action: str) -> None:
        """Sets the execution actions in simulation mode. (Only Simulation Mode Active) 

        Args:
            action (str): Action to be executed. Acceptable values are:
                - 'STOP': Stops simulation execution
                - 'STARt': Starts simulation execution
                - 'HOLD': Holds simulation execution
        """
        self.write(f":TRIGger:SIMulation:SELected:EXECute {action}")

    def set_gain(self, gain: str) -> None:
        """Sets the input gain value. (Only AC+DC-EXT or AC-EXT or AC+DC-ADD or AC-ADD Active)

        Args:
            gain(float or str): Input gain value in volts, or 'MINimum' / 'MAXimum'.
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)

        if output_mode not in ['ACDC-EXT', 'AC-EXT', 'ACDC-ADD', 'AC-ADD']:
            raise ValueError(f"Invalid mode: {output_mode}. Gain setting is only allowed in modes ACDC-EXT, AC-EXT, ACDC-ADD, or AC-ADD.")
        self.write(f":INPut:GAIN {gain}")

    def set_sync_source(self, source: str) -> None:
        """Sets the sync source state. (Only AC+DC-sync or AC-sync Active)
        
        Args:
            source (str): Sync source, can be 'LINE'(0) or 'EXT'(1).
        """
        output_mode = self.get_output_mode()
        # time.sleep(0.2)
        
        if output_mode not in ['ACDC-Sync', 'AC-Sync']:
            raise ValueError(f"Invalid mode: {output_mode}. Sync source can only be set in modes ACDC-SYNC or AC-SYNC.")

        self.write(f":INPut:SYNC:SOURce {source}")

if __name__ =='__main__':
    pass