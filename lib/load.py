# Name: load.py
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

class Load():
    """This module can control DC Electronic Loads.

    It supports USB interface to use SCPI.

    It will scan available instruments on your DSO, then require a serial number to specify and connect to it.

    Usage:
    -------
    .. code-block:: python

        import load
        inst = load.Load()
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
        self.max_current = 0
        """MAX Current for this instrument. You will get it after connection.
        """
        self.min_current = 0
        """MIN Current for this instrument. You will get it after connection.
        """
        self.max_voltage = 0
        """MAX Voltage for this instrument. You will get it after connection.
        """
        self.min_voltage = 0
        """MIN Voltage for this instrument. You will get it after connection.
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
        self.max_current = float(self.query('CURR? MAX'))
        self.min_current = float(self.query('CURR? MIN'))
        self.max_voltage = float(self.query('VOLT? MAX'))
        self.min_voltage = float(self.query('VOLT? MIN'))

    def connect(self, SN:str, baudrate:int=115200, timeout:int=3) -> int:
        """Connect to the Load.

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
    
    def err(self) -> str:
        return self.query(':SYST:ERR?')

    def ocp(self) -> str:
        '''Query the OCP (over-current protection) settings.

        Returns:
            settings (str, float): trip setting ('LIMIT', 'Load off', or 'OFF'), and contain the over current limit value (if the trip setting is not 'OFF').
        '''
        return self.query(':OCP?')

    def set_ocp_level(self, current:float = 15.75) -> None:
        '''Set the OCP (over-current protection) value in amps.

        Args:
            current (float): current value.
        '''
        cmd = f':OCP {current}'
        self.write(cmd)

    def set_ocp_trip(self, trip:str = 'LIM') -> None:
        '''Set the OCP (over-current protection) trip setting.

        Args:
            trip (str) : LOFF, LIM, or OFF.
        '''
        cmd = f':OCP {trip}'
        self.write(cmd)

    def ovp(self) -> float or str:
        '''Query the OVP settings.

        Returns:
            settings (float, str): over voltage limit value, or 'OFF' for function off.
        '''
        return self.query(':OVP?')

    def set_ovp(self, voltage: float or str = 'MAX') -> None:
        '''Set the OVP setting.

        Args:
            voltage (float, str): over voltage limit value, 'MAX' for function off, 'MIN' for 0V.
        '''
        cmd = f':OVP {voltage}'
        self.write(cmd)

    def is_on(self) -> bool:
        '''Get the status of the load.
        '''
        ret = self.query(':INP?')
        if '1' in ret:
            return True
        else:
            return False

    def set_on(self) -> None:
        """Set to ON in the input configuration of the Load. Sets restart of program, sequence, and OCP test.
        """
        self.write(':INP ON')

    def set_off(self) -> None:
        """Set to OFF in the input configuration of the Load. Sets stop of program, sequence, and OCP test.

        """
        self.write(':INP OFF')

    def meas_current(self) -> float:
        """Query of current measurement.

        Returns:
            float: the current measurement.
        """
        return float(self.query(':MEAS:CURR?'))

    def get_current_CCS(self, level:str = 'A', value:str = None) -> float:
        """Get the current of the CC static mode.

        Args:
            level (str): 'A' value or 'B' value.
            value (str, optional): 'MAX', 'MIN', or None (default).

        Returns:
            float: the current value.
        """
        cmd = f':CURR:V{level}'
        if isinstance(value, str):
            if 'MAX' in value:
                cmd += '? MAX'
            elif 'MIN' in value:
                cmd += '? MIN'
            else:
                cmd += '?'    
        else:
            cmd += '?'
        return float(self.query(cmd))

    def set_current_CCS(self, level:str = 'A', value = None) -> None:
        """Set the current of the CC static mode.

        Args:
            level (str): 'A' value or 'B' value.
            value (str, float): 'MAX', 'MIN', or the current value.
        """
        cmd = f':CURR:V{level}'
        if value is not None:
            if isinstance(value, str):
                if 'MAX' in value:
                    cmd += ' MAX'
                elif 'MIN' in value:
                    cmd += ' MIN'
            else:
                cmd += f' {float(value)}'     
        self.write(cmd)

    def meas_voltage(self) -> float:
        """Query of voltage measurement.

        Returns:
            float: the voltage measurement.
        """
        return float(self.query(':MEAS:VOLT?'))
    
    def get_voltage_CV(self, level:str = 'A', value:str = None) -> float:
        """Get the CV mode voltage or the +CV voltage value.

        Args:
            level (str): 'A' value or 'B' value.
            value (str, optional): 'MAX', 'MIN', or None (default).

        Returns:
            float: the voltage value.
        """
        cmd = f':VOLT:V{level}'
        if isinstance(value, str):
            if 'MAX' in value:
                cmd += '? MAX'
            elif 'MIN' in value:
                cmd += '? MIN'
            else:
                cmd += '?'    
        else:
            cmd += '?'
        return float(self.query(cmd))

    def set_voltage_CV(self, level:str = 'A', value = None) -> None:
        """Set the CV mode voltage or the +CV voltage value.

        Args:
            level (str): 'A' value or 'B' value.
            value : (float) the voltage value of "A Value". (str): 'MAX' or 'MIN'
        """
        cmd = f':VOLT:V{level}'
        if value is not None:
            if isinstance(value, str):
                if 'MAX' in value:
                    cmd += ' MAX'
                elif 'MIN' in value:
                    cmd += ' MIN'
            else:
                cmd += f' {float(value)}'     
        self.write(cmd)

    def mode(self) -> str:
        """Get the operating function of the load.

        Returns:
            str: mode of operation.
        """
        return self.query(':INPut:MODE?')

    def set_mode(self, mode:int) -> None:
        """Set the operating function of the load.

        Args:
            mode (int): 0:'LOAD',
                1:'PROG',
                2:'NSEQ',
                3:'FSEQ',
        """
        s={
            0:'LOAD',
            1:'PROG',
            2:'NSEQ',
            3:'FSEQ',
        }
        cmd = ':INPut:MODE '+ s[mode]
        self.write(cmd)

    def nseq_state(self) -> str:
        """Get the state of the Normal Sequence function.

        Returns:
            state (str) : “ON, {STOP | RUN | PAUSE}”, OFF
        """
        return self.query(':NSEQuence:STATe?')
    
    def set_nseq_state(self, state:str) -> None:
        """Set the state of the Normal Sequence function.

        Args:
            state (str) : OFF, ON, PAUSe, CONTinue, EXT
        """
        cmd = ':NSEQuence:STATe %s' % (state)
        ret = self.write(cmd)

    def get_nseq_para(self) -> str:
        """Get parameters of the Normal Sequence function. 

        Returns:
            parameters (str) : Start:, Seq No:, Memo:, Mode:, Range:, Loop:, Last Load:, Last:, Chain:
        """
        return self.query(':NSEQuence?')
    
    def set_nseq_para(self, start:int = 1, seq_no:int = 1, memo:str = '', mode:str = 'CC', range:str = 'ILVL', loop:str = 'Infinity', last_load:str = 'OFF', last_value:float = 0.0000, chain:str = 'Off') -> None:
        """Set parameters of the Normal Sequence function.

        Args:
            start (int): start sequence number.(1~10)
            seq_no (int): sequence number.(1~10)
            memo (str): note of up to 12 characters. Enclose the string in double quotation marks.
            mode (str): 'CC', 'CR', 'CV', 'CP'
            range (str): 'IHVH', 'IMVH', 'ILVH', 'IHVL', 'IMVL', 'ILVL'
            loop (str, int): loop count.('INFinity' / 0, 1~9999)
            last_load (str): 'ON', 'OFF'
            last_value (float): Last Value after the end.
            chain (int, str): next sequence number (1~10), 'OFF' for No chain.
        """
        cmd = f':NSEQuence {start},{seq_no},"{memo}",{mode},{range},{loop},{last_load},{last_value},{chain}'
        ret = self.write(cmd)

    def get_nseq_data_edit(self) -> str:
        """Get the editing data of normal sequence.

        Returns:
            data (str) : 'Step:, Value:, Time:, LOAD:, TRIG OUT:, RAMP:, PAUSE:'
        """
        return self.query(':NSEQ:EDIT?')
    
    def set_nseq_data_edit(self, step:int = 1, total_step:int = 1, load_value:float = 0.0000, hours:int = 0, minutes:int = 0, seconds:int = 0, milliseconds:int = 0, load_state:str = 'OFF', RAMP:str = 'OFF', trig_out:str = 'OFF', pause:str = 'OFF') -> None:
        """Set the editing data of normal sequence. 

        Args:
            step (int): The edit step number.
            total_step (int): The total number of steps.
            load_value (float): Set a load value of operation mode.
            hours (int): Set hours.
            minutes (int): Set minutes.
            seconds (int): Set seconds.
            milliseconds (int): Set milliseconds.
            load_state (str): 'ON', 'OFF'
            RAMP (str): 'ON', 'OFF'
            trig_out (str): 'ON', 'OFF'
            pause (str): 'ON', 'OFF'
        """
        cmd = f':NSEQ:EDIT {step},{total_step},{load_value},{hours},{minutes},{seconds},{milliseconds},{load_state},{RAMP},{trig_out},{pause}'
        ret = self.write(cmd)

    def get_nseq_edit_point(self) -> str:
        """Get the editing step number of the normal sequence.

        Returns:
            point (str) : The edit step number of the normal sequence, 1~1000.  
        """
        return self.query(':NSEQuence:EDIT:POINt?')
    
    def set_nseq_edit_point(self, point:int = 1) -> None:
        """Set the editing step number of the normal sequence.

        Args:
            point (int): The edit step number of the normal sequence, 1~1000.  
        """
        cmd = f':NSEQuence:EDIT:POINt {point}'
        ret = self.write(cmd)

    def save_nseq(self) -> None:
        """Save program of normal sequence.

        """
        cmd = f':NSEQ:SAVE'
        ret = self.write(cmd)   
    
    def delete_all_nseq(self) -> None:
        """Delete all the steps of the selected normal sequence.
        
        """
        cmd = ':NSEQ:ALL'
        self.write(cmd)

    def meas_power(self) -> float:
        """Query of power measurement.

        Returns:
            float: the power measurement, unit is the watt.
        """
        return float(self.query(':MEAS:POWer?'))

if __name__ =='__main__':
    pass