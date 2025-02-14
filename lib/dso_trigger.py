# Name: dso_trigger.py
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

class Trigger():
    """This module can control the Trigger function on your DSO
    """
    def __init__(self, parent) -> None:
        self.write = parent.write #for DSO SCPI
        self.query = parent.query #for DSO SCPI

    def freq(self) -> float:
        """Queries the trigger frequency.

        Returns:
            float: frequency
        """
        ret = self.query(':TRIGger:FREQuency?')
        return float(ret)

    def type(self) -> str:
        """Queries the trigger type.

        Returns:
            str: EDGE|DELAY|PULSEWIDTH|VIDEO|RUNT|RISEFALL|LOGIC|BUS|TIMEOUT
        """
        cmd=':TRIG:TYP?\n'
        ret = self.query(cmd)
        return ret

    def set_type(self, type:str):
        """Sets the trigger type.

        Args:
            type (str): EDGe|DELay|PULSEWidth|VIDeo|RUNT|RISEFall|LOGic|BUS|TIMEOut
        """
        cmd=':TRIG:TYP %s\n'%type
        self.write(cmd)

    def source(self) -> str:
        """Queries the trigger source.

        Returns:
            str: CH1|CH2|CH3|CH4|EXT|LINE|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15
        """
        cmd=':TRIG:SOUR?\n'
        ret = self.query(cmd)
        return ret

    def set_source(self, src:str):
        """Sets the trigger source.

        Args:
            src (str): CH1|CH2|CH3|CH4|EXT|LINe|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15
        """
        cmd=':TRIG:SOUR %s\n'%src
        self.write(cmd)

    def mode(self) -> str:
        """Queries the trigger mode.

        Returns:
            str: AUTO|NORMAL
        """
        cmd=':TRIG:MOD?\n'
        ret = self.query(cmd)
        return ret

    def set_mode(self, mode:str):
        """Sets the trigger mode.

        Args:
            mode (str): AUTo|NORMal
        """
        cmd=':TRIG:MOD %s\n'%mode
        self.write(cmd)

    def coupling(self) -> str:
        """Queries the trigger coupling.

        Returns:
            str: DC|AC|HF|LF
        """
        cmd=':TRIG:COUP?\n'
        ret = self.query(cmd)
        return ret

    def set_coupling(self, mode:str):
        """Sets the trigger coupling.

        Args:
            mode (str): DC|AC|HF|LF
        """
        cmd=':TRIG:COUP %s\n'%mode
        self.write(cmd)


    def slope(self) -> str:
        """Queries the edge/delay/rise&fall trigger slope.

        Returns:
            str: RISE|FALL|EITHER
        """
        trig_type = self.type()
        if trig_type.lower() in ['edge', 'delay', 'risefall']:
            cmd=':TRIG:%s:SLOP?\n'%trig_type
            ret = self.query(cmd)
            return ret
        else:
            return 'Unsupported trigger type for slope query: %s' % trig_type

    def set_slope(self, type:str):
        """Sets the edge/delay/rise&fall trigger slope.

        Args:
            type (str): RISe|FALL|EITher
        """
        trig_type = self.type()
        if trig_type.lower() in ['edge', 'delay', 'risefall']:
            cmd=':TRIG:%s:SLOP %s\n'%(trig_type,type)
            self.write(cmd)

    def polarity(self) -> str:
        """Queries the pulse width/runt/video trigger polarity.

        Returns:
            str: POSITIVE|NEGATIVE
        """
        trig_type = self.type()
        if trig_type.lower() in ['pulsewidth', 'runt', 'video']:
            cmd=':TRIG:%s:POL?\n'%trig_type
            ret = self.query(cmd)
            return ret
        else:
            return 'Unsupported trigger type for polarity query: %s' % trig_type

    def set_polarity(self, type:str):
        """Sets the pulse width/runt/video trigger polarity.

        Args:
            type (str): POSitive|NEGative
        """
        trig_type = self.type()
        if trig_type.lower() in ['pulsewidth', 'runt', 'video']:
            cmd=':TRIG:%s:POL %s\n'%(trig_type,type)
            self.write(cmd)

    def level(self) -> float:
        """Queries the trigger level.        
           Note: Not applicable to Pulse Runt and Rise & Fall triggers.

        Returns:
            float: trigger level
        """
        cmd=':TRIG:LEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_level(self, value:float):
        """Sets the trigger level.
           Note: Not applicable to Pulse Runt and Rise & Fall triggers.

        Args:
            value (float): trigger level
        """
        cmd=':TRIG:LEV %f\n'%value
        self.write(cmd)


    def hlevel(self) -> float:
        """Queries the high trigger level.        
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Returns:
            float: trigger high level
        """
        cmd=':TRIG:HLEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_hlevel(self, value:float):
        """Sets the high trigger level.
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Args:
            value (float): trigger high level
        """
        cmd=':TRIG:HLEV %f\n'%value
        self.write(cmd)
        
    def llevel(self) -> float:
        """Queries the low trigger level.        
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Returns:
            float: trigger low level
        """
        cmd=':TRIG:LLEV?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_llevel(self, value:float):
        """Sets the low trigger level.
           Note: Applicable for Rise and Fall/Pulse Runt triggers.

        Args:
            value (float): trigger low level
        """
        cmd=':TRIG:LLEV %f\n'%value
        self.write(cmd)


    def external_probe_ratio(self) -> float:
        """Queries the external probe ratio.

        Returns:
            float: external probe ratio
        """
        cmd=':TRIG:EXTER:PROB:RAT?\n'
        ret = self.query(cmd)
        return float(ret)

    def set_external_probe_ratio(self, value:float):
        """Sets the external probe ratio.

        Args:
            value (float): external probe ratio
        """
        cmd=':TRIG:EXTER:PROB:RAT %f\n'%value
        self.write(cmd)

    def is_noise_rejection(self) -> bool:
        cmd = ':TRIGger:NREJ?'
        ret = self.query(cmd)
        if('ON' in ret):
            return True
        else:
            return False

    def set_noise_rejection_on(self):
        """Sets noise rejection on.
        """
        cmd = ':TRIGger:NREJ ON'
        self.write(cmd)

    def set_noise_rejection_off(self):
        """Sets noise rejection off.
        """
        cmd = ':TRIGger:NREJ OFF'
        self.write(cmd)

    def holdoff(self) -> float:
        """Queries the holdoff time.

        Returns:
            float: holdoff time
        """
        cmd = ':TRIGger:HOLDoff?'
        ret = self.query(cmd)
        return float(ret)

    def set_holdoff(self, value:float):
        """Sets the holdoff time.

        Args:
            value (float): holdoff time
        """
        cmd = ':TRIGger:HOLDoff %f'%(value)
        self.write(cmd)

    def bus_type(self) -> str:
        """Returns the current bus type.
        
        Returns:
            str: The current bus type, one of 'UART', 'I2C', 'SPI', 'PARALLEL', 'CAN', or 'LIN'.
        """
        return self.query(':TRIGger:BUS:TYPe?')
    
    def set_bus_threshold(self, ch: int, threshold: float) -> None:
        """Sets the threshold level for the specified channel.

        Args:
            ch (int): The channel number (1 to 4).
            threshold (float): The threshold level to set in volts.
        """
        self.write(f':TRIGger:BUS:THReshold:CH{ch} {threshold}')

    def i2c_trigger_on(self) -> str:
        """Queries the I2C bus trigger condition.

        Returns:
            str: The I2C bus trigger condition.
        """
        return self.query(':TRIGger:BUS:B1:I2C:CONDition?') 
    
    def set_i2c_trigger_on(self, condition: str) -> None:
        """Sets the I2C bus trigger condition.
        
        Args:
            condition (str): The I2C bus trigger condition to set. One of the following:
                - 'STARt' - Start condition.
                - 'STOP' - Stop condition.
                - 'REPEATstart' - Repeated Start condition.
                - 'ACKMISS' - Missing Acknowledgement.
                - 'ADDRess' - Address condition.
                - 'DATA' - Data condition.
                - 'ADDRANDDATA' - Address and Data condition.
        """
        self.write(f':TRIGger:BUS:B1:I2C:CONDition {condition}')

    def set_i2c_address_trigger(self, mode: str = None, type_: str = None, value: str = None, direction: str = None) -> None:
        """Sets the I2C address trigger configuration for the ADDRess or ADDRANDDATA trigger condition.

        Args:
            mode (str, optional): I2C addressing mode, either 'ADDR7' for 7-bit or 'ADDR10' for 10-bit.
            type_ (str, optional): I2C bus address type. One of the following:
                - 'GENeralcall' for a general call address (0000 000 0).
                - 'STARtbyte' for a start byte address (0000 000 1).
                - 'HSmode' for high-speed mode address (0000 1xx x).
                - 'EEPROM' for EEPROM address (1010 xxx x).
                - 'CBUS' for CBUS address (0000 001 x).
            value (str, optional): The I2C bus address value:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a don't care placeholder.
                - Number of characters depends on the mode setting (7 bits for 'ADDR7' or 10 bits for 'ADDR10').
                - **Examples**:
                    - For 7-bit: "xxx0101".
                    - For 10-bit: "xxx1010101".
            direction (str, optional): Data direction, one of 'READ', 'WRITE', or 'NOCARE'.
        """
        if mode is not None:
            self.write(f':TRIGger:BUS:B1:I2C:ADDRess:MODe {mode}')

        if type_ is not None:
            self.write(f':TRIGger:BUS:B1:I2C:ADDRess:TYPe {type_}')

        if value is not None:
            self.write(f':TRIGger:BUS:B1:I2C:ADDRess:VALue "{value}"')

        if direction is not None:
            if direction.upper() not in ['READ', 'WRITE', 'NOCARE']:
                raise ValueError("Invalid value for direction. Must be one of: 'READ', 'WRITE', or 'NOCARE'.")
            self.write(f':TRIGger:BUS:B1:I2C:ADDRess:DIRection {direction}')

    def set_i2c_data_trigger(self, size: int = None, value: str = None) -> None:
        """Sets the I2C data trigger configuration for the DATA or ADDRANDDATA trigger condition.

        Args:
            size (int, optional): Number of data bytes (1 to 5) to set. 
            value (str, optional): The triggering data value:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 8).
                - **Example**: 
                    - For size 1 (8 bits): "1x1x0101".
                    - For size 3 (24 bits): "1x1x0101010010110010xxxx".
        """
        if size is not None:
            if size < 1 or size > 5:
                raise ValueError('Size must be between 1 and 5.')
            self.write(f':TRIGger:BUS:B1:I2C:DATa:SIZe {size}')

        if value is not None:
            self.write(f':TRIGger:BUS:B1:I2C:DATa:VALue "{value}"')

    def uart_trigger_on(self) -> str:
        """Queries the UART bus trigger condition.

        Returns:
            str: The UART bus trigger condition.
        """
        return self.query(':TRIGger:BUS:B1:UART:CONDition?') 

    def set_uart_trigger_on(self, condition: str) -> None:
        """Sets the UART bus trigger condition.

        Args:
            condition (str): The UART bus trigger condition to set. One of the following:
                - 'RXSTArt': Trigger on the RX Start Bit.
                - 'RXDATA': Trigger on RX Data.
                - 'RXENDPacket': Trigger on the RX End of Packet condition.
                - 'RXPARItyerr': Trigger on RX Parity error condition.
                - 'TXSTArt': Trigger on the TX Start Bit.
                - 'TXDATA': Trigger on TX Data.
                - 'TXENDPacket': Trigger on the TX End of Packet condition.
                - 'TXPARItyerr': Trigger on TX Parity error condition.
        """
        self.write(f':TRIGger:BUS:B1:UART:CONDition {condition}')

    def set_uart_rx_data_trigger(self,  size: int = None, value: str = None) -> None:
        """Sets the UART Rx data trigger configuration for the RXDATA trigger condition.

        Args:
            size (int, optional): Number of data bytes (1 to 10) to set. 
            value (str, optional): The triggering data value:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 8).
                - **Example**: 
                    - For size 1 (8 bits): "1x1x0101".
                    - For size 3 (24 bits): "1x1x0101010010110010xxxx".
        """
        if size is not None:
            if size < 1 or size > 10:
                raise ValueError('Size must be between 1 and 10.')
            self.write(f':TRIGger:BUS:B1:UART:RX:DATa:SIZe {size}')

        if value is not None:
            self.write(f':TRIGger:BUS:B1:UART:RX:DATa:VALue "{value}"')

    def set_uart_tx_data_trigger(self, size: int = None, value: str = None) -> None:
        """Sets the UART Tx data trigger configuration for the TXDATA trigger condition.

        Args:
            size (int, optional): Number of data bytes (1 to 10) to set.
            value (str, optional): The triggering data value:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 8).
                - **Example**:
                    - For size 1 (8 bits): "1x1x0101".
                    - For size 3 (24 bits): "1x1x0101010010110010xxxx".
        """
        if size is not None:
            if not 1 <= size <= 10:
                raise ValueError('Size must be between 1 and 10.')
            self.write(f':TRIGger:BUS:B1:UART:TX:DATa:SIZe {size}')
        
        if value is not None:
            self.write(f':TRIGger:BUS:B1:UART:TX:DATa:VALue "{value}"')

    def spi_trigger_on(self) -> str:
        """Queries the SPI bus trigger condition.

        Returns:
            str: The SPI bus trigger condition.
        """
        return self.query(':TRIGger:BUS:B1:SPI:CONDition?') 

    def set_spi_trigger_on(self, condition: str) -> None:
        """Sets the SPI bus trigger condition.

        Args:
            condition (str): The SPI bus trigger condition to set. One of the following:
                - 'SS': Trigger on the Slave Select condition.
                - 'MISO': Trigger on the Master-In Slave-Out condition.
                - 'MOSI': Trigger on the Master-Out Slave-In condition.
                - 'MISOMOSI': Trigger on both Master-In Slave-Out and Master-Out Slave-In conditions.
        """
        self.write(f':TRIGger:BUS:B1:SPI:CONDition {condition}')

    def set_spi_data_trigger(self, size: int = None, val_miso: str = None, val_mosi: str = None) -> None:
        """Sets the SPI data trigger configuration for the MISO, MOSI, or MISOMOSI trigger condition.

        Args:
            size (int): Number of words (1 to 32) to set.
            val_miso (str): The triggering data value for MISO or MISOMOSI:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 4).
                - **Example**:
                    - For size 2 (8 bits): "1x1x0101".
                    - For size 3 (12 bits): "1x1x01010100".
            val_mosi (str): The triggering data value for MOSI or MISOMOSI, with the same formatting rules as val_miso.
        """
        if size is not None:
            if not 1 <= size <= 32:
                raise ValueError('Size must be between 1 and 32.')
            self.write(f':TRIGger:BUS:B1:SPI:DATa:SIZe {size}')

        if val_miso is not None:
            self.write(f':TRIGger:BUS:B1:SPI:DATa:MISO:VALue "{val_miso}"')

        if val_mosi is not None:
            self.write(f':TRIGger:BUS:B1:SPI:DATa:MOSI:VALue "{val_mosi}"')

    def can_trigger_on(self) -> str:
        """Queries the CAN bus trigger condition.

        Returns:
            str: The CAN bus trigger condition.
        """
        return self.query(':TRIGger:BUS:B1:CAN:CONDition?') 
    
    def set_can_trigger_on(self, condition: str) -> None:
        """Sets the CAN bus trigger condition.

        Args:
            condition (str): The CAN trigger condition to set. One of the following:
                - 'SOF'        : Triggers on a start of frame.
                - 'FRAMEtype'  : Triggers on the type of frame.
                - 'Identifier' : Triggers on a matching identifier.
                - 'DATA'       : Triggers on matching data.
                - 'IDANDDATA'  : Triggers on matching identifier and data field.
                - 'EOF'        : Triggers on the end of frame.
                - 'ACKMISS'    : Triggers on a missing acknowledge.
                - 'STUFFERR'   : Triggers on a bit stuffing error.
        """
        self.write(f':TRIGger:BUS:B1:CAN:CONDition {condition}')

    def set_can_frametype_trigger(self, frame_type: str) -> None:
        """Sets the frame type for a CAN FRAMEType trigger.

        Args:
            frame_type (str): The frame type to set. One of the following:
                - 'DATA'    : Data frame.
                - 'REMote'  : Remote frame.
                - 'ERRor'   : Error frame.
                - 'OVERLoad' : Overload frame.
        """
        self.write(f':TRIGger:BUS:B1:CAN:FRAMEtype {frame_type}')

    def set_can_identifier_trigger(self, mode: str = None, value: str = None, direction: str = None) -> None:
        """Sets the CAN identifier trigger configuration for the IDentifier or IDANDDATA trigger condition.
        
        Args:
            mode (str, optional): CAN identifier mode, either 'STANDard' or 'EXTended'.
            value (str, optional): Identifier string used for the CAN trigger:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the mode setting (11 for 'STANDard' or 29 for 'EXTended').
                - **Example**:
                    - For 'STANDard' mode : "01100X1X01X".
                    - For 'EXTended' mode : "01100X1X01X0X1X1X000X01X1X01X".
            direction (str, optional): Data direction, one of 'READ', 'WRITE', or 'NOCARE'.
        """
        if mode is not None:
            self.write(f':TRIGger:BUS:B1:CAN:IDentifier:MODe {mode}')

        if value is not None:
            self.write(f':TRIGger:BUS:B1:CAN:IDentifier:VALue "{value}"')

        if direction is not None:
            if direction.upper() not in ['READ', 'WRITE', 'NOCARE']:
                raise ValueError("Invalid value for direction. Must be one of: 'READ', 'WRITE', or 'NOCARE'.")
            self.write(f':TRIGger:BUS:B1:CAN:IDentifier:DIRection {direction}')

    def set_can_data_trigger(self, qualifier: str = None, size: int = None, value: str = None) -> None:
        """Sets the CAN data trigger configuration for the DATA or IDANDDATA trigger condition.
        
        Args:
            qualifier (str, optional): Data qualifier for triggering. One of the following:
                - 'LESSthan': Triggers when data is less than the qualifier value.
                - 'MOREthan': Triggers when data is greater than the qualifier value.
                - 'EQual': Triggers when data is equal to the qualifier value.
                - 'UNEQual': Triggers when data is not equal to the qualifier value.
                - 'LESSEQual': Triggers when data is less than or equal to the qualifier value.
                - 'MOREEQual': Triggers when data is more than or equal to the qualifier value.
            size (int, optional): Length of the data string in bytes (1 to 8).
            value (str, optional): Binary data string used for the CAN trigger:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 8).
                - **Example**:
                    - For size 1 (8 bits): "01010X1X".
        """
        if qualifier is not None:
            self.write(f':TRIGger:BUS:B1:CAN:DATa:QUALifier {qualifier}')

        if size is not None:
            if not (1 <= size <= 8):
                raise ValueError("Invalid size. Must be between 1 and 8 bytes.")
            self.write(f':TRIGger:BUS:B1:CAN:DATa:SIZe {size}')
            
        if value is not None:
            self.write(f':TRIGger:BUS:B1:CAN:DATa:VALue "{value}"')

    def lin_trigger_on(self) -> str:
        """Queries the LIN bus trigger condition.

        Returns:
            str: The LIN bus trigger condition.
        """
        return self.query(':TRIGger:BUS:B1:LIN:CONDition?') 
    
    def set_lin_trigger_on(self, condition: str) -> None:
        """Sets the LIN bus trigger condition.

        Args:
            condition (str): The LIN trigger condition to set. One of the following:
                - 'SYNCField': Sync field trigger.
                - 'IDentifier': Identifier field trigger.
                - 'DATA': Data field trigger.
                - 'IDANDDATA': Identifier and data field trigger.
                - 'WAKEup': Wake up trigger.
                - 'SLEEP': Sleep trigger.
                - 'ERRor': Error trigger.
        """
        self.write(f':TRIGger:BUS:B1:LIN:CONDition {condition}')

    def set_lin_data_trigger(self, qualifier: str = None, size: int = None, value: str = None) -> None:
        """Sets the LIN data trigger configuration for the DATA or IDANDDATA trigger condition.
        
        Args:
            qualifier (str, optional): Data qualifier for triggering. One of the following:
                - 'LESSthan': Triggers when data is less than the qualifier value.
                - 'MOREthan': Triggers when data is greater than the qualifier value.
                - 'EQual': Triggers when data equals the qualifier value.
                - 'UNEQual': Triggers when data is not equal to the qualifier value.
                - 'LESSEQual': Triggers when data is less than or equal to the qualifier value.
                - 'MOREEQual': Triggers when data is greater than or equal to the qualifier value.
            size (int, optional): Length of the data string in bytes (1 to 8).
            value (str, optional): Binary data string used for the LIN trigger:
                - Use '1' for binary 1.
                - Use '0' for binary 0.
                - Use 'x' as a "don't care" placeholder.
                - Number of characters depends on the data size setting (size * 8).
                - **Example**:
                    - For size 1 (8 bits): "01010X1X".
        """
        if qualifier is not None:
            self.write(f':TRIGger:BUS:B1:LIN:DATa:QUALifier {qualifier}')

        if size is not None:
            if not (1 <= size <= 8):
                raise ValueError("Invalid size. Must be between 1 and 8 bytes.")
            self.write(f':TRIGger:BUS:B1:LIN:DATa:SIZe {size}')
            
        if value is not None:
            self.write(f':TRIGger:BUS:B1:LIN:DATa:VALue "{value}"')

    def set_lin_error_trigger(self, error_type: str) -> None:
        """Sets the LIN error trigger configuration for the ERRor trigger condition.

        Args:
            error_type (str): The LIN error type to set. One of the following:
                - 'SYNC': Sets the LIN error type to SYNC.
                - 'PARIty': Sets the LIN error type to parity.
                - 'CHecksum': Sets the LIN error type to checksum.
        """
        self.write(f":TRIGger:BUS:B1:LIN:ERRTYPE {error_type}")

    def set_lin_identifier_trigger(self, value: str) -> None:
        """Sets the LIN identifier trigger configuration for the IDentifier or IDANDDATA trigger condition.

        Args:
            value (str): The LIN identifier string:
                - '1' for binary 1,
                - '0' for binary 0,
                - 'x' as a "don't care" placeholder.
                - The string is 6 characters long.
                - **Example**: "110101" or "x1x0x1".
        """
        self.write(f':TRIGger:BUS:B1:LIN:IDentifier:VALue "{value}"')
