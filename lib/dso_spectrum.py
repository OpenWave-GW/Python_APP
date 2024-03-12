# Name: dso_spectrum.py
#
# Description: Spectrum mode control on the DSO.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

"""Spectrum mode control on the DSO.

Basic control functions for the spectrum mode.

Typical usage example:

.. code-block::

    import dso2ke as gds
    
    # Create a Dso instance, myDso, and get connected to it.
    myDso = gds.Dso()
    ret = myDso.connect(host='localhost', port=3000)
    if ret != 0:
        raise ValueError('Socket connection failed.')

    # Activate spectrum mode
    myDso.sa.set_spectrum_mode('ON')
    
    # Configure SA parameters: center and span frequency
    myDso.sa.set_freq(10e6)
    myDso.sa.set_span(10e6)
    
    # Exit the spectrum mode
    myDso.sa.set_spectrum_mode('OFF')
    
    myDso.close() # Clean-up
    
"""
__VERSION__ = (0, 0, 0)

SA, XSA1, XSA2 = range(3)
try:
    from micropython import const
    SA = const(0)
    XSA1 = const(1)
    XSA2 = const(2)
except ImportError:
        pass
        
trace_types = {
    'NORMAL' : 0,
    'AVERAGE' : 1,
    'MAXHOLD' : 2,
    'MINHOLD' : 3,
}

_span2rbw_ratios = {
    'RATIO_1K' : 1000,
    'RATIO_2K' : 2000,
    'RATIO_5K' : 5000,
}

_rbw_modes = ('AUTO', 'MANUAL')

kRectWin, kHammingWin, kHanningWin, kBlackmanWin = range(0, 4)

kUnit_db, kUnit_Lin, kUnit_dbm = range(0, 3)

_windows = {
    kRectWin : 'RECTANGULAR',
    kHammingWin : 'HAMMING',
    kHanningWin : 'HANNING',
    kBlackmanWin : 'BLACKMAN',
}

_units = {
    kUnit_db : 'DBV',
    kUnit_Lin : 'LINEAR',
    kUnit_dbm : 'DBM',
}


class Spectrum:
    """This module controls the spectrum analyzer(SA) on the DSO.
    """
    
    def __init__(self, parent = None, max_instances:int = 1) -> None:
        if parent is None:
            raise ValueError('A parent object of class DsoBasic or its derived class is required.')
        self.write = parent.write
        self.query = parent.query
        self._dso = parent
        self.terminator = '\n'
        #: list of str: [ '', '1', '2' ]
        self._id_prefix = [ str(_) for _ in range(max_instances+1) ]
        self._id_prefix[0] = ''
        self.max_instances = max_instances
                
    def _is_valid(self, id:int) -> bool:
        """ Check validility of a SA ID. Applied only for a multi-SA feature.
        
        Args:
            id (int): ranges from 0 to a value of max_instances.
        """
        if id > self.max_instances:
            raise ValueError(f'id exceeded a maximum value of {self.max_instances}.')
            return False
        return True
        
    def _fset(self, param:str, freq:float, _id:int = SA) -> None:
        if self._is_valid(_id):
            cmd = ':SA%s:%s %f' % (self._id_prefix[_id], param, freq)
            cmd += self.terminator
            ret = self.write(cmd)
            
    def _fget(self, param:str, _id:int = SA) -> float:
        if self._is_valid(_id):
            cmd = ':SA%s:%s?' % (self._id_prefix[_id], param)
            cmd += self.terminator
            ret = self.query(cmd)
            return float(ret)
    
    def set_freq(self, freq:float, _id:int = SA) -> None:
        """Set center frequency of a SA instance

        Args:
            freq (float): frequency in Hz
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        """
        self._fset('FREQuency', freq, _id)
    
    def set_span(self, freq:float, _id:int = SA) -> None:
        """Set span frequency of a SA instance

        Args:
            freq (float): frequency in Hz
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        """
        self._fset('SPAN', freq, _id)
            
    def set_start(self, freq:float, _id:int = SA) -> None:
        """Set start frequency of a SA instance

        Args:
            freq (float): frequency in Hz
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        """
        self._fset('START', freq, _id)
            
    def set_stop(self, freq:float, _id:int = SA) -> None:
        """Set stop frequency of a SA instance

        Args:
            freq (float): frequency in Hz
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        """
        self._fset('STOP', freq, _id)
    
    def set_RBW_Manual(self, rbw:float, _id:int = SA) -> None:
        """ Set manual-RBW value
        
        Args:
            rbw (float): manual-RBW value to set
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
        
        """
        if self.is_RBW_Manual(_id):
            self._fset('RBW', rbw, _id)
    
    def set_Span2RBW_Ratio(self, ratio:str, _id:int = SA) -> None:
        """ Set ratio of span over rbw in auto-RBW mode.
        
        Args:
            ratio (str): RATIO_1K, RATIO_2K, or RATIO_5K
            _id (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        """
        if not self.is_RBW_Manual(_id):
            rvalue = _span2rbw_ratios.get(ratio)
            if rvalue:
                cmd = ':SA{0}:SPANRbwratio {1}'.format(self._id_prefix[_id], rvalue)
                cmd += self.terminator
                ret = self.write(cmd)
            else:
                raise ValueError(f'Unknown value:{ratio}.')
                
    def set_scale(self, scale:float, unit:int = kUnit_db, _id:int = SA) -> None:
        """ Scale of spectrum magnitude
        
        Args:
            scale (float): value of scale
            unit (int, optional): unit of the scale, kUnit_db, kUnit_Lin, or kUnit_dbm
            _id (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        """
        if self._is_valid(_id):
            _unit = _units.get(unit)
            if not _unit:
                raise ValueError(f'Invalid unit:{unit}.')
            _prefix = f':SA{self._id_prefix[_id]}'
            _unit = _prefix + f':UNITS {_unit}'
            _scale = _prefix + f':SCALE {scale}'
            cmd = ';'.join([_unit, _scale])
            cmd += self.terminator
            ret = self.write(cmd)
        
    def set_position(self, position:float, _id:int = SA) -> None:
        """ Vertical offset for spectrum traces
        
        Args:
            position (float): set value in unit of Div.
            _id (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        """
        if self._is_valid(_id):
            _prefix = f':SA{self._id_prefix[_id]}'
            cmd = _prefix + f':POSITION {position}'
            cmd += self.terminator
            ret = self.write(cmd)
            
    def set_window(self, window:int = kHanningWin, _id:int = SA) -> None:
        """ Window function for spectrum analysis
        
        Args:
            window(int, optional): Choose one of the following window functions
                to trade-off amplitude accurary and side-lobe reduction.
                
                kRectWin    for Rectangular
                kHammingWin for Hamming 
                kHanningWin for Hann(default)
                kBlackmanWin for Blackman
                
            _id (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
        
        """
        if self._is_valid(_id):
            _window = _windows.get(window)
            if not _window:
                raise ValueError(f'Invalid window:{window}.')
            _prefix = f':SA{self._id_prefix[_id]}'
            cmd = _prefix + f':WINDOW {_window}'
            cmd += self.terminator
            ret = self.write(cmd)
    
    def is_RBW_Manual(self, _id:int = SA) -> bool:
        """ Check for manual-RBW mode
        
        Args:
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        Returns:
            True if manual-RBW mode, False otherwise.
            
        """
        if self._is_valid(_id):
            cmd = ':SA{0}:RBW:MODE?'.format(self._id_prefix[_id])
            cmd += self.terminator
            ret = self.query(cmd)
            try:
                idx = _rbw_modes.index(ret.upper())
                return True if idx else False
            except ValueError:
                raise ValueError(f'Unknown value:{ret}.')

    def get_freq(self, _id:int = SA) -> float:
        """Get center frequency of a SA instance"""
        return self._fget('FREQuency', _id)
        
    def get_span(self, _id:int = SA) -> float:
        """Get span frequency of a SA instance"""
        return self._fget('SPAN', _id)
        
    def get_start(self, _id:int = SA) -> float:
        """Get start frequency of a SA instance"""
        return self._fget('START', _id)
        
    def get_stop(self, _id:int = SA) -> float:
        """Get stop frequency of a SA instance"""
        return self._fget('STOP', _id)
        
    def get_rbw(self, _id:int = SA) -> float:
        """Get RBW of a SA instance"""
        return self._fget('RBW', _id)        
        
    def set_spectrum_mode(self, state:str) -> None:
        """Set state of the spectrum mode

        Args:
            state (str): ON or OFF

        """
        state = state.upper()
        if not state in {'ON', 'OFF'}:
            raise ValueError(f'Invalid value of argument:{state}.')
        cmd = ':SA:STATE %s' % (state)
        cmd += self.terminator
        ret = self.write(cmd)

    def is_spectrum_mode(self) -> bool:
        """Get state of the spectrum mode

        Returns:
            bool: True if present state is the spectrum mode. False otherwise.

        """    
        cmd = ':SA:STATE?'
        cmd += self.terminator
        ret = self.query(cmd)
        assert ret in {'ON', 'OFF'}
        return True if ret == 'ON' else False
        
    def set_state(self, state:str, _id:int = SA) -> None:
        """Set ON/OFF state of a SA instance

        Args:
            state (str): ON or OFF
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        """
        state = state.upper()
        assert state in {'ON', 'OFF'}
        if self._is_valid(_id):
            cmd = ':SA%s:INPut %s' % (self._id_prefix[_id], state)
            cmd += self.terminator
            ret = self.write(cmd)
        
    def get_state(self, _id:int = SA) -> bool:
        """Get ON/OFF state of a SA instance
        
        Args:
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        Returns:
            bool: True for the 'ON' state, False otherwise.

        """
        if self._is_valid(_id):
            cmd = ':SA%s:INPut?' % (self._id_prefix[_id])
            cmd += self.terminator
            ret = self.query(cmd)
            assert ret in {'ON', 'OFF'}
            return True if ret == 'ON' else False
        
    def set_source(self, ch:int, _id:int = SA):
        """Set input source for a SA instance

        Args:
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            source (int): 1:CH1, 2:CH2, and etc.

        """
        if not self._dso.is_ch_support(ch):
            raise ValueError(f'Not supported ch={ch}')
        else:
            if self._is_valid(_id):
                cmd = ':SA%s:SOURce CH%d' % (self._id_prefix[_id], ch)
                cmd += self.terminator
                ret = self.write(cmd)
        
    def get_source(self, _id:int = SA) -> int:
        """Get input source of a SA instance
        
        Args:
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs

        Returns:
            ch (int): 1:CH1, 2:CH2, and etc.

        """
        if self._is_valid(_id):
            cmd = ':SA%s:SOURce?' % (self._id_prefix[_id])
            cmd += self.terminator
            ret = self.query(cmd)
        
            ch = int(ret[-1])
            assert self._dso.is_ch_support(ch)
            return ch

    def set_trace_data_type(self, trace_type:str, _id:int = SA) -> bool:
        """Set trace type before retrieving the trace data

        Args:
            trace_type (str): NORMAL, AVERAGE, MAXHOLD, MINHOLD
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
                       
        Returns:
            True if set successfully. False otherwise.
        """
        if self._is_valid(_id):
            if trace_types.get(trace_type) == None:
                return False
            cmd = ':SA%s:MEMory:SOURce %s' % (self._id_prefix[_id], trace_type)
            cmd += self.terminator
            ret = self.write(cmd)
            return True
        
    def get_trace_data_type(self, _id:int = SA):
        """Get trace data type after set_trace_data_type().

        Args:
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
       
        Returns:
            ret (str): NORMAL, AVERAGE, MAXHOLD, MINHOLD 
            
        """
        if self._is_valid(_id):
            cmd = ':SA%s:MEMory:SOURce?' % (self._id_prefix[_id])
            cmd += self.terminator
            ret = self.query(cmd)
            return ret
         
    def get_trace(self, trace_type:str, _id:int = SA) -> list:
        """Get trace data of a SA instance

        Args:
            trace_type (str): NORMAL, AVERAGE, MAXHOLD, MINHOLD
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        Returns:
            trace_data (list): spectrum data represented in 8-bit wordlength.

        """
        if self._is_valid(_id):
            if self.set_trace_data_type(trace_type, _id):
                try:
                    import dso_math
                    return dso_math._get_waveform(self._dso, 'spectrum', self._id_prefix[_id])
                except ImportError:
                    print(f'import dso_math failed.')

    def set_spectrum_trace(self, trace_type:str, state:str, _id:int = SA) -> None:
        """ Set traces on and off
        
        Args:
            trace_type (str): NORMAL, AVERAGE, MAXHOLD, or MINHOLD
            
            state (str): ON or OFF
            
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        """
        if self._is_valid(_id):
            if trace_types.get(trace_type) is None:
                raise ValueError(f'Invalid trace type:{trace_type}')
            _prefix = ':SELect' if _id == SA else ':SA{0}'.format(self._id_prefix[_id])
            cmd = _prefix + ':{0} {1}'.format(trace_type, state.upper())
            cmd += self.terminator
            ret = self.write(cmd)
    
    def is_spectrum_trace(self, trace_type:str, _id:int = SA) -> bool:
        """ Get display state of a given spectrum trace
        
        Args:
            trace_type (str): NORMAL, AVERAGE, MAXHOLD, or MINHOLD
            
            _id  (int): 0 for single SA(optional) while 1,2, .. and etc for multi-SAs
            
        Returns:
            True if the trace is 'ON'. False otherwise.
            
        """    
        if self._is_valid(_id):
            if trace_types.get(trace_type) is None:
                raise ValueError(f'Invalid trace type:{trace_type}')
            _prefix = ':SELect' if _id == SA else ':SA{0}'.format(self._id_prefix[_id])
            cmd = _prefix + f':{trace_type}?'
            cmd += self.terminator
            ret = self.query(cmd)
            assert ret in {'ON', 'OFF'}
            return True if ret == 'ON' else False

                    
if __name__ == '__main__':
    """ Command line arguments
    
    Args:
        sys.argv[1] (str, optional): connection string
        
    Examples:
        # Run in local loop-back
            python dso_spectrum.py
            
        # Run with user's connection
            python dso_spectrum.py 192.168.1.1:3000
            
        # Run with auto-scanning port
            python dso_spectrum.py 192.168.1.1
            
    """
    _host= 'localhost:3000'
    import sys
    if len(sys.argv) > 1:
        _host = sys.argv[1] 
        
    if _host.index(':'):
        _host, _port = _host.split(':')
        _port = int(_port)
        if not isinstance(_port, int):
            raise ValueError(f'Invalid port no:{_port}')
        if __debug__:
            print(f'Connecting {_host}:{_port}')
    else:
        _port = 0 # Auto-scan mode

    import dso2ke as gds
    myDso = gds.Dso()
    ret = myDso.connect(host=_host, port=_port)
    if ret != 0:
        raise ValueError('Socket connection failed.')

    if not myDso.sa.is_spectrum_mode():
        myDso.sa.set_spectrum_mode('ON')

    # Configure SA parameters: center and span frequency        
    myDso.sa.set_freq(10e6)
    myDso.sa.set_span(10e6)
    
    #myDso.stop()
    
    # Get spectrum trace
    #trace = myDso.sa.get_trace('NORMAL')
    
    #if trace:
    
        
    
    # if myDso.sa.is_spectrum_mode():
        # myDso.sa.set_spectrum_mode('OFF')