# Name: psw.py
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

class Psw():
    """This module can control the PSW.

    It supports USB interface to use SCPI.

    It will scan available instruments on your DSO, then require a Serial Number to specify and connect to it.

    Usage:
    -------
    .. code-block:: python

        import psw
        inst = psw.Psw()
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

    def set_scpi_delay(self, delay:float):
        """Set the SCPI delay

        Args:
            delay (float): delay time
        """
        self.scpi_delay = delay
    
    def __fillModelInfo(self):
        ret = self.query('*idn?')
        self.ModelName = ret.split(',')[1]
        self.SerialNumber = ret.split(',')[2]
        self.max_current = float(self.query('CURR? MAX'))
        self.min_current = float(self.query('CURR? MIN'))
        self.max_voltage = float(self.query('VOLT? MAX'))
        self.min_voltage = float(self.query('VOLT? MIN'))

    def connect(self, SN:str, baudrate:int=115200, timeout:int=3):
        """Connect to the PSW.

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

    def close(self):
        """
        Close the connection.
        """
        if self.com is None:
            return
        self.com.close()

    def write(self, cmd:str):
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

    def idn(self):
        return self.query('*idn?')
    
    def opc(self):
        return self.query('*opc?')

    def ocp(self):
        '''Queries the OCP (over-current protection) level in amps.

        Returns:
            float: current
        '''
        return self.query(':CURR:PROT?')

    def set_ocp(self, current:float):
        '''Sets the OCP (over-current protection) level in amps.
        '''
        cmd=':CURR:PROT %f'%current
        self.write(cmd)

    def set_ocp_on(self):
        '''Turns OCP (over-current protection) on.
        '''
        cmd=':CURR:PROT:STAT 1'
        self.write(cmd)

    def set_ocp_off(self):
        '''Turns OCP (over-current protection) off.
        '''
        cmd=':CURR:PROT:STAT OFF'
        self.write(cmd)

    def is_ocp_on(self):
        '''Returns the OCP (over-current protection) status.
        '''
        ret = self.query(':CURR:PROT:STAT?')
        if '1' in ret:
            return True
        else:
            return False

    def ovp(self):
        '''Queries the overvoltage protection level.

        Returns:
            float: current
        '''
        return self.query(':VOLT:PROT?')

    def set_ovp(self, voltage:float):
        '''Sets the overvoltage protection level.
        '''
        cmd=':VOLT:PROT %f'%voltage
        self.write(cmd)

    def is_on(self):
        '''Returns output status of the instrument.
        '''
        ret = self.query('OUTP?')
        if '1' in ret:
            return True
        else:
            return False

    def set_on(self):
        """Turns the output on.
        """
        self.write(':OUTP ON')

    def set_off(self):
        """Turns the output off.
        """
        self.write(':OUTP OFF')

    def current(self) -> float:
        """Queries the current level in amps.

        Returns:
            float: output current
        """
        return float(self.query('CURR?'))

    def set_current(self, value):
        """Sets the current level in amps.

        Args:
            value : (float) output current level. (str): MAX or MIN
        """
        if isinstance(value, str):
            if 'MAX' in value:
                cmd = 'CURR MAX'
            elif 'MIN' in value:
                cmd = 'CURR MIN'
        else:
            cmd = 'CURR %f'%(value)
        self.write(cmd)

    def voltage(self) -> float:
        """Queries the voltage level in volts.

        Returns:
            float: output voltage
        """
        return self.query('VOLT?')
    
    def set_voltage(self, value):
        """Sets the voltage level in volts.

        Args:
            value : (float) output voltage level. (str): MAX or MIN
        """
        if isinstance(value, str):
            if 'MAX' in value:
                cmd = 'VOLT MAX'
            elif 'MIN' in value:
                cmd = 'VOLT MIN'
        else:
            cmd = 'VOLT %f'%(value)
        self.write(cmd)

    def mode(self) -> str:
        """Returns the output mode.

        Returns:
            str: output mode
        """
        return self.query('OUTPut:MODE?')

    def set_mode(self, mode:int):
        """Sets the PSW output mode.

        Args:
            mode (int): 0:'CVHS',
                1:'CCHS',
                2:'CVLS',
                3:'CCLS',
        """
        s={
            0:'CVHS',
            1:'CCHS',
            2:'CVLS',
            3:'CCLS',
        }
        cmd = ':OUTPut:MODE '+ s[mode]
        self.write(cmd)

    def meas_power(self) -> float:
        """Takes a measurement and returns the average output power

        Returns:
            float: output power
        """
        cmd='MEAS:POW?'
        ret=self.query(cmd)
        return float(ret)

    def meas_voltage(self) -> float:
        """Takes a measurement and returns the average output voltage

        Returns:
            float: output voltage
        """
        cmd='MEAS:VOLT?'
        ret=self.query(cmd)
        return float(ret)

    def meas_current(self) -> float:
        """Takes a measurement and returns the average output current

        Returns:
            float: output current
        """
        cmd='MEAS:CURR?'
        ret=self.query(cmd)
        return float(ret)

    def is_prot_trip(self):
        """Returns the state of the protection circuits (OVP, OCP, OTP).
        """
        ret = self.query(':OUTP:PROT:TRIP?')
        if '1' in ret:
            return True
        else:
            return False

    def clear_prot(self):
        """Clears over-voltage, over-current and overtemperature (OVP, OCP, OTP) protection circuits.
           It also clears the shutdown protection circuit.
        """
        self.write(':OUTP:PROT:CLE')

if __name__ =='__main__':
    pass