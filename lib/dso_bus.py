# Name: dso_bus.py
#
# Description: Control the DSO's bus.
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

class Bus:
    """This module can control the bus function on the DSO.
    """

    def __init__(self, parent) -> None:
        self.write = parent.write
        self.query = parent.query

    def get_supported_buses(self) -> tuple:
        """Returns the supported BUS types.
        
        Returns:
            str: A comma-separated list of supported bus types.
        """
        return tuple(self.query(':BUS1?').strip().split(','))
    
    def is_on(self) -> bool:
        """Is the bus state on?

        Return:
            bool: True or False.
        """
        ret = self.query(':BUS1:STATE?')
        return True if ('ON' in ret) else False
    
    def set_on(self) -> None:
        """Turns the bus on.
        """
        self.write(':BUS1:STATE ON')
    
    def set_off(self) -> None:
        """Turns the bus off.
        """
        self.write(':BUS1:STATE OFF')

    def set_type(self, type: str) -> None:
        """Sets the type of bus.

        Args:
            type (str): The type of bus, one of 'UART', 'I2C', 'SPI', 'PARallel', 'CAN', or 'LIN'.
        """
        self.write(f':BUS1:TYPe {type}')
    
    def get_type(self) -> str:
        """Gets the current bus type.
        
        Returns:
            type (str): The current bus type, one of 'UART', 'I2C', 'SPI', 'PARallel', 'CAN', or 'LIN'.
        """
        return self.query(':BUS1:TYPe?')
    
    def set_source(self, source: str) -> None:
        """Sets the bus source.

        Args:
            source (str): 'ANAlog' for analog inputs or 'DIGital' for digital inputs.
        """
        self.write(f':BUS1:INPut {source}')
    
    def get_source(self) -> str:
        """Gets the current bus input source.
        
        Returns:
            source (str): The current but input source ('ANAlog' or 'DIGital').
        """
        return self.query(':BUS1:INPut?')
    
    def set_i2c_params(self, rw_include: str = None, sclk_ch: int = None, sda_ch: int = None) -> None:
        """Sets I2C related settings.
        
        Args:
            rw_include (str, optional): 'ON' to inlcude the R/W bit, 'OFF' to exclude it.
            sclk_ch (int, optional): The channel for SCLK (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            sda_ch (int, optional): The channel for SDA (1: CH1, 2: CH2, 3: CH3, 4: CH4).
        """
        if rw_include is not None:
            self.write(f':BUS1:I2C:ADDRess:RWINClude {rw_include}')
        
        if sclk_ch is not None:
            self.write(f':BUS1:I2C:SCLK:SOURce CH{sclk_ch}')
        
        if sda_ch is not None:
            self.write(f':BUS1:I2C:SDA:SOURce CH{sda_ch}')
    
    def set_uart_params(self, bitrate: int = None, databits: int = None, parity: int = None, 
                 packet: int = None, eof_packet: int = None, tx_ch: int = None, rx_ch: int = None) -> None:
        """Sets UART related settings.
        
        Args:
            bitrate (int, optional): UART bit rate in bps.
            databits (int, optional): Number of data bits in the UART frame (5, 6, 7, 8, 9).
            parity (int, optional): UART bus parity (0: None, 1: Odd, 2: Even).
            packet (int, optional): UART packet setting (0: Off, 1: On).
            eof_packet (int, optional): EOF character (0: NULL, 1: LF, 2: CR, 3: SP, 4: FF).
            tx_ch (int, optional): Tx channel (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            rx_ch (int, optional): Rx channel (1: CH1, 2: CH2, 3: CH3, 4: CH4).
        """
        if bitrate is not None:
            self.write(f':BUS1:UART:BITRate {bitrate}')
        
        if databits is not None:
            self.write(f':BUS1:UART:DATABits {databits}')
        
        if parity is not None:
            self.write(f':BUS1:UART:PARIty {parity}')

        if packet is not None:
            self.write(f':BUS1:UART:PACKEt {packet}')

        if eof_packet is not None:
            self.write(f':BUS1:UART:EOFPAcket {eof_packet}')
        
        if tx_ch is not None:
            self.write(f':BUS1:UART:TX:SOURce CH{tx_ch}')
        
        if rx_ch is not None:
            self.write(f':BUS1:UART:RX:SOURce CH{rx_ch}')

    def set_spi_params(self, sclk_pol: str = None, ss_pol: str = None, word_size: int = None, 
                bit_order: int = None, sclk_ch: int = None, ss_ch: int = None, 
                mosi_ch: str = None, miso_ch: str = None) -> None:
        """Set SPI related settings.
 
        Args:
            sclk_pol (str, optional): SCLK line polarity ('FALL' for falling edge, 'RISE' for rising edge).
            ss_pol (str, optional): SS line polarity ('LOW' for active low, 'HIGH' for active high).
            word_size (int, optional): Number of bits per word for SPI (4~32).
            bit_order (int, optional): Bit order for SPI (0: MSB first, 1: LSB first).
            sclk_ch (int, optional): SCLK channel source (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            ss_ch (int, optional): SS channel source (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            mosi_ch (str or int, optional): MOSI channel source ('OFF', 1: CH1, 2: CH2, 3: CH3, 4: CH4).
            miso_ch (str or int, optional): MISO channel source ('OFF', 1: CH1, 2: CH2, 3: CH3, 4: CH4).
        """
        if sclk_pol is not None:
            self.write(f':BUS1:SPI:SCLK:POLARity {sclk_pol}')

        if ss_pol is not None:
            self.write(f':BUS1:SPI:SS:POLARity {ss_pol}')

        if word_size is not None:
            self.write(f':BUS1:SPI:WORDSize {word_size}')

        if bit_order is not None:
            self.write(f':BUS1:SPI:BITORder {bit_order}')

        if sclk_ch is not None:
            self.write(f':BUS1:SPI:SCLK:SOURce CH{sclk_ch}')

        if ss_ch is not None:
            self.write(f':BUS1:SPI:SS:SOURce CH{ss_ch}')

        if mosi_ch is not None:
            if mosi_ch.upper() == 'OFF':
                self.write(':BUS1:SPI:MOSI:SOURce OFF')
            else:
                self.write(f':BUS1:SPI:MOSI:SOURce CH{mosi_ch}')
        
        if miso_ch is not None:
            if miso_ch.upper() == 'OFF':
                self.write(':BUS1:SPI:MISO:SOURce OFF')
            else:
                self.write(f':BUS1:SPI:MISO:SOURce CH{miso_ch}')

    def set_disp_format(self, format: str) -> None:
        """Sets the dispaly format for the bus.

        Args:
            format (str): Desired display for the bus. Options are 'BINary' or 'HEXadecimal'
        """
        self.write(f':BUS1:DISplay:FORMAt {format}')

    def set_can_params(self, source: int = None, signal_type: str = None, bitrate: str = None) -> None:
        """Sets CAN bus related settings.

        Args:
            source (int, optional): The CAN input source (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            signal_type (str, optional): The signal type of the CAN bus. Can be one of the following:
                - 'CANH': CAN-High
                - 'CANL': CAN-Low
                - 'TX': Transmit
                - 'RX': Receive
            bitrate (str or int, optional): The bit rate of the CAN bus. Can be one of the following:
                - 'RATE10K': 10 kbps
                - 'RATE20K': 20 kbps
                - 'RATE50K': 50 kbps
                - 'RATE125K': 125 kbps
                - 'RATE250K': 250 kbps
                - 'RATE500K': 500 kbps
                - 'RATE800K': 800 kbps
                - 'RATE1M': 1 Mbps
                - Any integer value representing the desired bit rate in bps.
        """
        if source is not None:
            self.write(f':BUS1:CAN:SOURce CH{source}')

        if signal_type is not None:
            self.write(f':BUS1:CAN:PROBe {signal_type}')

        if bitrate is not None:
            self.write(f':BUS1:CAN:BITRate {bitrate}')

    def get_can_sample_point(self) -> int:
        """Returns the sample point of the CAN bus as a percentage of the bit time.
        
        Returns:
            int: The sample point as a percentage.
        """
        return self.query(':BUS1:CAN:SAMPLEpoint?')
    
    def set_lin_params(self, bitrate: int = None, id_format: str = None, polarity: str = None, source: int = None, std_ver: str = None) -> None:
        """Sets LIN bus related settings.
        
        Args:
            bitrate (int, optional): The bit rate of the LIN bus in bps.
            id_format (str, optional): The LIN ID format. Can be one of the following:
                - 'NOPARrity': Don't include parity bits with ID.
                - 'PARIty': Include parity bits with ID.
            polarity (str, optional): The LIN polarity. Can be one of the following:
                - 'NORMal': Normal LIN polarity.
                - 'INVerted': Inverted LIN polarity.
            source (int, optional): The LIN data source channel (1: CH1, 2: CH2, 3: CH3, 4: CH4).
            std_ver (str, optional): The LIN standard version. Can be one of the following:
                - 'V1X': LIN standard version 1.x.
                - 'V2X': LIN standard version 2.x.
                - 'BOTH': Both standards.
        """
        if bitrate is not None:
            self.write(f':BUS1:LIN:BITRate {bitrate}')

        if id_format is not None:
            self.write(f':BUS1:LIN:IDFORmat {id_format}')

        if polarity is not None:
            self.write(f':BUS1:LIN:POLARity {polarity}')

        if source is not None:
            self.write(f':BUS1:LIN:SOURce CH{source}')

        if std_ver is not None:
            self.write(f':BUS1:LIN:STANDard {std_ver}')

    def get_lin_sample_point(self) -> int:
        """Returns the sample point of the LIN bus as a percentage.
        
        Returns:
            int: The sample point as a percentage.
        """
        return self.query(':BUS1:LIN:SAMPLEpoint?')  

if __name__ == '__main__':
    pass
