# Name: dso_math.py
#
# Description: Perform math operations on the DSO.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

"""Perform math operations on the DSO.

Basic signal processing functions, including dual-waveform math,
FFT, and advanced math.

Typical usage example:

.. code-block::

    import dso2ke as gds
    
    # Create a Dso instance, myDso, and get connected to it.
    myDso = gds.Dso()
    ret = myDso.connect(host='localhost', port=3000)
    if ret != 0:
        raise ValueError('Socket connection failed.')

    myDso.math.set_math_on() # Trun on MATH
    
    # Run dual-waveform math as CH1*CH1
    myDso.math.run_dual_wfrm_math('CH1*CH1')
    myDso.math.set_dual_wfrm_math_scale_and_pos(0.5, 1.0)
    
    # Run FFT with default hann window and decibel output
    myDso.math.run_fft('CH1')
    
    # FFT using hamming window
    myDso.math.run_fft('CH1', window = kHammingWin)
    
    # Run advanced math
    myDso.math.run_advanced_math('CH1+CH1')
    
    myDso.math.set_math_off() # Trun off MATH
    
    myDso.close() # Clean-up
    
"""
__VERSION__ = (0, 0, 0)

kRectWin, kHammingWin, kHanningWin, kBlackmanWin = range(0, 4)
kUnit_db, kUnit_Lin = range(0, 2)
fft_windows = {
    kRectWin : 'RECTANGULAR',
    kHammingWin : 'HAMMING',
    kHanningWin : 'HANNING',
    kBlackmanWin : 'BLACKMAN',
}
fft_units = {
    kUnit_db : 'DB',
    kUnit_Lin : 'LINEAR',
}
dual_wfrm_math_operators = {
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'MUL',
    '/' : 'DIV',
}
kFFT_WINDOWS_DEF = kHanningWin
kFFT_UNITS_DEF =  kUnit_db

class MathError(Exception):
    pass

class Math:
    """This module controls the math function on the DSO.
    """
    def __init__(self, parent = None) -> None:
        if parent is None:
            raise ValueError('A parent object of class DsoBasic or its derived class is required.')
        self.write = parent.write
        self.query = parent.query
        self._dso = parent
        self.terminator = '\n'
        
    def is_math_on(self) -> bool:
        """Check status of MATH display
       
        Returns:
            True if MATH display is 'ON', False otherwise.
            
        """    
        cmd=':MATH:DISPlay?'
        cmd += self.terminator
        ret = self.query(cmd)
        return True if ret.upper() == 'ON' else False
            
    def set_math_on(self) -> None:
        cmd=':MATH:DISPlay ON'
        cmd += self.terminator
        self.write(cmd)
        
    def set_math_off(self) -> None:
        cmd=':MATH:DISPlay OFF'
        cmd += self.terminator        
        self.write(cmd)
        
    def set_dual_wfrm_math_scale_and_pos(self, scale:float, pos:float) -> None:
        """Set dual waveform math scale and position ofsets
        
        Args:
            scale(float) : value per divison
            
            pos(float) :  value in unit of divison

        """
        cmd = f':MATH:DUAL:SCALE {scale};:MATH:DUAL:POSITION {pos}'
        cmd += self.terminator
        self.write(cmd)
        
    def set_fft_scale_and_pos(self, scale:float, pos:float) -> None:
        """Set FFT scale and position ofsets
        
        Args:
            scale(float) : value per divison
            
            pos(float) :  value in unit of divison

        """
        cmd = f':MATH:FFT:SCALE {scale};:MATH:FFT:POSITION {pos}'
        cmd += self.terminator
        self.write(cmd)
                
    def set_advanced_math_scale_and_pos(self, scale:float, pos:float) -> None:
        """Set advanced math scale and position ofsets
        
        Args:
            scale(float) : value per divison
            
            pos(float) :  value in unit of divison

        """
        cmd = f':MATH:ADVANCED:SCALE {scale};:MATH:ADVANCED:POSITION {pos}'
        cmd += self.terminator
        self.write(cmd)        
        
    def run_fft(
        self,
        source:str,
        window:int = kFFT_WINDOWS_DEF,
        unit:int = kFFT_UNITS_DEF
    ):
        """ Run FFT processing
        
        Args:
            source(str) : analog or reference soruce. e.g. 'CH1' or 'REF1'
            window(int, optional) : window function used by FFT.
                                    kRectWin    for Rectangular
                                    kHammingWin for Hamming 
                                    kHanningWin for Hann(default)
                                    kBlackmanWin for Blackman
            unit(int, optional) :  unit of the FFT magnitude
                                    kUnit_db for dB(default)
                                    kUnit_Lin for Linear RMS
        """
        window, unit = fft_windows.get(window), fft_units.get(unit)
        if window is None:
            raise MathError('Window function required.')
        if unit is None:
            raise MathError('Invalid FFT unit.')
        if is_fft_source_valid(source):
            cmd = f':MATH:FFT:SOURCE {source};:MATH:FFT:WINDOW {window};:MATH:FFT:MAG {unit};:MATH:TYPE FFT'
            cmd += self.terminator
            self.write(cmd)
        else:
            raise MathError('Invalid FFT source: {source}.')
        
    def run_dual_wfrm_math(self, equation:str) -> None:
        """ Run dual waveform math
        
        Args:
            equation(str) : equation for the dual waveform math. e.g. 'CH1+CH1'
            
        Raises:
            MathError : error found in the input equation
        
        """
        match = dual_wfrm_math_parser(equation)
        if match is not None:
            try:
                op1, op, op2 = match.group(1), match.group(2), match.group(3)
                # print('{0} {1} {2}'.format(op1, op, op2))
                
                if not is_source_valid(op1):
                    raise MathError('Invalid operand: {op1}.')
                    
                if not is_source_valid(op2):
                    raise MathError('Invalid operand: {op2}.')
                
                _op = op
                op = dual_wfrm_math_operators.get(op)
                if op is not None:
                    cmd = f':MATH:DUAL:SOURCE1 {op1};:MATH:DUAL:OPERATOR {op};:MATH:DUAL:SOURCE2 {op2};:MATH:TYPE DUAL'
                    cmd += self.terminator
                    self.write(cmd)
                else:
                    raise MathError('Invalid operator: {_op}.')
            except IndexError:
                raise MathError('Check input equation for dual waveform math.')
                # matches = ('+', '-', '*', '/') = tuple( dual_wfrm_math_operators.keys() )
                # if any( x in equation for x in matches):
                    # pass
        else:
            raise MathError('Check input equation for dual waveform math.')

    def run_advanced_math(self, equation:str) -> None:
        """ Run advanced math
        
        Args:
            equation(str) : equation for the advanced math.
        
        """
        cmd = f':MATH:DEFINE "{equation}";:MATH:TYPE ADVANCED'
        cmd += self.terminator        
        self.write(cmd)
        
        
def dual_wfrm_math_parser(equation:str):
    """ Parsing an input equation for the dual waveform math
    
    Args:
        equation (str): such as 'CH1+CH2'
    
    Returns:
        match: see examples below.

    Examples :
    
    >>> match = dso_math.dual_wfrm_math_parser('CH1+CH2')
    >>> print([ match.group(i+1) for i in range(3) ])
        ['CH1', '+', 'CH2']    

    """ 
    import re
    regex = re.compile(r'(CH\d|REF\d)([+|-|*|/])(CH\d|REF\d)')
    return regex.search(equation.upper())

    
def is_source_valid(source:str, pattern:str = r'(CH\d|REF\d)') -> bool:
    """ Is the input source matches a given pattern ?
    
    Args:
        source (str) : CH<x> or REF<x>, where <x> ranges from 1 to 4.
        pattern (str, optional): using regular expression
    
    Returns:
        True if source matches the pattern, False otherwise.
        
    Typical usage example:

    .. code-block::
    
        ch1_vld = is_source_valid('CH1')
        ref1_vld = is_source_valid('REF1')
    
    """
    import re
    regex = re.compile(pattern)
    return True if regex.search(source) is not None else False

    
def is_fft_source_valid(source:str) -> bool:
    """ A valid source for FFT processing is CH<x> or REF<x>
    
    Args:
        source(str) : input for FFT analysis
    
    Returns:
        True if the input is supported by FFT. False otherwise.
        
    """
    return is_source_valid(source.upper())

import dso_basic
    
_BLOCK_DATA_SRC = {
    'analog' : ':acq%d:mem?',
    'math' : ':MATH:MEM?',
    'spectrum' : ':SA%s:MEM?',
    #'reference' : '',
    #'digital' : '',
}    
    
def _get_waveform(handle:dso_basic.DsoBasic, source:str, *args) -> list:
    """Get block data from various sources provided by DSO(with just one call).

    Args:
        handle (dso_basic.DsoBasic): handle of the scope instrument
        
        source (str): 'analog', 'spectrum', 'math', and so on as
                    listed in '_BLOCK_DATA_SRC'
            
        *args (optional): Additonal parameters required for commands with
                        repect to different block data sources.
        
    Returns:
        waveform_flat_list (list): waveform data represented in range from 0 to 255.

    Raises:
        ValueError: throw out exception for 'zero-length' data cases.
    
    Typical usage example:
    
    .. code-block::

        from dso_math import _get_waveform
        
        # Get the MATH waveform with
        math_data = _get_waveform(myDso, 'math')
            
        # Get the Spectrum waveform with
        spectrum_data = _get_waveform(myDso, 'sepctrum')
            
        # Get the analogue waveform CH1 with
        ch1_data = _get_waveform(myDso, 'analog', 1)
        
    """
    waveform_chunks = []
    for waveform in _get_waveform_batch(handle, source, *args, chunk_size = 1024):
        waveform_chunks.append(waveform)
    if not waveform_chunks:
        raise ValueError(f'len(waveform_chunks) == {len(waveform_chunks)}')
    waveform_flat_list = [item for chunk in waveform_chunks for item in chunk]
    return  waveform_flat_list

    
def _get_waveform_minmax(handle:dso_basic.DsoBasic, source:str, *args) -> tuple:
    _min, _max = [], []
    for waveform in _get_waveform_batch(handle, source, *args, chunk_size = 1024):
        _min.append( min(waveform) )
        _max.append( max(waveform) )
    
    if _min and _max:
        _minmax = min(_min), max(_max)
    else:
        _minmax = ('None', 'None')

    return _minmax
        

def _get_waveform_batch(handle:dso_basic.DsoBasic, source:str, *args, chunk_size:int = 1024) -> list:
    """Get block data from various sources provided by DSO(with batch or 'chunk-by-chunk' procesing).

    Args:
        handle (dso_basic.DsoBasic): handle to the scope instrument
        
        source (str): 'analog', 'digital', 'math', and so on
            as listed in '_BLOCK_DATA_SRC'
            
        *args (optional): Additonal parameters required for commands with
            repect to different block data sources.
                         
        chunk_size (int, optional): batch size used for reading a block data.
    
    Yields:
        data (list): next slice in size of 'chunk_size' from a whole bunch of data.
    
    Typical usage example:
        
    .. code-block::
    
        # Do some processing on the 'analog:CH1' on a batch basis
        for slice in get_waveform_batch(a socket instance, 'analog', 1, chunk_size=1024):
            do_some_processing(slice)

    """
    if not isinstance(handle, dso_basic.DsoBasic):
        raise ValueError(f'Handle must be a instance of DsoBasic')
        
    import socket
    _socket = handle.s
    if not isinstance(_socket, socket.socket):
        raise ValueError(f'Handle must have a instance of Socket')
    
    terminator = '\n'
    _write_CALL_, _recv_CALL_ = handle.write, _socket.recv
    
    cmd_src = _BLOCK_DATA_SRC.get(source)
    if cmd_src is None:
        return
    # return value data_out is numeric array
    # check header
    cmd = ":header?"
    cmd += terminator
    _write_CALL_(cmd)
    
    header = _recv_CALL_(1024).decode('utf-8')
    # print(header)
    if ('ON' in header):
        pass
    else:
        cmd = ":header ON"
        cmd += terminator
        _write_CALL_(cmd)
    # --------
    # cmd_src = ":acq%d:mem?" % (ch)
    cmd = cmd_src
    if len(args):
        cmd = cmd % args
    if not cmd.endswith('?'):
        raise ValueError(f'cmd must end with a "?"')
        
    cmd += terminator
    _write_CALL_(cmd)
    
    state = 'READ_HEADER'
    header_buffer = b''
    while True:
        if state == 'READ_HEADER':
            info = _recv_CALL_(1)
            if info == b'\n':
                header_buffer += info
                # Parsing header_buffer
                header_buffer = header_buffer.decode('utf-8')
                databit_str = 'Data Bit,'
                try:
                    databit = int(header_buffer[header_buffer.find(databit_str) + len(databit_str)])
                except:
                    databit = 8
                # print(databit)
            elif info == b'#':
                head = _recv_CALL_(1)
                head_d = int(head.decode('utf-8'))
                length = b''
                while True:
                    length += _recv_CALL_(1)
                    if(head_d == len(length)):
                        break
                length = length.decode('utf-8')
                length = int(length) + 1 # '\n'
                state = 'READ_DATA'
            else:
                header_buffer += info
        elif state == 'READ_DATA':
            # read block data waveform
            from struct import unpack
            while length >= chunk_size:
                data = unpack('>%dh' % (chunk_size // 2), _recv_CALL_(chunk_size)) # 0xffe6(=-26) big-endian
                length = length - chunk_size
                yield data
            else:
                if length > 0:
                    length = length -1 # '\n'
                    data = unpack('>%dh' % (length // 2), _recv_CALL_(length))
                    _recv_CALL_(1)
                    yield data
                break

                
if __name__ == '__main__':
    """ Command line arguments

    Args:
        sys.argv[1] (str, optional): connection string
        
    Examples:
        # Run in local loop-back
            python dso_math.py
            
        # Run with user's connection
            python dso_math.py 192.168.1.1:3000
            
        # Run with auto-scanning port
            python dso_math.py 192.168.1.1

            
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
    
    myDso.math.set_math_on()

    run_tests = {
        'dual wfrm math' : [ myDso.math.run_dual_wfrm_math, 'CH1*CH1'],
        'FFT'            : [ myDso.math.run_fft, 'CH1'],
        'advanced math'  : [ myDso.math.run_advanced_math, 'CH1+CH1'],
    }

    import time
    from dso_math import _get_waveform
    for test, [func, *args] in run_tests.items():
        func(*args)
        time.sleep(1.0)
        math_data = _get_waveform(myDso, 'math')
        assert len(math_data) > 0, f'math_data failed : {test}'
        _min, _max, total_samples = min(math_data), max(math_data), len(math_data)

    print('All tests PASSED.\n')

    #myDso.math.set_math_off()
    #myDso.close()

