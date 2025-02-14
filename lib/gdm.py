# Name: gdm.py
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

class Gdm():
    """This module can control GDM-8261A、GDM-906X.

    It supports USB interface to use SCPI.

    It will scan available instruments on your DSO, then require a serial number to specify and connect to it.

    Usage:
    -------
    .. code-block:: python

        import gdm
        inst = gdm.Gdm()
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

    def connect(self, SN:str, baudrate:int=9600, timeout:int=3) -> int:
        """Connect to the gdm.

        Args:
            SN (str): Serial Number is necessary.
            baudrate (int, optional): baudrate. Defaults to 9600.
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
        cmd = cmd.strip()
        if cmd[-1] == '\n':
            pass
        else:
            cmd += '\n'
        self.write(cmd)
        time.sleep(self.scpi_delay)
        response = self.readline().strip()
        retry_count = 5
        while not response and retry_count > 0:
            print("Debug: Empty response, retrying...")
            time.sleep(self.scpi_delay * 5)
            self.write(cmd)
            time.sleep(self.scpi_delay * 5)
            response = self.readline().strip()
            retry_count -= 1
        return response

    def _validate_disp(self, disp: int) -> None:
        if disp not in [1, 2]:
            raise ValueError(f"Invalid display: '{disp}'. Must be 1 or 2.")

    def _validate_range(self, value: str = None) -> str:
        if value is not None:
            if value not in ['DEF', 'AUTO', 'MIN', 'MAX']:
                try:
                    float(value)
                except ValueError:
                    raise ValueError(f"Invalid range value: '{value}'. Must be 'DEF', 'AUTO', 'MIN', 'MAX', or a numeric value.")
            cmd = f' {value}'
            return cmd
        return ''
        
    def _validate_resolution(self, value: str = None) -> str:    
        if value is not None:
            if value not in ['DEF', 'MIN', 'MAX']:
                try:
                    float(value)
                except ValueError:
                    raise ValueError(f"Invalid res value: '{value}'. Must be 'DEF', 'MIN', 'MAX', or a numeric value.")
            cmd += f',{value}'
            return cmd
        return '' 

    def idn(self) -> str:
        return self.query('*idn?')
    
    def opc(self) -> int:
        return self.query('*opc?')
    
    def err(self) -> str:
        return self.query(':SYST:ERR?')
    
    def abort(self) -> None:
        """Aborts a measurement in progress, returning the instrument to the trigger idle state.

        """
        self.write('ABORt')

    def initiate(self) -> None:
        """Changes the state of the triggering system from "idle" to "wait-for-trigger", and clears the previous set of measurements from reading memory. 
        
        """
        self.write("INITiate:IMMediate")

    def read_display_value(self, disp: int = 1) -> list:
        """Returns the display values based on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.

        Returns:
            list: The measured values from the specified display.
        """
        self._validate_disp(disp)
        cmd = 'VAL1?' if disp == 1 else 'VAL2?'
        response = self.query(cmd)
        return response.strip().split(',')

    def get_function(self, disp: int = 1) -> str:
        """Returns the current function on the specified display.

        Args:
            disp (int): Display number (1 or 2).

        Return:
            current function (str): 
                For display 1: One of 'VOLT', 'VOLT:AC', 'CURR', 'CURR:AC', 'RES', 'FRES', 
                    'FREQ', 'PER', 'TEMP:RTD', 'TEMP:FRTD', 'TEMP:TCO', 'DIOD', 'CONT'.
                For display 2: One of 'VOLT', 'VOLT:AC', 'CURR', 'CURR:AC', 'RES', 'FRES',
                    'FREQ', 'PER', 'NON'.
        """
        cmd = f'CONFigure{disp if disp == 2 else ""}:FUNCtion?'
        return self.query(cmd)

    def get_range(self, disp: int = 1) -> str:
        """Returns the current range on the specified display.

        Args:
            disp (int): Display number (1 or 2).
        
        Return:
            range (str):
                For DCV: 0.1(100mV), 1(1V), 10(10V), 100(100V), 1000(1000V).
                For ACV: 0.1(100mV), 1(1V), 10(10V), 100(100V), 750(750V).
                For ACI: 0.001(1mA), 0.01(10mA), 0.1(100mA), 1(1A), 10(10A).
                For DCI: 0.0001(100μA), 0.001(1mA), 0.01(10mA), 0.1(100mA), 1(1A), 10(10A) for disp 1,
                    or 0.001(1mA), 0.01(10mA), 0.1(100mA), 1(1A), 10(10A) for disp 2.
                For RES: 10E+1(100Ω) 10E+2(1kΩ), 10E+3(10kΩ), 10E+4 (100kΩ), 10E+5(1MΩ), 10E+6(10MΩ), 10E+7(100MΩ).
                NONE: Indicates that the second display is not active.
        """
        cmd = f'CONFigure{disp if disp == 2 else ""}:RANGe?'
        return self.query(cmd)

    def set_auto_range(self, disp: int = 1, state: str = None) -> None:
        """Sets Auto-Range on or off on the specified display.

        Args:
            disp (int): Display number (1 or 2).
            state (str): 'ON' or 'OFF'.
        """
        self._validate_disp(disp)
        if state not in ['ON', 'OFF']:
            raise ValueError(f"Invalid state: '{state}'. Must be 'ON' or 'OFF'.")
        cmd = f'CONFigure{disp if disp == 2 else ""}:AUTO {state}'
        self.write(cmd)

    def get_auto_range(self, disp: int = 1) -> bool:
        """Returns the Auto-Range status of the function on the specified display.

        Args:
            disp (int): Display number (1 or 2).
                        
        Return:
            status (bool): True if the current status is Auto range, False if the current status is Manual range.
        """
        cmd = f'CONFigure{disp if disp == 2 else ""}:AUTO?'
        response = self.query(cmd)
        return response == '1'

    def configure_DCV(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None, nplc: str = None, auto_imp: str = None) -> None:
        """Sets measurement to DC Voltage on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): DC voltage auto-range setting. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
            nplc (str, optional): Integration time in PLCs. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value. 
                                For any numeric value, the DMM will automatically set the PLC to the closest acceptable value. 
                                The acceptable PLC values are:
                                    - GDM-8261A: 0.025, 0.1, 0.25, 1, 2, 12.
                                    - GDM-906X: 0.006, 0.0083, 0.0125, 0.025, 0.05, 0.15, 0.6, 1, 3, 12.
            auto_imp (str, optional): Automatic input impedance. Acceptable values include 0, 1, 'ON' or 'OFF'. (For GDM-906X)
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:VOLTage:DC' if disp == 1 else f'CONFigure{disp}:VOLTage:DC'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid DC voltage auto-range setting: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:VOLTage:DC:RANGe:AUTO {auto_range}')
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            self.write(f'SENSe:VOLTage:DC:NPLCycles {nplc}')
        if auto_imp is not None:
            if auto_imp not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid auto impedance value: '{auto_imp}'. Must be 'ON' or 'OFF'.")
            self.write(f'SENSe:VOLTage:DC:IMPedance:AUTO {auto_imp}')    

    def configure_DCV_ratio(self, range: str = None, res: str = None) -> None:
        """Sets measurement to DCV ratio mode on the 1st display and specifies range/resolution.

        Args:
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
        """
        cmd = 'CONFigure:VOLTage:DC:RATio'
        cmd += self._validate_range(range)        
        cmd += self._validate_resolution(res)           
        self.write(cmd)

    def configure_ACV(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None) -> None:
        """Sets measurement to AC Voltage on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): AC voltage auto-range setting. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:VOLTage:AC' if disp == 1 else f'CONFigure{disp}:VOLTage:AC'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid AC voltage auto-range setting: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:VOLTage:AC:RANGe:AUTO {auto_range}')


    def configure_DCI(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None, nplc: str = None) -> None:
        """Sets measurement to DC Current on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Current range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): DC current auto-range setting. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
            nplc (str, optional): Integration time in PLCs. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value.
                                For any numeric value, the DMM will automatically set the PLC to the closest acceptable value. 
                                The acceptable PLC values are:
                                    - GDM-8261A: 0.025, 0.1, 0.25, 1, 2, 12.
                                    - GDM-906X: 0.006, 0.0083, 0.0125, 0.025, 0.05, 0.15, 0.6, 1, 3, 12.
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:CURRent:DC' if disp == 1 else f'CONFigure{disp}:CURRent:DC'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)     
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid DC current auto-range setting: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:CURRent:DC:RANGe:AUTO {auto_range}')
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            self.write(f'SENSe:CURRent:DC:NPLCycles {nplc}')

    def configure_ACI(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None) -> None:
        """Sets measurement to AC Current on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Current range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): AC current auto-range setting. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:CURRent:AC' if disp == 1 else f'CONFigure{disp}:CURRent:AC'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid AC current auto-range setting: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:CURRent:AC:RANGe:AUTO {auto_range}')

    def configure_resistance(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None, nplc: str = None) -> None:
        """Sets measurement to 2W Resistance on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Resistance range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): Auto-range setting for 2-wire resistance. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
            nplc (str, optional): Integration time in PLCs. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value.
                                For any numeric value, the DMM will automatically set the PLC to the closest acceptable value. 
                                The acceptable PLC values are:
                                    - GDM-8261A: 0.025, 0.1, 0.25, 1, 2, 12.
                                    - GDM-906X: 0.006, 0.0083, 0.0125, 0.025, 0.05, 0.15, 0.6, 1, 3, 12.
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:RESistance' if disp == 1 else f'CONFigure{disp}:RESistance'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto-range setting: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:RESistance:RANGe:AUTO {auto_range}')
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            self.write(f'SENSe:RESistance:NPLCycles {nplc}')

    def configure_4W_resistance(self, disp: int = 1, range: str = None, res: str = None, auto_range: str = None, nplc: str = None) -> None:
        """Sets measurement to 4W Resistance on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Resistance range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            auto_range (str, optional): Auto-range setting. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
            nplc (str, optional): Integration time in PLCs. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value.
                                For any numeric value, the DMM will automatically set the PLC to the closest acceptable value. 
                                The acceptable PLC values are:
                                    - GDM-8261A: 0.025, 0.1, 0.25, 1, 2, 12.
                                    - GDM-906X: 0.006, 0.0083, 0.0125, 0.025, 0.05, 0.15, 0.6, 1, 3, 12.
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:FRESistance' if disp == 1 else f'CONFigure{disp}:FRESistance'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto_range value: '{auto_range}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:FRESistance:RANGe:AUTO {auto_range}')
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            self.write(f'SENSe:FRESistance:NPLCycles {nplc}')

    def configure_frequency(self, disp: int = 1, range: str = None, res: str = None, gtimer: float = None, injack: int = None, volt_range: str = None, vrange_auto: str = None, curr_range: str = None, crange_auto: str = None) -> None:
        """Sets measurement to Frequency on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            gtimer (float, optional): Aperture time (gate time). Acceptable values are 0.01 for FAST, 0.1 for MID, or 1 for SLOW.
            injack (int, optional): Input port. 
                                For GDM-8261A, acceptable values are 0 for volt, 1 for 1A, or 2 for 10A.
                                For GDM-906X, acceptable values are 0 for Voltage, 1 for 3A, or 2 for 10A.
            volt_range (str, optional): Voltage range for the frequency measurement. Acceptable values include a specific numeric value, 'MIN', 'MAX', or 'DEF'.
            vrange_auto (str, optional): Auto-range setting for voltage range. Acceptable values are 0, 1, 'ON', 'OFF', 'ONCE'.
            curr_range (str, optional): Current range for the frequency measurement. Acceptable values include a specific numeric value, 'MIN', 'MAX', or 'DEF'. (For GDM-906X)
            crange_auto (str, optional): Auto-range setting for current range. Acceptable values are 0, 1, 'ON', 'OFF', 'ONCE'. (For GDM-906X)
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:FREQuency' if disp == 1 else f'CONFigure{disp}:FREQuency'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if gtimer is not None:
            if gtimer not in [0.01, 0.1, 1]:
                raise ValueError("Invalid gate time. Must be one of 0.01 (FAST), 0.1 (MID), or 1 (SLOW).")
            cmd_gtimer = f'SENSe:FREQuency:APERture {gtimer}'
            self.write(cmd_gtimer)
        if injack is not None:
            if injack not in [0, 1, 2]:
                raise ValueError("Invalid input port. Must be one of 0 (volt), 1 (1A/3A), or 2 (10A).")
            cmd_injack = f'SENSe:FREQuency:INPutjack {injack}'
            self.write(cmd_injack)
        if volt_range is not None:
            if volt_range not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(volt_range)
                except ValueError:
                    raise ValueError(f"Invalid voltage range value: '{volt_range}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd_volt_range = f'SENSe:FREQuency:VOLTage:RANGe {volt_range}'
            self.write(cmd_volt_range)
        if vrange_auto is not None:
            if vrange_auto not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError("Invalid voltage range auto setting. Must be one of 0, 1, 'ON', 'OFF', 'ONCE'.")
            self.write(f'SENSe:FREQuency:VOLTage:RANGe:AUTO {vrange_auto}')
        if curr_range is not None:
            if curr_range not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(curr_range)
                except ValueError:
                    raise ValueError(f"Invalid current range value: '{curr_range}'. Must be 'DEF', 'MIN', 'MAX', or a numeric value.")
            cmd_curr_range = f'SENSe:FREQuency:CURRent:RANGe {curr_range}'
            self.write(cmd_curr_range)
        if crange_auto is not None:
            if crange_auto not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError("Invalid current range auto setting. Must be one of 0, 1, 'ON', 'OFF', 'ONCE'.")
            self.write(f'SENSe:FREQuency:CURRent:RANGe:AUTO {crange_auto}') 

    def configure_period(self, disp: int = 1, range: str = None, res: str = None, gtimer: float = None, injack: int = None, volt_range: str = None, vrange_auto: str = None, curr_range: str = None, crange_auto: str = None) -> None:
        """Sets measurement to Period on the specified display (either the first or second) and specify the range/resolution.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            gtimer (float, optional): Aperture time (gate time). Acceptable values are 0.01 for FAST, 0.1 for MID, or 1 for SLOW.
            injack (int, optional): Input port. Acceptable values are 0 for volt, 1 for 1A, or 2 for 10A.
            volt_range (str, optional): Voltage range for the period measurement. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value.
            vrange_auto (str, optional): Auto-range setting for voltage range. Acceptable values are 0, 1, 'ON', 'OFF', 'ONCE'.
            curr_range (str, optional): Current range for the period measurement. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value. (For GDM-906X)
            crange_auto (str, optional): Auto-range setting for current range. Acceptable values are 0, 1, 'ON', 'OFF', 'ONCE'. (For GDM-906X)
        """
        self._validate_disp(disp)
        cmd = f'CONFigure:PERiod' if disp == 1 else f'CONFigure{disp}:PERiod'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        self.write(cmd)
        if gtimer is not None:
            if gtimer not in [0.01, 0.1, 1]:
                raise ValueError("Invalid gate time. Must be one of 0.01 (FAST), 0.1 (MID), or 1 (SLOW).")
            cmd_gtimer = f'SENSe:PERiod:APERture {gtimer}'
            self.write(cmd_gtimer)
        if injack is not None:
            if injack not in [0, 1, 2]:
                raise ValueError("Invalid input port. Must be one of 0 (volt), 1 (1A), or 2 (10A).")
            cmd_injack = f'SENSe:PERiod:INPutjack {injack}'
            self.write(cmd_injack)
        if volt_range is not None:
            if volt_range not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(volt_range)
                except ValueError:
                    raise ValueError(f"Invalid voltage range value: '{volt_range}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd_volt_range = f'SENSe:PERiod:VOLTage:RANGe {volt_range}'
            self.write(cmd_volt_range)
        if vrange_auto is not None:
            if vrange_auto not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError("Invalid voltage range auto setting. Must be one of 0, 1, 'ON', 'OFF', 'ONCE'.")
            self.write(f'SENSe:PERiod:VOLTage:RANGe:AUTO {vrange_auto}')
        if curr_range is not None:
            if curr_range not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(curr_range)
                except ValueError:
                    raise ValueError(f"Invalid current range value: '{curr_range}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd_curr_range = f'SENSe:PERiod:CURRent:RANGe {curr_range}'
            self.write(cmd_curr_range)

        if crange_auto is not None:
            if crange_auto not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError("Invalid current range auto setting. Must be one of 0, 1, 'ON', 'OFF', 'ONCE'.")
            self.write(f'SENSe:PERiod:CURRent:RANGe:AUTO {crange_auto}')    

    def configure_capacitance(self, range: str = None, auto_range: str = None, calibrate: bool = False) -> None:
        """Sets measurement to Capacitance on the 1st display and specify the range. (For GDM-906X)

        Args:
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            auto_range (int or str, optional): Auto-range setting for the capacitance measurement. Acceptable values include 0, 1, 'ON', 'OFF', 'ONCE'.
            calibrate (bool, optional): If True, perform calibration before measurement. Only valid for 1nF and 10nF ranges.
        """
        cmd = f'CONFigure:CAPacitance'
        cmd += self._validate_range(range)
        self.write(cmd)
        if auto_range is not None:
            if auto_range not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto_range value: '{auto_range}'. Must be one of 0, 1, 'ON', 'OFF', 'ONCE'.")
            cmd_auto_range = f'SENSe:CAPacitance:RANGe:AUTO {auto_range}'
            self.write(cmd_auto_range)
        if calibrate:
            self.write('SENSe:CAPacitance:CABLe:CALibratoin')

    def configure_disp2_off(self) -> None:
        """Turns the second display function off.
        """
        self.write('CONFigure2:OFF')

    def configure_continuity(self, thr: int = 10, res: str = None, nplc: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets measurement to Continuity on the first display and specifies the related parameters.

        Args:
            thr (int): Continuity threshold in ohms, 0 ~ 1000.
            res (str, optional): Continuity measurement resolution. Acceptable values include a numeric value, 'MIN', 'MAX', or 'DEF' (DEF is for GDM-906X).
            nplc (str, optional): Integration time in PLCs (power line cycles). Acceptable values include a numeric value, 'MIN', 'MAX', or 'DEF'. (For GDM-906X)
            trig_delay (str, optional): Trigger delay that minimum step is microseconds. Acceptable values include a numeric value, 'MIN', 'MAX', or 'DEF'. (For GDM-906X)
            auto_zero (int or str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'. (For GDM-906X)
        """
        self.write('CONFigure:CONTinuity')
        cmd = f'SENSe:CONTinuity:THReshold {thr}'
        self.write(cmd)
        if res is not None:
            if res not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid resolution value: '{res}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            cmd_res = f'SENSe:CONTinuity:RESolution {res}'
            self.write(cmd_res)
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            cmd_nplc = f'SENSe:CONTinuity:NPLCycles {nplc}'
            self.write(cmd_nplc)
        if trig_delay is not None:
            if trig_delay not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(trig_delay)
                except ValueError:
                    raise ValueError(f"Invalid trigger delay value: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            cmd_trig_delay = f'SENSe:CONTinuity:TRIGger:DELay {trig_delay}'
            self.write(cmd_trig_delay) 
        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero value: '{auto_zero}'. Must be one of 0, 1, 'ON', 'OFF', or 'ONCE'.")
            cmd_auto_zero = f'SENSe:CONTinuity:ZERO:AUTO {auto_zero}'
            self.write(cmd_auto_zero)  
        

    def configure_diode(self, res: str = None, nplc: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets measurement to Diode on the first display and specifies the related parameters.

        Args:
            res (str, optional): Diode measurement resolution. Acceptable values include a numeric value, 'MIN', or 'MAX'', or 'DEF' (DEF is for GDM-906X).
            nplc (str, optional): Integration time in PLCs (power line cycles). Acceptable values include a numeric value, 'MIN', 'MAX', or 'DEF'. (For GDM-906X)
            trig_delay (str, optional): Trigger delay that minimum step is microseconds. Acceptable values include a numeric value (0 ~ 3600 s), 'MIN', 'MAX', or 'DEF'. (For GDM-906X)
            auto_zero (int or str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'. (For GDM-906X)
        """
        self.write('CONFigure:DIODe')
        if res is not None:
            if res not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid resolution value: '{res}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd_res = f'SENSe:DIODe:RESolution {res}'
            self.write(cmd_res)
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            cmd_nplc = f'SENSe:DIODe:NPLCycles {nplc}'
            self.write(cmd_nplc) 
        if trig_delay is not None:
            if trig_delay not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(trig_delay)
                    if not (0 <= float(trig_delay) <= 3600):
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Invalid trigger delay value: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value between 0 and 3600 seconds.")
            cmd_trig_delay = f'SENSe:DIODe:TRIGger:DELay {trig_delay}'
            self.write(cmd_trig_delay)
        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero value: '{auto_zero}'. Must be one of 0, 1, 'ON', 'OFF', or 'ONCE'.")
            cmd_auto_zero = f'SENSe:DIODe:ZERO:AUTO {auto_zero}'
            self.write(cmd_auto_zero)

    def configure_TCUP(self, sensor: str = '', rjunction: float = None, res: str = None) -> None:
        """Sets measurement to Temperature thermocouple (T-CUP) on the first display and specifies sensor type, along with related coefficients.

        Args:
            sensor (str, optional): Thermocouple type, one of 'B', 'E', 'J', 'K', 'N', 'R', 'S', or 'T'.
            rjunction (float, optional): Simulated junction temperature value (0.00 ~ 50.00), default value is 23.00.
            res (str, optional): Thermocouple resolution. Acceptable values include 'MIN', 'MAX', or a specific numeric value.
        """
        if sensor not in ['', 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T']:
            raise ValueError("Invalid sensor type. Must be one of '', 'B', 'E', 'J', 'K', 'N', 'R', 'S', or 'T'.")

        cmd = f'CONFigure:TEMPerature:TCOuple {sensor}'
        self.write(cmd)

        if rjunction is not None:
            if not (0.00 <= rjunction <= 50.00):
                raise ValueError("The rjunction must be between 0.00 and 50.00.")
            cmd = f'SENSe:TEMPerature:RJUNction:SIMulated {rjunction:.2f}'
            self.write(cmd)
        if res is not None:
            if res not in ['MIN', 'MAX']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid resolution value: '{res}'. Must be 'MIN', 'MAX', or a numeric value.")
            self.write(f'SENSe:TEMPerature:TCOuple:RESolution {res}')    
    
    def configure_FRTD(self, sensor: str = '', alpha: float = None, beta: float = None, delta: float = None, res: str = None, R0: str = None) -> None:
        """Sets measurement to 4W RTD on the first display and specifies sensor type, along with related coefficients.

        Args:
            sensor (str, optional): RTD Type, one of 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.
            alpha (float, optional): RTD Alpha coefficient, range is 0 to 10, default value is 0.00385.
            beta (float, optional): RTD BETA coefficient, range is 0 to 10, default value is 0.10863.
            delta (float, optional): RTD DELTa coefficient, range is 0 to 10, default value is 1.49990.
            res (str, optional): 4W RTD resolution. Acceptable values include 'MIN', 'MAX', or a specific numeric value.
            R0 (str, optional): Reference resistance (R0) of 4-wire RTD measurement. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value (80.0~120.0). (For GDM-906X)
        """
        if sensor not in ['', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER']:
            raise ValueError("Invalid sensor type. Must be one of '', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.")
        cmd = f'CONFigure:TEMPerature:FRTD {sensor}'
        self.write(cmd)
        if sensor == 'USER':
            if alpha is not None:
                cmd = f'SENSe:TEMPerature:FRTD:ALPHa {alpha}'
                self.write(cmd)
            if beta is not None:     
                cmd = f'SENSe:TEMPerature:FRTD:BETA {beta}'
                self.write(cmd)
            if delta is not None: 
                cmd = f'SENSe:TEMPerature:FRTD:DELTa {delta}'
                self.write(cmd)  
        if res is not None:
            if res not in ['MIN', 'MAX']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid resolution value: '{res}'. Must be 'MIN', 'MAX', or a numeric value.")
            self.write(f'SENSe:TEMPerature:FRTD:RESolution {res}')
        if R0 is not None:
            if R0 not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(R0)
                except ValueError:
                    raise ValueError(f"Invalid R0 value: '{R0}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (80.0~120.0).")
            self.write(f'SENSe:TEMPerature:FRTD:RESistance:REFerence {R0}')

    def configure_RTD(self, sensor: str = '', alpha: float = None, beta: float = None, delta: float = None, res: str = None, R0: str = None) -> None:
        """Sets measurement to 2W RTD on the first display and specifies sensor type, along with related coefficients.

        Args:
            sensor (str, optional): RTD Type, one of 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.
            alpha (float, optional): RTD Alpha coefficient, range is 0 to 10, default value is 0.00385.
            beta (float, optional): RTD BETA coefficient, range is 0 to 10, default value is 0.10863.
            delta (float, optional): RTD DELTa coefficient, range is 0 to 10, default value is 1.49990.
            res (str, optional): 2W RTD resolution. Acceptable values include 'MIN', 'MAX', or a specific numeric value.
            R0 (str, optional): Reference resistance (R0) of 2-wire RTD measurement. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value (80.0~120.0). (For GDM-906X)
        """
        if sensor not in ['', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER']:
            raise ValueError("Invalid sensor type. Must be one of '', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.")
        cmd = f'CONFigure:TEMPerature:RTD {sensor}'
        self.write(cmd)
        if sensor == 'USER':
            if alpha is not None:
                cmd = f'SENSe:TEMPerature:RTD:ALPHa {alpha}'
                self.write(cmd)
            if beta is not None:    
                cmd = f'SENSe:TEMPerature:RTD:BETA {beta}'
                self.write(cmd)
            if delta is not None:    
                cmd = f'SENSe:TEMPerature:RTD:DELTa {delta}'
                self.write(cmd)
        if res is not None:
            if res not in ['MIN', 'MAX']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid resolution value: '{res}'. Must be 'MIN', 'MAX', or a numeric value.")
            self.write(f'SENSe:TEMPerature:RTD:RESolution {res}')
        if R0 is not None:
            if R0 not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(R0)
                except ValueError:
                    raise ValueError(f"Invalid R0 value: '{R0}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (80.0~120.0).")
            self.write(f'SENSe:TEMPerature:RTD:RESistance:REFerence {R0}')

    def configure_temperature(self, probe: str = None, sensor: str = None, res: str = None, nplc: str = None) -> None:
        """Sets measurement to Temperature on the 1st display and specifies type/resolution. (For GDM-906X)

        Args:
            probe (str, optional): probe type, one of 'TCOuple', 'RTD', 'FRTD', 'THERmistor', 'FTHermistor'.
            sensor (str, optional): Sensor type, varies based on the probe type.
                TCOuple: 'J', 'K', 'N', 'R', 'S', 'T', 'B', 'E', 'USER'
                RTD / FRTD: 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'
                Thermistor / Fthermistor: '2.2kΩ', '5kΩ', '10kΩ', 'USER'
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.
            nplc (str, optional): Integration time in PLCs. Acceptable values include 'MIN', 'MAX', 'DEF', or a specific numeric value (1, 3, or 12).
        """
        cmd = f'CONFigure:TEMPerature'
        if probe is not None:
            if probe not in ['TCOuple', 'RTD', 'FRTD', 'THERmistor', 'FTHermistor']:
                raise ValueError(f"Invalid probe type: '{probe}'. Must be one of 'TCOuple', 'RTD', 'FRTD', 'THERmistor', or 'FTHermistor'.")
            cmd += f' {probe}'

            valid_sensor = {
                'TCOuple': ['J', 'K', 'N', 'R', 'S', 'T', 'B', 'E', 'USER'],
                'RTD': ['PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'],
                'FRTD': ['PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'],
                'Thermistor': ['2.2kΩ', '5kΩ', '10kΩ', 'USER'],
                'Fthermistor': ['2.2kΩ', '5kΩ', '10kΩ', 'USER']
            }

            if sensor is not None:
                if sensor not in valid_sensor.get(probe, []):
                    raise ValueError(f"Invalid sensor type: '{sensor}' for probe type '{probe}'. Must be one of {valid_sensor[probe]}.")
                cmd += f',{sensor}'

            if res is not None:
                if res not in ['DEF', 'MIN', 'MAX']:
                    try:
                        float(res)
                    except ValueError:
                        raise ValueError(f"Invalid res value: '{res}'. Must be 'DEF', 'MIN', 'MAX', or a numeric value.")
                cmd += f',1,{res}'
        self.write(cmd)
        if nplc is not None:
            if nplc not in ['MIN', 'MAX', 'DEF']:
                try:
                    float(nplc)
                except ValueError:
                    raise ValueError(f"Invalid NPLC value: '{nplc}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            self.write(f'SENSe:TEMPerature:NPLCycles {nplc}')

    def measure_DCV(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the DC voltage measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            DCV (float): DC voltage value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:VOLTage:DC?' if disp == 1 else f'MEASure{disp}:VOLTage:DC?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_DCV_ratio(self, range: str = None, res: str = None) -> float:
        """Returns the DC ratio measurement on the 1st display.

        Args:
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            DC ratio (float): DC ratio value.
        """
        cmd = 'MEASure:VOLTage:DC:RATio?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_ACV(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the AC voltage measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            ACV (float): AC voltage value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:VOLTage:AC?' if disp == 1 else f'MEASure{disp}:VOLTage:AC?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_DCI(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the DC current measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Current range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            DCI (float): DC current value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:CURRent:DC?' if disp == 1 else f'MEASure{disp}:CURRent:DC?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_ACI(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the AC current measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Current range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            ACI (float): AC current value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:CURRent:AC?' if disp == 1 else f'MEASure{disp}:CURRent:AC?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_resistance(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the 2W resistance measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Resistance range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            resistance (float): 2W resistance value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:RESistance?' if disp == 1 else f'MEASure{disp}:RESistance?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_4W_resistance(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the 4W resistance measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Resistance range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            resistance (float): 4W resistance value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:FRESistance?' if disp == 1 else f'MEASure{disp}:FRESistance?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_frequency(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the frequency measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            frequency (float): Frequency value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:FREQuency?' if disp == 1 else f'MEASure{disp}:FREQuency?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)

    def measure_period(self, disp: int = 1, range: str = None, res: str = None) -> float:
        """Returns the period measurement on the specified display.

        Args:
            disp (int): Display number, 1 for the first display, 2 for the second display.
            range (str, optional): Voltage range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            period (float): Period value.
        """
        self._validate_disp(disp)
        cmd = f'MEASure:PERiod?' if disp == 1 else f'MEASure{disp}:PERiod?'
        cmd += self._validate_range(range)
        cmd += self._validate_resolution(res)
        return self.query(cmd)
    
    def measure_capacitance(self, range: str = None) -> float:
        """Returns the capacitance measurement value on the 1st display. (For GDM-906X)

        Args:
            range (str, optional): Capacitance range for the measurement. Acceptable values include 'AUTO', 'DEF' (both for autoranging), 'MIN', 'MAX', or a specific numeric value.

        Returns:
            capacitance (float): Capacitance measurement value.
        """
        cmd = 'MEASure:CAPacitance?'
        cmd += self._validate_range(range)
        return self.query(cmd)

    def measure_continuity(self) -> float:
        """Returns the continuity measurement on the first display.

        Returns:
            continuity (float): Continuity in ohms.
        """
        return self.query('MEASure:CONTinuity?')

    def measure_diode(self) -> float:
        """Returns the diode measurement on the first display.

        Returns:
            diode (float): Diode voltage value.
        """
        return self.query('MEASure:DIODe?')

    def measure_TCUP(self, sensor: str = '') -> float:
        """Returns the temperature for the selected thermocouple type on the first display.

        Args:
            sensor (str, optional): Thermocouple type, one of 'B', 'E', 'J', 'K', 'N', 'R', 'S', or 'T'.

        Returns:
            temperature (float): Temperature value.
        """
        if sensor not in ['', 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T']:
            raise ValueError("Invalid sensor type. Must be one of '', 'B', 'E', 'J', 'K', 'N', 'R', 'S', or 'T'.")
        cmd = f'MEASure:TEMPerature:TCOuple? {sensor}'
        return self.query(cmd)

    def measure_FRTD(self, sensor: str = '') -> float:
        """Returns the 4W RTD temperature for the selected sensor type on the first display.

        Args:
            sensor (str, optional): RTD Type, one of 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.

        Returns:
            temperature (float): Temperature value.
        """
        if sensor not in ['', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER']:
            raise ValueError("Invalid sensor type. Must be one of '', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.")
        cmd = f'MEASure:TEMPerature:FRTD? {sensor}'
        return self.query(cmd)

    def measure_RTD(self, sensor: str = '') -> float:
        """Returns the 2W RTD temperature for the selected sensor type on the first display.

        Args:
            sensor (str, optional): RTD Type, one of 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.

        Returns:
            temperature (float): Temperature value.
        """
        if sensor not in ['', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER']:
            raise ValueError("Invalid sensor type. Must be one of '', 'PT100', 'D100', 'F100', 'PT385', 'PT3916', or 'USER'.")
        cmd = f'MEASure:TEMPerature:RTD? {sensor}'
        return self.query(cmd)

    def measure_temperature(self, probe: str = None, sensor: str = None, res: str = None) -> float:
        """Returns the temperature measurement value with the selected probe and type on the 1st display. (For GDM-906X)

        Args:
            probe (str, optional): Probe type, one of 'TCO', 'RTD', 'FRTD', 'THER', 'FTH'.
            sensor (str, optional): Sensor type, varies based on the probe type.
                TCOuple: 'J', 'K', 'N', 'R', 'S', 'T', 'B', 'E'
                RTD / FRTD: 'PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'
                THERmistor / FTHermistor: '2.2kΩ', '5kΩ', '10kΩ', 'USER'
            res (str, optional): Resolution for the measurement. Acceptable values include 'DEF' for default setting value, 'MIN', 'MAX', or a specific numeric value.

        Returns:
            Temperature (float): Temperature measurement value.
        """
        cmd = 'MEASure:TEMPerature?'
        if probe is not None:
            if probe not in ['TCO', 'RTD', 'FRTD', 'THER', 'FTH']:
                raise ValueError(f"Invalid probe type: '{probe}'. Must be one of 'TCO', 'RTD', 'FRTD', 'THER', or 'FTH'.")
            cmd += f' {probe}'

            valid_sensor = {
                'TCO': ['J', 'K', 'N', 'R', 'S', 'T', 'B', 'E'],
                'RTD': ['PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'],
                'FRTD': ['PT100', 'D100', 'F100', 'PT385', 'PT3916', 'USER'],
                'THER': ['2.2kΩ', '5kΩ', '10kΩ', 'USER'],
                'FTH': ['2.2kΩ', '5kΩ', '10kΩ', 'USER']
            }

            if sensor is not None:
                if sensor not in valid_sensor.get(probe, []):
                    raise ValueError(f"Invalid sensor type: '{sensor}' for probe type '{probe}'. Must be one of {valid_sensor[probe]}.")
                cmd += f',{sensor}'

            if res is not None:
                if res not in ['DEF', 'MIN', 'MAX']:
                    try:
                        float(res)
                    except ValueError:
                        raise ValueError(f"Invalid res value: '{res}'. Must be 'DEF', 'MIN', 'MAX', or a numeric value.")
                cmd += f',1,{res}'
        return self.query(cmd)

    def set_refresh_rate(self, rate: str = None) -> None:
        """Sets the detection rate (sample rate).

        Args:
            rate (str): One of 'S' for SLOW, 'M' for MID, or 'F' for FAST.
        """
        if rate not in ['S', 'M', 'F']:
            raise ValueError("Invalid rate. Must be one of 'S', 'M', or 'F'.")
        cmd = f'SENSe:DETector:RATE {rate}'
        self.write(cmd)

    def set_ac_bandwidth(self, bandwidth: int = None) -> None:
        """Sets the AC bandwidth (AC filter).

        Args:
            bandwidth (int): AC bandwidth. Acceptable values are 3, 20, or 200.
        """
        if bandwidth not in [3, 20, 200]:
            raise ValueError(f"Invalid AC bandwidth: '{bandwidth}'. Must be one of 3, 20, or 200.")
        cmd = f'SENSe:DETector:BANDwidth {bandwidth}'
        self.write(cmd)

    def set_digital_filter(self, disp: int = 1, type: str = None, count: str = None, window: str = None, method: str = None, state: str = None) -> None:
        """Sets the digital filter parameters.

        Args:
            disp (int, optional): Display number, 1 for the first display, 2 for the second display (2 for GDM-9261A).
            type (str, optional): Filter type, One of 'MOV' for moving (default), 'REP' for repeating.
            count (str, optional): Filter count a number between 2 and 100, or 'MIN' or 'MAX'. For GDM-9261A, 'DEF' is also valid.
            window (float or str, optional): Filter window, one of 0.01, 0.1, 1, 10, or 'NONE'.
            method (str, optional): Filter window method, 'Measure' or 'Range' (For GDM-9261A).
            state (str, optional): Filter state, 'ON' or 'OFF'. For GDM-9261A, 0 or 1 is also valid.
        """
        self._validate_disp(disp)

        if type is not None:
            if type not in ['MOV', 'REP']:
                raise ValueError(f"Invalid type: '{type}'. Must be one of 'MOV', or 'REP'.")
            cmd_type = f'SENSe:AVERage:TCONtrol{disp if disp == 2 else ""} {type}'
            self.write(cmd_type)
        
        if count is not None:
            if count not in ['MIN', 'MAX', 'DEF'] and not (2 <= int(count) <= 100):
                raise ValueError(f"Invalid count: '{count}'. Must be 'MIN', 'MAX', 'DEF', or a number between 2 and 100")
            cmd_count = f'SENSe:AVERage:COUNt{disp if disp == 2 else ""} {count}'
            self.write(cmd_count)
        
        if window is not None:
            if window not in [0.01, 0.1, 1, 10, 'NONE']:
                raise ValueError(f"Invalid window: '{window}'. Must be one of 0.01, 0.1, 1, 10, or 'NONE'.")
            cmd_window = f'SENSe:AVERage:WINDow{disp if disp == 2 else ""} {window}'
            self.write(cmd_window)

        if method is not None:
            if method not in ['Measure', 'Range']:
                raise ValueError(f"Invalid method: '{method}'. Must be 'Measure' or 'Range'.")
            cmd_method = f'SENSe:AVERage:WINDow:METHod{disp} {method}'
            self.write(cmd_method)
        
        if state is not None:
            if state not in ['ON', 'OFF', 0, 1]:
                raise ValueError(f"Invalid state: '{state}'. Must be one of 'ON', 'OFF', 0, or 1.")
            cmd_state = f'SENSe:AVERage:STATe{disp if disp == 2 else ""} {state}'
            self.write(cmd_state)

    def set_analog_filter(self, state: str = None) -> None:
        """Turns the analog filter On/Off. (For GDM-8261A)

        Args:
            state (str): Filter state, 'ON' or 'OFF'.
        """
        if state not in ['ON', 'OFF']:
            raise ValueError(f"Invalid state: '{state}'. Must be 'ON' or 'OFF'.")
        cmd_state = f'SENSe:FILTer:STATe {state}'
        self.write(cmd_state)

    def set_auto_zero(self, mode: str = None) -> None:
        """Sets the Auto zeroing mode to on, off or once only. (For GDM-8261A)

        Args:
            mode (str): Auto zero mode, one of 'ON', 'OFF', or 'ONCE'.
        """
        if mode not in ['ON', 'OFF', 'ONCE']:
            raise ValueError(f"Invalid mode: '{mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        cmd = f'SENSe:ZERO:AUTO {mode}'
        self.write(cmd)

    def set_auto_gain(self, mode: str = None) -> None:
        """Sets the Auto gain mode to on, off or once only. (For GDM-8261A)

        Args:
            mode (str): Auto gain mode, one of 'ON', 'OFF', or 'ONCE'.
        """
        if mode not in ['ON', 'OFF', 'ONCE']:
            raise ValueError(f"Invalid mode: '{mode}'. Must be 'ON', 'OFF', or 'ONCE'.")
        cmd = f'SENSe:GAIN:AUTO {mode}'
        self.write(cmd)

    def set_current_auto_detect(self, mode: str = None) -> None:
        """Sets the current auto-detect mode on or off for the current functions. (For GDM-8261A)

        Args:
            mode (str): Current auto-detect, 'ON' or 'OFF'.
        """
        if mode not in ['ON', 'OFF']:
            raise ValueError(f"Invalid mode: '{mode}'. Must be 'ON' or 'OFF'.")
        cmd = f'SENSe:CURRent:DETect {mode}'
        self.write(cmd)

    def set_digital_shift(self, mode: str = 'ON') -> None:
        """Sets the Digital Shift function on or off.

        Args:
            mode (str): D-Shift, 'ON' or 'OFF'. Defaults to 'ON'.
        """
        if mode not in ['ON', 'OFF']:
            raise ValueError(f"Invalid mode: '{mode}'. Must be 'ON' or 'OFF'.")
        cmd = f'SENSe:DIGital:SHIFt {mode}'
        self.write(cmd)

    def set_temperature_unit(self, unit: str = None) -> None:
        """Sets the temperature unit.

        Args:
            unit (str): Temperature unit, one of 'C' or 'F'.
        """
        if unit not in ['C', 'F']:
            raise ValueError(f"Invalid unit: '{unit}'. Must be 'C' or 'F'.")
        cmd = f'SENSe:UNIT {unit}'
        self.write(cmd)

    def set_DCV_sense(self, rel_stat: str = None, rel_val: float = None, rel_val_auto: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for DC Voltage measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-1200.0 to 1200.0 V).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
            auto_zero (str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            cmd_rel_stat = f'SENSe:VOLTage:DC:NULL:STATe {rel_stat}'
            self.write(cmd_rel_stat)
            
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-1200.0 <= float_rel_val <= 1200.0):
                    raise ValueError
            except(ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-1200.0 to 1200.0).")
            self.write(f'SENSe:VOLTage:DC:NULL:VALue {rel_val}')
            print(f'SENSe:VOLTage:DC:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:VOLTage:DC:NULL:VALue:AUTO {rel_val_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600).")
            self.write(f'SENSe:VOLTage:DC:TRIGger:DELay {trig_delay}')

        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero mode: '{auto_zero}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:VOLTage:DC:ZERO:AUTO {auto_zero}')

    def set_ACV_sense(self, bandwidth: float = None, rel_stat: str = None, rel_val: float = None, rel_val_auto: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for AC Voltage measurement. (For GDM-906X)

        Args:
            bandwidth (float, optional): AC bandwidth setting. Acceptable values include 3, 20, 200, 'MIN', 'MAX', or 'DEF'.
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-1200.0 to 1200.0 V).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
        """
        if bandwidth is not None:
            if bandwidth not in [3, 20, 200, 'MIN', 'MAX', 'DEF']:
                raise ValueError(f"Invalid AC bandwidth value: '{bandwidth}'. Must be 3, 20, 200, 'MIN', 'MAX', or 'DEF'.")
            self.write(f'SENSe:VOLTage:AC:BANDwidth {bandwidth}')

        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            cmd_rel_stat = f'SENSe:VOLTage:AC:NULL:STATe {rel_stat}'
            self.write(cmd_rel_stat)
            
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-1200.0 <= float_rel_val <= 1200.0):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-1200.0 to 1200.0).")
            self.write(f'SENSe:VOLTage:AC:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:VOLTage:AC:NULL:VALue:AUTO {rel_val_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600). Minimum step is microseconds.")
            self.write(f'SENSe:VOLTage:AC:TRIGger:DELay {trig_delay}')

    def set_DCI_sense(self, rel_stat: str = None, rel_val: float = None, rel_val_auto: str = None, terminals: int = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for DC Current measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-12.0 to 12.0 A).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            terminals (int, optional): Input port for the current function. Acceptable values include 3 or 10 (depending on the model, GDM-9060 : 3 / GDM-9061 : 3 | 10).
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
            auto_zero (str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:CURRent:DC:NULL:STATe {rel_stat}')
        
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-12.0 <= float_rel_val <= 12.0):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-12.0 to 12.0 A).")
            self.write(f'SENSe:CURRent:DC:NULL:VALue {rel_val}')
        
        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:CURRent:DC:NULL:VALue:AUTO {rel_val_auto}')

        if terminals is not None:
            if terminals not in [3, 10]:
                raise ValueError(f"Invalid terminals value: '{terminals}'. Must be 3 or 10.")
            self.write(f'SENSe:CURRent:DC:TERMinals {terminals}')
        
        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600).")
            self.write(f'SENSe:CURRent:DC:TRIGger:DELay {trig_delay}')
        
        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero mode: '{auto_zero}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:CURRent:DC:ZERO:AUTO {auto_zero}')

    def set_ACI_sense(self, bandwidth: str = None, rel_stat: str = None, rel_val: float = None, rel_val_auto: str = None, terminals: int = None, trig_delay: str = None) -> None:
        """Sets the sense parameters for AC Current measurement. (For GDM-906X)

        Args:
            bandwidth (str, optional): AC current bandwidth setting. Acceptable values include 3, 20, 200, 'MIN', 'MAX', or 'DEF'.
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-12.0 to 12.0 A).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            terminals (int, optional): Input port for the current function. Acceptable values include 3 or 10 (depending on the model, GDM-9060 : 3 / GDM-9061 : 3 | 10).
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
        """
        if bandwidth is not None:
            if bandwidth not in [3, 20, 200, 'MIN', 'MAX', 'DEF']:
                raise ValueError(f"Invalid AC bandwidth value: '{bandwidth}'. Must be 3, 20, 200, 'MIN', 'MAX', or 'DEF'.")
            self.write(f'SENSe:CURRent:AC:BANDwidth {bandwidth}')

        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:CURRent:AC:NULL:STATe {rel_stat}')
            
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-12.0 <= float_rel_val <= 12.0):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-12.0 to 12.0 A).")
            self.write(f'SENSe:CURRent:AC:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:CURRent:AC:NULL:VALue:AUTO {rel_val_auto}')

        if terminals is not None:
            if terminals not in [3, 10]:
                raise ValueError(f"Invalid terminals value: '{terminals}'. Must be 3 or 10.")
            self.write(f'SENSe:CURRent:AC:TERMinals {terminals}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600). Minimum step is microseconds.")
            self.write(f'SENSe:CURRent:AC:TRIGger:DELay {trig_delay}')

    def set_resistance_sense(self, rel_stat: str = None, rel_val: str = None, rel_val_auto: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for 2-wire resistance measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-120.0 ~ 120.0 MΩ).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
            auto_zero (str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:RESistance:NULL:STATe {rel_stat}')
            
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-120.0 <= float_rel_val <= 120.0):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-120.0 to 120.0 MΩ).")
            self.write(f'SENSe:RESistance:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:RESistance:NULL:VALue:AUTO {rel_val_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600). Minimum step is microseconds.")
            self.write(f'SENSe:RESistance:TRIGger:DELay {trig_delay}')

        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero mode: '{auto_zero}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:RESistance:ZERO:AUTO {auto_zero}')

    def set_4W_resistance_sense(self, rel_stat: str = None, rel_val: str = None, rel_val_auto: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for 4-wire resistance measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-120.0 ~ 120.0 MΩ).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s). Minimum step is microseconds.
            auto_zero (str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function value: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:FRESistance:NULL:STATe {rel_stat}')
            
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-120.0 <= float_rel_val <= 120.0):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-120.0 to 120.0 MΩ).")
            self.write(f'SENSe:FRESistance:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:FRESistance:NULL:VALue:AUTO {rel_val_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600). Minimum step is microseconds.")
            self.write(f'SENSe:FRESistance:TRIGger:DELay {trig_delay}')

        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero mode: '{auto_zero}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:FRESistance:ZERO:AUTO {auto_zero}')

    def set_frequency_sense(self, rel_stat: str = None, rel_val: str = None, rel_val_auto: str = None, timeout_auto: str = None, trig_delay: str = None) -> None:
        """Sets the sense parameters for Frequency measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-1.2e6 to 1.2e6 Hz).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            timeout_auto (str, optional): Assigns timeout time at the frequency measurement. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s).
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function state: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:FREQuency:NULL:STATe {rel_stat}')
        
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-1.2e6 <= float_rel_val <= 1.2e6):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-1.2e6 to 1.2e6 Hz).")
            self.write(f'SENSe:FREQuency:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:FREQuency:NULL:VALue:AUTO {rel_val_auto}')

        if timeout_auto is not None:
            if timeout_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid timeout auto setting: '{timeout_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:FREQuency:TIMeout:AUTO {timeout_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600).")
            self.write(f'SENSe:FREQuency:TRIGger:DELay {trig_delay}')

    def set_period_sense(self, rel_stat: str = None, rel_val: str = None, rel_val_auto: str = None, timeout_auto: str = None, trig_delay: str = None) -> None:
        """Sets the sense parameters for Period measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-1.2 to 1.2 s).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            timeout_auto (str, optional): Assigns timeout time at the period measurement. Acceptable values include 0, 1, 'ON', or 'OFF'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s).
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function state: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:PERiod:NULL:STATe {rel_stat}')
        
        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-1.2 <= float_rel_val <= 1.2):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-1.2 to 1.2 s).")
            self.write(f'SENSe:PERiod:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:PERiod:NULL:VALue:AUTO {rel_val_auto}')

        if timeout_auto is not None:
            if timeout_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid timeout auto setting: '{timeout_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:PERiod:TIMeout:AUTO {timeout_auto}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600).")
            self.write(f'SENSe:PERiod:TRIGger:DELay {trig_delay}')

    def set_temperature_sense(self, rel_stat: str = None, rel_val: str = None, rel_val_auto: str = None, res: str = None, probe_type: str = None, trig_delay: str = None, auto_zero: str = None) -> None:
        """Sets the sense parameters for Temperature measurement. (For GDM-906X)

        Args:
            rel_stat (str, optional): Relative function state. Acceptable values include 0, 1, 'ON', or 'OFF'.
            rel_val (str, optional): Relative value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-1.0e15 to 1.0e15).
            rel_val_auto (str, optional): Relative value auto on/off. Acceptable values include 0, 1, 'ON', or 'OFF'.
            res (str, optional): Temperature measurement resolution. Acceptable values include 'DEF', 'MIN', 'MAX', or a specific numeric value.
            probe_type (str, optional): Temperature probe type. Acceptable values include 'TC', 'RTD', 'FRTD', 'THER', 'FTH'.
            trig_delay (str, optional): Trigger delay time. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s).
            auto_zero (str, optional): Auto zero mode. Acceptable values include 0, 1, 'ON', 'OFF', or 'ONCE'.
        """
        if rel_stat is not None:
            if rel_stat not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative function state: '{rel_stat}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:TEMPerature:NULL:STATe {rel_stat}')

        if rel_val is not None:
            try:
                float_rel_val = float(rel_val)
                if not (-1.0e15 <= float_rel_val <= 1.0e15):
                    raise ValueError
            except (ValueError, TypeError):
                if rel_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid relative value: '{rel_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-1.0e15 to 1.0e15).")
            self.write(f'SENSe:TEMPerature:NULL:VALue {rel_val}')

        if rel_val_auto is not None:
            if rel_val_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid relative value auto mode: '{rel_val_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:TEMPerature:NULL:VALue:AUTO {rel_val_auto}')
            
        if res is not None:
            if res not in ['DEF', 'MIN', 'MAX']:
                try:
                    float(res)
                except ValueError:
                    raise ValueError(f"Invalid res value: '{res}'. Must be 'DEF', 'MIN', 'MAX', or a numeric value.")
            self.write(f'SENSe:TEMPerature:RESolution {res}')

        if probe_type is not None:
            if probe_type not in ['TC', 'RTD', 'FRTD', 'THER', 'FTH']:
                raise ValueError(f"Invalid probe type: '{probe_type}'. Must be 'TC', 'RTD', 'FRTD', 'THER', or 'FTH'.")
            self.write(f'SENSe:TEMPerature:TRANsducer:TYPE {probe_type}')

        if trig_delay is not None:
            try:
                float_trig_delay = float(trig_delay)
                if not (0 <= float_trig_delay <= 3600):
                    raise ValueError
            except (ValueError, TypeError):
                if trig_delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{trig_delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600).")
            self.write(f'SENSe:TEMPerature:TRIGger:DELay {trig_delay}')

        if auto_zero is not None:
            if auto_zero not in [0, 1, 'ON', 'OFF', 'ONCE']:
                raise ValueError(f"Invalid auto zero setting: '{auto_zero}'. Must be 0, 1, 'ON', 'OFF', or 'ONCE'.")
            self.write(f'SENSe:TEMPerature:ZERO:AUTO {auto_zero}')

    def set_TCUP_sense(self, sim_val: str = None, sim_auto: str = None, sim_auto_offset: str = None) -> None:
        """Sets the thermocouple simulation parameters for Temperature measurement. (For GDM-906X)

        Args:
            sim_val (str, optional): Thermocouple junction simulation temperature value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-20.00 to 80.00).
            sim_auto (str, optional): Auto junction reference temperature. Acceptable values include 0, 1, 'ON', or 'OFF'.
            sim_auto_offset (str, optional): Junction reference temperature adjust value. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (-20.00 to 20.00).
        """
        if sim_val is not None:
            try:
                float_sim_val = float(sim_val)
                if not (-20.00 <= float_sim_val <= 80.00):
                    raise ValueError
            except (ValueError, TypeError):
                if sim_val not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid simulation value: '{sim_val}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-20.00 to 80.00).")
            self.write(f'SENSe:TEMPerature:RJUNction:SIMulated {sim_val}')

        if sim_auto is not None:
            if sim_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid auto simulation setting: '{sim_auto}'. Must be 0, 1, 'ON', or 'OFF'.")
            self.write(f'SENSe:TEMPerature:RJUNction:SIMulated:AUTO {sim_auto}')

        if sim_auto_offset is not None:
            try:
                float_sim_auto_offset = float(sim_auto_offset)
                if not (-20.00 <= float_sim_auto_offset <= 20.00):
                    raise ValueError
            except (ValueError, TypeError):
                if sim_auto_offset not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid auto offset value: '{sim_auto_offset}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (-20.00 to 20.00).")
            self.write(f'SENSe:TEMPerature:RJUNction:SIMulated:AUTO:OFFSet {sim_auto_offset}')

    def set_therm2w_sense(self, a_param: str = None, b_param: str = None, c_param: str = None, sensor: str = None) -> None:
        """Sets the sense parameters for 2-wire Thermistor measurement. (For GDM-906X)

        Args:
            a_param (str, optional): Thermistor A coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            b_param (str, optional): Thermistor B coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            c_param (str, optional): Thermistor C coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            sensor (str, optional): Thermistor sensor type. Acceptable values include 2200 (2.2kΩ), 5000 (5kΩ), 10000 (10kΩ), or 'USER'.
        """
        if a_param is not None:
            if a_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_a_param = float(a_param)
                    if not (0.0 <= float_a_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid A parameter value: '{a_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:THERmistor:APARameter {a_param}')

        if b_param is not None:
            if b_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_b_param = float(b_param)
                    if not (0.0 <= float_b_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid B parameter value: '{b_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:THERmistor:BPARameter {b_param}')

        if c_param is not None:
            if c_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_c_param = float(c_param)
                    if not (0.0 <= float_c_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid C parameter value: '{c_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:THERmistor:CPARameter {c_param}')

        if sensor is not None:
            if sensor not in [2200, 5000, 10000, 'USER']:
                raise ValueError(f"Invalid sensor type: '{sensor}'. Must be 2200, 5000, 10000, or 'USER'.")
            self.write(f'SENSe:TEMPerature:THERmistor:TYPE {sensor}')

    def set_therm4w_sense(self, a_param: str = None, b_param: str = None, c_param: str = None, sensor: str = None) -> None:
        """Sets the sense parameters for 4-wire Thermistor measurement. (For GDM-906X)

        Args:
            a_param (str, optional): Thermistor A coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            b_param (str, optional): Thermistor B coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            c_param (str, optional): Thermistor C coefficient. Acceptable values include 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).
            sensor (str, optional): Thermistor sensor type. Acceptable values include 2200 (2.2kΩ), 5000 (5kΩ), 10000 (10kΩ), or 'USER'.
        """
        if a_param is not None:
            if a_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_a_param = float(a_param)
                    if not (0.0 <= float_a_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid A parameter value: '{a_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:FTHermistor:APARameter {a_param}')

        if b_param is not None:
            if b_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_b_param = float(b_param)
                    if not (0.0 <= float_b_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid B parameter value: '{b_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:FTHermistor:BPARameter {b_param}')

        if c_param is not None:
            if c_param not in ['MIN', 'MAX', 'DEF']:
                try:
                    float_c_param = float(c_param)
                    if not (0.0 <= float_c_param <= 9.999999):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid C parameter value: '{c_param}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0.0~9.999999).")
            self.write(f'SENSe:TEMPerature:FTHermistor:CPARameter {c_param}')

        if sensor is not None:
            if sensor not in [2200, 5000, 10000, 'USER']:
                raise ValueError(f"Invalid sensor type: '{sensor}'. Must be 2200, 5000, 10000, or 'USER'.")
            self.write(f'SENSe:TEMPerature:FTHermistor:TYPE {sensor}')

    def clear_all_calculations(self) -> None:
        """Clears all of the compare results, statistic calculation value, histogram calculation value, and measurement value. (For GDM-906X)
        
        """
        cmd = 'CALCulate:CLEar:IMMediate'
        self.write(cmd)

    def get_uncalculated_data(self) -> str:
        """Returns uncalculated original measurement. (For GDM-906X)
        
        """
        cmd = 'CALCulate:DATA?'
        return self.query(cmd)

    def set_advanced_measurement(self, measurement: str = None) -> None:
        """Sets the Advanced function.

        Args:
            measurement (str): Advanced measurement. 
                For GDM-8261A: one of 'OFF', 'MIN', 'MAX', 'HOLD', 'REL', 'COMP', 'DB', 'DBM', 'STORE', 'AVER', 'MXB', 'INV', 'REF'.
                For GDM-906X: one of 'OFF', 'HOLD', 'DB', 'DBM', 'LIM', 'MXB', 'INV', 'REF'.
        """
        valid_measurements = ['OFF', 'MIN', 'MAX', 'HOLD', 'REL', 'COMP', 'DB', 'DBM', 'STORE', 'AVER', 'MXB', 'INV', 'REF', 'LIM']
        if measurement not in valid_measurements:
            raise ValueError(f"Invalid measurement: '{measurement}'. Must be one of {', '.join(valid_measurements)}.")
        cmd = f'CALCulate:FUNCtion {measurement}'
        self.write(cmd)

    def get_advanced_measurement(self) -> str:
        """Returns the current Advanced function.

        Returns:
            measurement (str): Current advanced measurement.
        """
        return self.query('CALCulate:FUNCtion?')

    def set_advanced_state(self, state: str = None) -> None:
        """Turns the Advanced function on/off.

        Args:
            state (str): Advanced function state, either 'ON' or 'OFF'.
        """
        if state not in ['ON', 'OFF']:
            raise ValueError(f"Invalid state: '{state}'. Must be 'ON' or 'OFF'.")
        cmd = f'CALCulate:STATe {state}'
        self.write(cmd)

    def get_advanced_state(self) -> str:
        """Returns the status of the Advanced function.

        Returns:
            status (str): Advanced function status, either 'ON' or 'OFF'.
        """
        response = self.query('CALCulate:STATe?')
        return 'ON' if response == '1' else 'OFF'
    
    def get_statistic_average(self) -> float:
        """Returns the average value. (For GDM-906X)

        Returns:
            float: The Average value.
        """
        return self.query('CALCulate:AVERage:AVERage?')
    
    def get_statistic_count(self) -> float:
        """Returns the total count of statistics. (For GDM-906X)

        Returns:
            float: The total count of statistics.
        """
        return self.query('CALCulate:AVERage:COUNt?')
    
    def get_statistic_maximum(self) -> float:
        """Returns the maximum value. (For GDM-906X)

        Returns:
            float: The maximum value.
        """
        return self.query('CALCulate:AVERage:MAXimum?')
    
    def get_statistic_minimum(self) -> float:
        """Returns the minimum value. (For GDM-906X)

        Returns:
            float: The minimum value.
        """
        return self.query('CALCulate:AVERage:MINimum?')
    
    def get_statistic_peak_to_peak(self) -> float:
        """Returns the peak to peak value (max value – min value). (For GDM-906X)

        Returns:
            float: The peak to peak value.
        """
        return self.query('CALCulate:AVERage:PTPeak?')
    
    def get_statistic_STDEV(self) -> float:
        """Returns the Standard Deviation value. (For GDM-906X)

        Returns:
            float: The Standard Deviation value.
        """
        return self.query('CALCulate:AVERage:SDEViation?')
    
    def clear_statistic_values(self) -> None:
        """Clears all of the statistic calculation values. (For GDM-906X)
        
        """
        self.write('CALCulate:AVERage:CLEar:IMMediate')

    def set_statistic_calculation_state(self, state: str = None) -> None:
        """Turns the statistic calculation function on or off. (For GDM-906X)

        Args:
            state (int or str): The state to set, must be one of 0, 1, 'ON', 'OFF'.
        """
        if state not in [0, 1, 'ON', 'OFF']:
            raise ValueError(f"Invalid state: '{state}'. Must be one of 0, 1, 'ON', 'OFF'.")
        cmd = f'CALCulate:AVERage:STATe {state}'
        self.write(cmd)

    def get_minimum_measurement(self) -> float:
        """Returns the minimum value from the Max/Min measurement.

        Returns:
            float: Minimum value.
        """
        return self.query('CALCulate:MINimum?')

    def get_maximum_measurement(self) -> float:
        """Returns the maximum value from the Max/Min measurement.

        Returns:
            float: Maximum value.
        """
        return self.query('CALCulate:MAXimum?')

    def set_hold_measurement(self, percentage: float = None) -> None:
        """Sets the percentage threshold for the Hold function.

        Args:
            percentage (float): Percentage threshold, one of 0.01, 0.1, 1, or 10.
        """
        if percentage not in [0.01, 0.1, 1, 10]:
            raise ValueError(f"Invalid percentage threshold: '{percentage}'. Must be one of 0.01, 0.1, 1, or 10.")
        cmd = f'CALCulate:HOLD:REFerence {percentage}'
        self.write(cmd)

    def set_relative_reference(self, reference: str = None) -> None:
        """Sets the reference value for the relative function. (For GDM-8261A)

        Args:
            reference (str): Reference value, one of 'MIN', 'MAX', or a numeric value.
        """
        if reference is not None:
            try:
                float(reference)
            except (ValueError, TypeError):
                if reference not in ['MIN', 'MAX']:
                    raise ValueError(f"Invalid reference value: '{reference}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd = f'CALCulate:REL:REFerence {reference}'
            self.write(cmd)

    def get_relative_reference(self) -> float:
        """Returns the reference value from the relative function. (For GDM-8261A)

        Returns:
            reference (float): Reference value.
        """
        return self.query('CALCulate:REL:REFerence?')

    def clear_compare_results(self) -> None:
        """Clears compare function result counts. (For GDM-906X)
        
        """
        self.write('CALCulate:LIMit:CLEar:IMMediate')

    def get_compare_fail_counts(self) -> tuple:
        """Returns the low and high fail count of the compare function. (For GDM-906X)

        Returns:
            tuple: A tuple containing two integers, the low fail count and the high fail count.
        """
        response = self.query('CALCulate:LIMit:DATA?')
        low_fail_count, high_fail_count = map(int, response.split(','))
        return low_fail_count, high_fail_count

    def set_compare_parameters(self, lower_limit: str = None, upper_limit: str = None, beeper: str = None) -> None:
        """Sets the lower and upper limits and the beeper alarm mode of the compare function.

        Args:
            lower_limit (str): Lower limit value, one of a float number, 'MIN', or 'MAX'.
            upper_limit (str): Upper limit value, one of a float number, 'MIN', or 'MAX'.
            beeper (str): Beeper alarm mode, one of 'OFF', 'PASS', or 'FAIL'.  (For GDM-906X)
        """
        if lower_limit is not None:
            try:
                float(lower_limit)
            except (ValueError, TypeError):
                if lower_limit not in ['MIN', 'MAX']:
                    raise ValueError(f"Invalid lower limit: '{lower_limit}'. Must be a float number, 'MIN', or 'MAX'.")
            cmd_lower = f'CALCulate:LIMit:LOWer {lower_limit}'
            self.write(cmd_lower)
        if upper_limit is not None:
            try:
                float(upper_limit)
            except (ValueError, TypeError):
                if upper_limit not in ['MIN', 'MAX']:
                    raise ValueError(f"Invalid upper limit: '{upper_limit}'. Must be a float number, 'MIN', or 'MAX'.")
            cmd_upper = f'CALCulate:LIMit:UPPer {upper_limit}'
            self.write(cmd_upper)
        if beeper is not None:
            if beeper not in ['OFF', 'PASS', 'FAIL']:
                raise ValueError(f"Invalid beeper mode: '{beeper}'. Must be one of 'OFF', 'PASS', 'FAIL'.")
            cmd_beeper = f'CALCulate:LIMit:BEEPer:MODE {beeper}'
            self.write(cmd_beeper)

    def get_compare_lower_limit(self) -> float:
        """Returns the lower limit of the compare function.

        Returns:
            float: The lower limit value.
        """
        return self.query('CALCulate:LIMit:LOWer?')

    def get_compare_upper_limit(self) -> float:
        """Returns the upper limit of the compare function.

        Returns:
            float: The upper limit value.
        """
        return self.query('CALCulate:LIMit:UPPer?')
    
    def set_compare_state(self, state: str = None) -> None:
        """Sets the status on/off for the compare function. (For GDM-906X)

        Args:
            state (int or str): Status of the compare function, one of 0, 1, 'ON', 'OFF'.
        """
        if state not in [0, 1, 'ON', 'OFF']:
            raise ValueError(f"Invalid state: '{state}'. Must be one of 0, 1, 'ON', 'OFF'.")
        cmd_state = f'CALCulate:LIMit:STATe {state}'
        self.write(cmd_state)

    def set_db_reference(self, reference: str = None, method: str = None) -> None:
        """Sets the reference value and the method for the dB function.

        Args:
            reference (str): Reference value, one of 'MIN', 'MAX', or a numeric value.
                RefMethod:
                    Voltage: (-1200 ~ 1200 V)
                    dBm: (-200.0 ~ 200 dBm)
            method (str): Method for the reference value, one of 'VOLTage' or 'DBM'. (For GDM-906X)
        """
        if reference is not None:
            try:
                float(reference)
            except (ValueError, TypeError):
                if reference not in ['MIN', 'MAX']:
                    raise ValueError(f"Invalid reference value: '{reference}'. Must be 'MIN', 'MAX', or a numeric value.")
            cmd = f'CALCulate:DB:REFerence {reference}'
            self.write(cmd)
        if method is not None:
            if method not in ['VOLTage', 'DBM']:
                raise ValueError(f"Invalid method: '{method}'. Must be 'VOLTage' or 'DBM'.")
            cmd_method = f'CALCulate:DB:REF:METHod {method}'
            self.write(cmd_method)    

    def set_db_reference_auto(self, auto: str = None) -> None:
        """Sets the first measurement as the reference value for dB measurement.

        Args:
            auto (int or str): Auto reference setting, one of 0, 1, 'ON', 'OFF'.
        """
        if auto not in [0, 1, 'ON', 'OFF']:
            raise ValueError(f"Invalid auto reference setting: '{auto}'. Must be one of 0, 1, 'ON', 'OFF'.")   
        cmd = f'CALCulate:SCALe:REFerence:AUTO {auto}'
        self.write(cmd)

    def get_db_reference(self) -> float:
        """Returns the reference voltage from the dB function.

        Returns:
            float: The reference voltage value.
        """
        return self.query('CALCulate:DB:REFerence?')

    def set_dbm_reference(self, reference: str = None) -> None:
        """Sets the resistance value for the dBm function.

        Args:
            reference (str): Reference value. 
                For GDM-8261A: one of 'MIN', 'MAX', or a numeric value.
                For GDM-906X: one of 'MIN', 'MAX', 'DEF', or a numeric value in the range of 
                (2, 4, 8, 16, 50, 75, 93, 110, 124, 125, 135, 150, 250, 300, 500, 600, 800, 900, 1000, 1200, 8000).
        """
        if reference is not None:
            try:
                float(reference)
            except (ValueError, TypeError):
                if reference not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid reference value: '{reference}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value.")
            cmd = f'CALCulate:DBM:REFerence {reference}'
            self.write(cmd)

    def get_dbm_reference(self) -> float:
        """Returns the resistance value from the dBm function.

        Returns:
            float: Resistance value.
        """
        return self.query('CALCulate:DBM:REFerence?')

    def set_store_count(self, count: str = None) -> None:
        """Sets the number of measurement counts that are recorded with the Store measurement function. (For GDM-8261A)

        Args:
            count (str): Number of counts to record, an integer value between 2 and 9999, or 'MIN' or 'MAX'.
        """
        if count is not None:
            try:
                int_count = int(count)
                if int_count < 2 or int_count > 9999:
                    raise ValueError
            except (ValueError, TypeError):
                if count not in ['MIN', 'MAX']:
                    raise ValueError(f"Invalid count: '{count}'. Must be an integer value between 2 and 9999, or 'MIN' or 'MAX'")
            cmd = f'CALCulate:STORe:COUNt {count}'
            self.write(cmd)

    def get_store_count(self) -> int:
        """Returns the number of counts that are recorded with the Store measurement function. (For GDM-8261A)

        Returns:
            int: Number of counts.
        """
        return self.query('CALCulate:STORe:COUNt?')

    def set_average_count(self, count: int = None) -> None:
        """Sets the total number of statistic counts for Statistics Calculations (Analyze Stats). (For GDM-8261A)

        Args:
            count (int): Number of counts, 0 for continuous count, or an integer value between 2 and 100000.
        """
        if count is not None:
            if count != 0 and (count < 2 or count > 100000):
                raise ValueError(f"Invalid count: '{count}'. Must be 0 for continuous, or an integer value between 2 and 100000.")
            cmd = f'CALCulate:AVERage:COUNt {count}'
            self.write(cmd)

    def get_average_count(self, function: int = 2) -> int:
        """Returns the total number of recorded counts. (For GDM-8261A)

        Args:
            function (int, optional): Function for the count query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            int: Total number of counts.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:COUNt? {function}'
            return self.query(cmd)
        
    def get_average_minimum(self, function: int = 2) -> float:
        """Returns the minimum recorded value. (For GDM-8261A)

        Args:
            function (int, optional): Function for the query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            float: Minimum recorded value.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:MINimum? {function}'
            return self.query(cmd)

    def get_average_maximum(self, function: int = 2) -> float:
        """Returns the maximum recorded value. (For GDM-8261A)

        Args:
            function (int, optional): Function for the query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            float: Maximum recorded value.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:MAXimum? {function}'
            return self.query(cmd)

    def get_average_value(self, function: int = 2) -> float:
        """Returns the average recorded value. (For GDM-8261A)

        Args:
            function (int, optional): Function for the query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            float: Average recorded value.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:AVERage? {function}'
            return self.query(cmd)

    def get_average_ptp(self, function: int = 2) -> float:
        """Returns the recorded peak-to-peak value (max value – min value). (For GDM-8261A)

        Args:
            function (int, optional): Function for the query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            float: Peak-to-peak recorded value.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:PTPeak? {function}'
            return self.query(cmd)

    def get_average_sdev(self, function: int = 2) -> float:
        """Returns the recorded Standard Deviation. (For GDM-8261A)

        Args:
            function (int, optional): Function for the query, 0 for Store, 1 for Scan (Route), or 2 for Stats.
            If not provided, defaults to 2 (Stats).

        Returns:
            float: Recorded Standard Deviation.
        """
        if function is not None:
            if function not in [0, 1, 2]:
                raise ValueError(f"Invalid function: '{function}'. Must be 0 (Store), 1 (Scan), or 2 (Stats).")
            cmd = f'CALCulate:AVERage:SDEViation? {function}'
            return self.query(cmd)

    def set_math_m_factor(self, factor: str = None) -> None:
        """Sets the scale factor M for math measurements.

        Args:
            factor (str): Scale factor M, one of 'MIN', 'MAX', or a numeric value.
        """
        if factor is not None:
            if factor not in ['MIN', 'MAX']:
                try:
                    float(factor)
                except ValueError:
                    raise ValueError(f"Invalid factor: '{factor}'. Must be 'MIN', 'MAX', a numeric value.")
            cmd = f'CALCulate:MATH:MMFactor {factor}'
            self.write(cmd)

    def get_math_m_factor(self) -> float:
        """Returns the scale factor M used in the math measurement.

        Returns:
            float: Scale factor M.
        """
        return self.query('CALCulate:MATH:MMFactor?')

    def set_math_b_offset(self, offset: str = None) -> None:
        """Sets the offset factor B for math measurements.

        Args:
            offset (str): Offset factor B, one of 'MIN', 'MAX', or a numeric value.
        """
        if offset is not None:
            if offset not in ['MIN', 'MAX']:
                try:
                    float(offset)
                except ValueError:
                    raise ValueError(f"Invalid offset : '{offset}'. Must be 'MIN', 'MAX', a numeric value.")
            cmd = f'CALCulate:MATH:MBFactor {offset}'
            self.write(cmd)

    def get_math_b_offset(self) -> float:
        """Returns the offset factor B used in the math measurement.

        Returns:
            float: Offset factor B.
        """
        return self.query('CALCulate:MATH:MBFactor?')

    def set_math_percent(self, value: str = None) -> None:
        """Sets the reference value for the Percent function.

        Args:
            value (str): Reference value, one of 'MIN', 'MAX', or a numeric value.
        """
        if value is not None:
            if value not in ['MIN', 'MAX']:
                try:
                    float(value)
                except ValueError:
                    raise ValueError(f"Invalid value: '{value}'. Must be 'MIN', 'MAX', a numeric value.")
            cmd = f'CALCulate:MATH:PERCent {value}'
            self.write(cmd)

    def get_math_percent(self) -> float:
        """Returns the reference value setting for the Percent function.

        Returns:
            float: Reference value.
        """
        return self.query('CALCulate:MATH:PERCent?')
    
    def set_trigger_parameters(self, source: str = None, delay: str = None, auto: str = None, sample_count: str = None, trigger_count: str = None, delay_time_auto: str = None, signal_slope: str = None, eom_slope: str = None) -> None:
        """Sets the trigger parameters including source, delay, auto mode, sample count, trigger count, and auto delay mode.

        Args:
            source (str): Trigger source, one of 'INT' or 'EXT'. For GDM-906X: one of 'IMM', 'EXT', 'BUS'.
            delay (str): Trigger delay time. 
                        For GDM-8261A: one of 'MIN', 'MAX', or a numeric value (0 ~ 9999 ms). 
                        For GDM-906X: one of 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s),  with a minimum step of microseconds.
            auto (str): Trigger auto mode, one of 'ON' or 'OFF'.
            sample_count (str): Number of samples. 
                                For GDM-8261A: one of 'MIN', 'MAX', or a numeric value (1 ~ 9999). 
                                For GDM-906X: one of 'MIN', 'MAX', 'DEF', or a numeric value (1.0 ~ 1000000.0).
            trigger_count (str): Number of trigger counts. 
                                For GDM-8261A: one of 'MIN', 'MAX', or a numeric value (1 ~ 9999).
                                For GDM-906X: one of 'MIN', 'MAX', 'DEF', or a numeric value (1.0 ~ 1000000.0).                    
            delay_time_auto (int or str): Trigger delay time auto mode, one of 0, 1, 'ON', or 'OFF'. (For GDM-906X)
            signal_slope (str): Trigger signal slope, one of 'POS' or 'NEG'. (For GDM-906X)
            eom_slope (str, optional): EOM output signal slope, one of 'POS' or 'NEG'.(For GDM-906X)
        """
        if source is not None:
            if source not in ['INT', 'EXT', 'IMM', 'BUS']:
                raise ValueError(f"Invalid trigger source: '{source}'. Must be one of 'INT' or 'EXT'.")
            self.write(f'TRIGger:SOURce {source}')

        if delay is not None:
            try:
                float_delay = float(delay)
                if not (0 <= float_delay <= 9999):
                    raise ValueError
            except (ValueError, TypeError):
                if delay not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger delay: '{delay}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (0 ~ 3600 s) for GDM-906X, or (0 ~ 9999 ms) for GDM-8261A.")
            self.write(f'TRIGger:DELay {delay}')

        if auto is not None:
            if auto not in ['ON', 'OFF']:
                raise ValueError(f"Invalid trigger auto mode: '{auto}'. Must be one of 'ON' or 'OFF'.")
            self.write(f'TRIGger:AUTO {auto}')

        if sample_count is not None:
            try:
                float_sample_count = float(sample_count)
                if not (1.0 <= float_sample_count <= 1000000.0):
                    raise ValueError
            except (ValueError, TypeError):
                if sample_count not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid sample count: '{sample_count}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (1.0 ~ 1000000.0) for GDM-906X, or (1 ~ 9999) for GDM-8261A.")
            self.write(f'SAMPle:COUNt {sample_count}')

        if trigger_count is not None:
            try:
                float_trigger_count = float(trigger_count)
                if not (1.0 <= float_trigger_count <= 1000000.0):
                    raise ValueError
            except (ValueError, TypeError):
                if trigger_count not in ['MIN', 'MAX', 'DEF']:
                    raise ValueError(f"Invalid trigger count: '{trigger_count}'. Must be 'MIN', 'MAX', 'DEF', or a numeric value (1.0 ~ 1000000.0) for GDM-906X, or (1 ~ 9999) for GDM-8261A.")
            self.write(f'TRIGger:COUNt {trigger_count}')

        if delay_time_auto is not None:
            if delay_time_auto not in [0, 1, 'ON', 'OFF']:
                raise ValueError(f"Invalid trigger delay auto mode: '{delay_time_auto}'. Must be one of 0, 1, 'ON', or 'OFF'.")
            self.write(f'TRIGger:DELay:AUTO {delay_time_auto}')

        if signal_slope is not None:
            if signal_slope not in ['POS', 'NEG']:
                raise ValueError(f"Invalid trigger signal slope: '{signal_slope}'. Must be one of 'POS' or 'NEG'.")
            self.write(f'TRIGger:SLOPe {signal_slope}')
        
        if eom_slope is not None:
            if eom_slope not in ['POS', 'NEG']:
                raise ValueError(f"Invalid EOM slope: '{eom_slope}'. Must be one of 'POS' or 'NEG'.")
            self.write(f'OUTPut:TRIGger:SLOPe {eom_slope}')

    def set_auto_input_impedance(self, auto_imp: str = None) -> None:
        """Sets the Automatic input impedance for DCV mode.

        Args:
            auto_imp (str): Automatic input impedance. Acceptable values include 'ON' or 'OFF'.
        """
        if auto_imp is not None:
            if auto_imp not in ['ON', 'OFF']:
                raise ValueError(f"Invalid auto impedance value: '{auto_imp}'. Must be 'ON' or 'OFF'.")
            cmd_auto_impedance = f'INPut:IMPedance:AUTO {auto_imp}'
            self.write(cmd_auto_impedance)

    def set_display_view(self, view_mode: str = None) -> None:
        """Sets the display form of the measured value.

        Args:
            view_mode (str): Display form, one of 'NUM' (NUMeric), 'HIST' (HISTogram), 'TCH' (TCHart), or 'MET' (METer).
        """
        if view_mode not in ['NUM', 'HIST', 'TCH', 'MET']:
            raise ValueError(f"Invalid view mode: '{view_mode}'. Must be one of 'NUM', 'HIST', 'TCH', or 'MET'.") 
        cmd = f'DISPlay:VIEW {view_mode}'
        self.write(cmd)

    def local_control(self) -> None:
        """Enables local control (front panel control) and disables remote control.
        
        """
        self.write('SYSTem:LOCal')

if __name__ =='__main__':
    pass