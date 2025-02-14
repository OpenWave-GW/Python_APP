# Name: dso_meas.py
#
# Description: Perform automated measurements on the DSO.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

"""Perform automated measurements on the DSO.

Basic signal parameters in both vertical and horizontal dimensions are
calculated using the atuomated measurement functions.

Typical usage example:

.. code-block::
    
    from dso_const import *
    import dso2ke as gds
    
    # Create a Dso instance, myDso, and get connected to it.
    myDso = gds.Dso()
    ret = myDso.connect(host='localhost', port=3000)
    if ret != 0:
        raise ValueError('Socket connection failed.')

    # List all supported measurements in the REPL
    myDso.meas.help()
    
    # Perform automated measurements on input sources.
    vmax = myDso.meas.get_max(kCH1)
    freq = myDso.meas.get_frequency(kCH1)
    phase = myDso.meas.get_phase(kCH1, kCH2)
    vpp_math = myDso.meas.get_vpp(kMATH1)
    
    # Control of active measurements
    myDso.meas.update() # update from current active measurements
    myDso.meas.remove_all() # Clean up all active measurements
    myDso.meas.add(1, 'max', kCH1)
    myDso.meas.add(2, 'phase', kCH1, kCH2)
    phase_diff = myDso.meas._value(2)
    myDso.meas.remove(1)
    
"""
from dso_const import *

__VERSION__ = (0, 1, 0)

_reference_level_units = {
    'percent' :'PERCent',
}

_reference_level_types = [ 'LOW', 'MID', 'MID2', 'HIGH' ]

_DEFAULT_REFERENCE_LEVELS_PERCENT = {
    'LOW' : 10.0,
    'MID' : 50.0,
    'MID2' : 50.0,
    'HIGH' : 90.0,
}

_volt_measures = {
    'amplitude' : 'AMPlitude',
    'mean' : 'MEAN',
    'cyclemean' : 'CMEan',
    'high' : 'HIGH',
    'low' : 'LOW',
    'max' : 'MAXimum',
    'min' : 'MINImum',
    'vpp' : 'PK2pk',
    'rms' : 'RMS',
    'cyclerms' : 'CRMS',
    'area' : 'AREa',
    'cyclearea' : 'CARea',
}

_time_measures = {
    'falltime' : 'FALL',
    'fallovershoot' : 'FOVShoot',
    'fallpreshoot' : 'FPReshoot',
    'frequency' : 'FREQuency',
    '-width' : 'NWIDth',
    '+width' : 'PWIDth',
    '+duty' : 'PDUTy',
    'period' : 'PERiod',
    'risetime' : 'RISe',
    'riseovershoot' : 'ROVShoot',
    'risepreshoot' : 'RPReshoot',
    '+pulse' : 'PPULSE',
    '-pulse' : 'NPULSE',
    '+edge' : 'PEDGE',
    '-edge' : 'NEDGE',
    'flickindexpercent' : 'PFLIcker',
    'flickindex' : 'FLIcker',
}

_delay_measures = {
    'frr' : 'FRRDelay',
    'frf' : 'FRFDelay',
    'ffr' : 'FFRDelay',
    'fff' : 'FFFDelay',
    'lrr' : 'LRRDelay',
    'lrf' : 'LRFDelay',
    'lfr' : 'LFRDelay',
    'lff' : 'LFFDelay',
    'phase' : 'PHAse',
}

_all_measures = [ _volt_measures, _time_measures, _delay_measures ]
_all_supported_soruces = [ kANALOGx, kMATHx ]

def _flatten_all_measures():
    """ Flatten all measures
    """
    x = {}
    for x_meas in _all_measures:
        x.update(x_meas)
    return x

    
def _get_supported_sources():
    """ Get supported sources for measurements 
    """
    x = {}
    for x_src in _all_supported_soruces:
        x.update(x_src)
    return x

    
class MeasureError(Exception):
    pass


class Measure:
    """This module controls the automated measurement function on the DSO.
    """

    def __init__(self, parent = None) -> None:
        if parent is None:
            raise MeasureError(
                (
                    'A parent object of class DsoBasic or'
                    f'its derived class is required.'
                )
            )
        self.write = parent.write
        self.query = parent.query
        self._dso = parent
        self.terminator = '\n'
        Measure.all_measures = _flatten_all_measures()
        Measure.supported_sources = _get_supported_sources()
        self._reset()

    @staticmethod
    def help():
        """ Show all available measurements """
        total = len(Measure.all_measures)
        str_help = f'Available {total} measurements are:\n'
        str_content = '\n'.join([k for _x in _all_measures for k in _x.keys()])
        str_help = f'{str_help}{str_content}'
        print(str_help)
        
    def _reset(self) -> None:
        self.num_measurements = 0
        self.max_measurements = 8
        self.dict_measurements = {}
        
    def _measurement_cmd(self, meas:str, *args, precision:str = None):
        """ Send command regarding a given measurement, and get the result
        accordingly.
        
        Args:
            meas (str): index key for a given measurement defined in
                        dso_meas.Measure.all_measures.
                        
            args (int): source(s) with respect to a given measurement above.
                        See dso_meas.Measure.supported_sources.
            
            precision (str): with 'precise', the measurement, if applicable,
                             returns with additional precision.
                        
        Raises:
            MeasureError: An error occurred parsing the input argument.
        
        """
        param = Measure.all_measures.get(meas)
        if param:
            cmd = None
            source = [ Measure.supported_sources.get(ch) for ch in args ]
            if meas in _delay_measures:
                source = source[:2]
                if all(source) and len(source) == 2:
                    cmd = f':MEASure:SOURce1 {source[0]};:MEASure:SOURce2 {source[1]};:MEASure:{param}?'
                    if precision == 'precise':
                        cmd += ' PRECise'
                    cmd += self.terminator
                else:
                    raise MeasureError(f'Invalid sources : {source}')
            elif source[0]:
                cmd = f':MEASure:SOURce1 {source[0]};:MEASure:{param}?'
                if precision == 'precise':
                    cmd += ' PRECise'
                cmd += self.terminator
            else:
                raise MeasureError(f'Invalid sources : {source[0]}')
            if cmd:
                ret = self.query(cmd)
                try:
                    fvalue = float(ret)
                    return fvalue
                except ValueError:
                    return None
        else:
            raise MeasureError(f'Invalid measurement item : {meas}')
            
    def get_frr(self, *args, precision:str = None):
        return self._measurement_cmd('frr', *args, precision = precision)
        
    def get_frf(self, *args, precision:str = None):
        return self._measurement_cmd('frf', *args, precision = precision)
        
    def get_ffr(self, *args, precision:str = None):
        return self._measurement_cmd('ffr', *args, precision = precision)
        
    def get_fff(self, *args, precision:str = None):
        return self._measurement_cmd('fff', *args, precision = precision)
        
    def get_lrr(self, *args, precision:str = None):
        return self._measurement_cmd('lrr', *args, precision = precision)
        
    def get_lrf(self, *args, precision:str = None):
        return self._measurement_cmd('lrf', *args, precision = precision)
        
    def get_lfr(self, *args, precision:str = None):
        return self._measurement_cmd('lfr', *args, precision = precision)
        
    def get_lff(self, *args, precision:str = None):
        return self._measurement_cmd('lff', *args, precision = precision)
        
    def get_phase(self, *args, precision:str = None):
        return self._measurement_cmd('phase', *args, precision = precision)
        
    def get_max(self, *args, precision:str = None):
        return self._measurement_cmd('max', *args, precision = precision)
        
    def get_min(self, *args, precision:str = None):
        return self._measurement_cmd('min', *args, precision = precision)
        
    def get_high(self, *args, precision:str = None):
        return self._measurement_cmd('high', *args, precision = precision)
        
    def get_low(self, *args, precision:str = None):
        return self._measurement_cmd('low', *args, precision = precision)
        
    def get_amplitude(self, *args, precision:str = None):
        return self._measurement_cmd('amplitude', *args, precision = precision)
        
    def get_vpp(self, *args, precision:str = None):
        return self._measurement_cmd('vpp', *args, precision = precision)
        
    def get_mean(self, *args, precision:str = None):
        return self._measurement_cmd('mean', *args, precision = precision)
        
    def get_rms(self, *args, precision:str = None):
        return self._measurement_cmd('rms', *args, precision = precision)
        
    def get_area(self, *args, precision:str = None):
        return self._measurement_cmd('area', *args, precision = precision)
        
    def get_cyclemean(self, *args, precision:str = None):
        return self._measurement_cmd('cyclemean', *args, precision = precision)
        
    def get_cyclerms(self, *args, precision:str = None):
        return self._measurement_cmd('cyclerms', *args, precision = precision)
        
    def get_cyclearea(self, *args, precision:str = None):
        return self._measurement_cmd('cyclearea', *args, precision = precision)
        
    def get_frequency(self, *args, precision:str = None):
        return self._measurement_cmd('frequency', *args, precision = precision)
        
    def get_period(self, *args, precision:str = None):
        return self._measurement_cmd('period', *args, precision = precision)
        
    def get_falltime(self, *args, precision:str = None):
        return self._measurement_cmd('falltime', *args, precision = precision)
        
    def get_fallovershoot(self, *args, precision:str = None):
        return self._measurement_cmd('fallovershoot', *args, precision = precision)
        
    def get_fallpreshoot(self, *args, precision:str = None):
        return self._measurement_cmd('fallpreshoott', *args, precision = precision)
        
    def get_neg_width(self, *args, precision:str = None):
        return self._measurement_cmd('-width', *args, precision = precision)
        
    def get_pos_width(self, *args, precision:str = None):
        return self._measurement_cmd('+width', *args, precision = precision)
        
    def get_pos_duty(self, *args, precision:str = None):
        return self._measurement_cmd('+duty', *args, precision = precision)
        
    def get_risetime(self, *args, precision:str = None):
        return self._measurement_cmd('risetime', *args, precision = precision)
        
    def get_riseovershoot(self, *args, precision:str = None):
        return self._measurement_cmd('riseovershoot', *args, precision = precision)
        
    def get_risepreshoot(self, *args, precision:str = None):
        return self._measurement_cmd('risepreshoot', *args, precision = precision)
        
    def get_pos_pulse(self, *args, precision:str = None):
        return self._measurement_cmd('+pulse', *args, precision = precision)
        
    def get_neg_pulse(self, *args, precision:str = None):
        return self._measurement_cmd('-pulse', *args, precision = precision)
        
    def get_pos_edge(self, *args, precision:str = None):
        return self._measurement_cmd('+edge', *args, precision = precision)
        
    def get_neg_edge(self, *args, precision:str = None):
        return self._measurement_cmd('-edge', *args, precision = precision)
        
    def get_flickindex_percent(self, *args, precision:str = None):
        return self._measurement_cmd('flickindexpercent', *args, precision = precision)
        
    def get_flickindex(self, *args, precision:str = None):
        return self._measurement_cmd('flickindex', *args, precision = precision)

    def get_reference_levels(self, unit:str = 'percent') -> dict:
        """ Get reference settings for measurements.
        
        Returns:
            _levels (dict) : settings in a dict form.
        
        Raises:
            MeasureError: An error occurred parsing the input argument.
        
        """    
        _unit = _reference_level_units.get(unit)
        if _unit:
            _levels = {}
            for _type in _reference_level_types:
                cmd = f'MEASUrement:REFLevel:{_unit}:{_type}?'
                cmd += self.terminator
                ret = self.query(cmd)
                try:
                    fvalue = float(ret)
                    _levels[_type] = fvalue
                except ValueError:
                    _levels[_type] = None
            return _levels
        else:
            raise MeasureError(f'Invalid unit for ref. levels : {unit}')
            
    def set_reference_levels(self, rlvls:dict,  unit:str = 'percent') -> None:
        """ Setup reference levels in a dict form.
        
        Args:
            rlvls (dict): reference levels
            
            unit (str, optional): unit of reference levels
        
        Raises:
            MeasureError: An error occurred parsing the input argument.

        """
        _unit = _reference_level_units.get(unit)
        if _unit:
            for _type, _set_val in rlvls.items():
                if _set_val:
                    cmd = f'MEASUrement:REFLevel:{_unit}:{_type} {_set_val}'
                    cmd += self.terminator
                    self.write(cmd)
        else:
            raise MeasureError(f'Invalid unit for ref. levels : {unit}')
            
    def reset_reference_levels(self, unit:str = 'percent') -> None:
        """ Set reference levels to defaults.
        
        Args:
            unit (str, optional): unit of reference levels

        Raises:
            MeasureError: An error occurred parsing the input argument.
        """
        if unit == 'percent':
            self.set_reference_levels(_DEFAULT_REFERENCE_LEVELS_PERCENT, unit)
        else:
            raise MeasureError(f'Invalid unit for ref. levels : {unit}')
    
    def is_on(self, item:int) -> bool:
        """ Check state of a given measurement item.
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.        
        
        Returns:
            True if the state of a given measurement is 'ON' else False
        """
        cmd = f':MEASUrement:MEAS{item}:STATE?'
        cmd += self.terminator
        ret = self.query(cmd)
        return True if int(ret) else False
        
    def _get_type(self, item:int) -> str:
        """ Get type of a given measurement item.
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.
        
        Returns:    
            _type (str): index key for a given item defined in
                        dso_meas.Measure.all_measures.        
        
        Raises:
            MeasureError: An error occurred if multiple types are found.
        
        """
        if self.is_on(item):
            cmd = f':MEASUrement:MEAS{item}:TYPe?'
            cmd += self.terminator
            ret = self.query(cmd)
            _type = [ k for k,v in Measure.all_measures.items() if ret in v.upper() ]
            if len(_type) == 1:
                return _type[0]
            elif not _type:
                raise MeasureError(f'{ret} not found.')
            else:
                raise MeasureError(f'{ret} multiple hits:{len(_type)}')
            
    def _get_sources(self, item:int) -> tuple:
        """ Get sources of a give measurement item.
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.
        
        Returns:
            _sources (tuple): A 2-element tuple regardless the state of the given item.
        
        """
        _sources = []
        _prefix = f':MEASUrement:MEAS{item}:'
        for _x in range(2):
            cmd = _prefix + f'SOUrce{_x+1}?'
            cmd += self.terminator
            ret = self.query(cmd)
            _sources.append(ret)
        return tuple(_sources)
        
    def _get(self, item:int) -> dict:
        """ Summerize a give measurement item.
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.
                        
        Returns:
            d (dict): information for a given measurement item.
        
        """
        d = {
            'state' : 1 if self.is_on(item) else 0,
            'type' : self._get_type(item) if self.is_on(item) else None,
            'sources' : self._get_sources(item)
        }
        return d

    
    def _num(self) -> int :
        """ Get total number of active measurement items. """
        tot = [ self.is_on(_x+1) for _x in range(self.max_measurements) ]
        return sum(tot)
        
    def _value(self, item:int) -> float:
        """ Get value of measurement items
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.
            
        Returns:
            _value (float): the value of the given measurement item.

        """
        if self.is_on(item):
            _prefix = f':MEASUrement:MEAS{item}:'
            _value = _prefix + f'VALue?'
            _value += self.terminator
            ret = self.query(_value)
            try:
                _value = float(ret) # Always return a numeric value regardless the state of either channel.
            except ValueError:
                _value = None
            return _value
    
    def remove(self, item:int) -> None:
        """ Remove existing measurment items
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.
        
        Raises:
            MeasureError: An error occurred for non-existed items.
        
        """
        if self.num_measurements > 0:
            if self.dict_measurements.get(item):
                _prefix = f':MEASUrement:MEAS{item}:'
                _state_off = _prefix + f'STATE OFF'
                cmd = _state_off
                cmd += self.terminator
                self.write(cmd)
                del self.dict_measurements[item]
                self.num_measurements -= 1
            else:
                raise MeasureError(f'Invalid measurement item : {item}')
        
    def add(self, item:int, meas:str, *args) -> None:
        """ Add new measurment items or change existing ones.
        
        Args:
            item (int): measurement of interested ranges in 1 to a maximum item,
                        which is 8 by default.

            meas (str): index key for a given measurement defined in
                        dso_meas.Measure.all_measures.
                        
            args (int): source(s) with respect to a given measurement above.
                        See dso_meas.Measure.supported_sources.

        Raises:
            MeasureError: An error occurred parsing the input argument.
        
        """
        if self.num_measurements < self.max_measurements:
            param = Measure.all_measures.get(meas)
            if param:
                _prefix = f':MEASUrement:MEAS{item}:'
                cmd = None
                source = [ Measure.supported_sources.get(ch) for ch in args ]
                if meas in _delay_measures:
                    source = source[:2]
                    if all(source):
                        _sources = (source[0], source[1])
                        _source1 = _prefix + f'SOUrce1 {source[0]};'
                        _source2 = _prefix + f'SOUrce2 {source[1]};'
                        _type = _prefix + f'TYPe {param};'
                        _state_on = _prefix + f'STATE ON'
                        cmd = _source1 + _source2 + _type + _state_on
                        cmd += self.terminator
                    else:
                        raise MeasureError(f'Two sources required.')
                elif source[0]:
                    _sources = (source[0], )
                    _source1 = _prefix + f'SOUrce1 {source[0]};'
                    _type = _prefix + f'TYPe {param};'
                    _state_on = _prefix + f'STATE ON'
                    cmd = _source1 + _type + _state_on
                    cmd += self.terminator
                else:
                    raise MeasureError(f'Invalid sources : {source[0]}')
                if cmd:
                    self.write(cmd)
                    self.dict_measurements[item] = dict(
                                                        sources = _sources,
                                                        type = meas
                                                    )
                    self.num_measurements += 1
            else:
                raise MeasureError(f'Invalid measurement item : {meas}')
        else:
            raise MeasureError(f'Max. item {self.max_measurements} exceeded.')

    def update(self) -> None:
        """ Update the instance with active measurements on the instrument. """
        update_measure(self)
        
    def remove_all(self) -> None:
        """ Remove all active measurements on the instrument. """
        remove_measure_all(self)

        
def remove_measure_all(mobj) -> None:
    """ Remove all active measurements from a instance of Measure.
    
    Args:
        mobj (Measure): target instance for the update.
    
    """
    import dso_meas
    
    if not isinstance(mobj, dso_meas.Measure):
        raise MeasureError(f'Must be a instance of Meaure')

    for _x in range(mobj.max_measurements):
        _sel = _x + 1
        if mobj.is_on(_sel):
            mobj.remove(_sel) 

def update_measure(mobj) -> None:
    """ Update a instance of Measure with active measurements on the instrument.
    
    Args:
        mobj (Measure): target instance for the update.
    
    """
    import dso_meas
    
    if not isinstance(mobj, dso_meas.Measure):
        raise MeasureError(f'Must be a instance of Meaure')

    for _x in range(mobj.max_measurements):
        _sel = _x + 1
        if mobj.is_on(_sel):
            d = mobj._get(_sel)
            sources = (
                k for k,v in mobj.supported_sources.items()
                for _src in d['sources'] if v in _src
            )
            if sources:
                mobj.add(_sel, d['type'], *sources)

       
if __name__ == '__main__':
    """ Command line arguments
    
    Args:
        sys.argv[1] (str, optional): connection string
        
    Examples:
        # Run in local loop-back
            python dso_meas.py
            
        # Run with user's connection
            python dso_meas.py 192.168.1.1:3000
            
        # Run with auto-scanning port
            python dso_meas.py 192.168.1.1
            
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
    
    # List all supported measurements
    # myDso.meas.help()
    
    # Perform automated measurements on input sources.
    freq = myDso.meas.get_frequency(kCH1)
    print(f'Freq({kCH1}) = {freq} Hz')

    vmax = myDso.meas.get_max(kCH1)
    print(f'Max({kCH1}) = {vmax} volt')
    
    phase = myDso.meas.get_phase(kCH1, kCH2)
    print(f'Phase({kCH1},{kCH2}) = {phase} deg.')
    
    frr = myDso.meas.get_frr(kCH1, kCH2)
    print(f'FRR({kCH1},{kCH2}) = {frr} sec.')
    
    # Control of active measurements
    myDso.meas.update() # update with active measurements on the scope
    myDso.meas.remove_all() # Clean up all active measurements
    myDso.meas.add(1, 'max', kCH1)
    myDso.meas.add(2, 'phase', kCH1, kCH2)
    myDso.meas.add(1, 'high', kCH2) # adding an existing one is equivalent to modification
    high_of_kCH2 = myDso.meas._value(1) # Get value of item 1.
    phase_diff = myDso.meas._value(2) 
    myDso.meas.remove(1)

    # Increase all reference levels by 3%
    rlvls = myDso.meas.get_reference_levels()
    rlvls['HIGH'] += 3.0
    rlvls['MID'] += 3.0
    rlvls['MID2'] += 3.0
    rlvls['HIGH'] += 3.0
    myDso.meas.set_reference_levels(rlvls)

    # Set the high level to 95%
    myDso.meas.set_reference_levels({'HIGH' : 95.0}, 'percent')
