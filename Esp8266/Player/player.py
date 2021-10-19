from machine import Pin, UART
from time import sleep_ms, ticks_ms, ticks_diff


START = 0x7E
VERSION = 0xFF
LENGTH = 0x06
FEEDBACK = 0x00
END = 0xEF


class Player():
    """
        This class will create a UART conection
        with DFPlayer module to play songs.
    """
    
    def __init__(self, uart_id, volume=15, equalizer=0):
        """
            The initialization will be responsible
            to create the UART object and set volume
            and equalizer.
        """
        self.__uart = UART(uart_id)
        self.__uart.init(baudrate=9600,
                          bits=8,
                          parity=None,
                          stop=1)
        
        print("Waiting to the module finish the initialization...")
        sleep_ms(1500)
        print("DFPlayer is ready to be used!")
        
        self.volume(volume)
        self.eq(equalizer)
    
    def __checksum(self, cmd, p_msb, p_lsb):
        """
            This method will calculate the
            checksum and send the MSB and LSB
            bytes.
        """
        checksum = 0xFFFF-(VERSION+LENGTH+cmd+p_msb+p_lsb)+1
    
        return checksum >> 8, checksum & 0xFFFF
        
        
    def __command(self, cmd, p_msb, p_lsb):
        """
            This method is responsible to create
            the data structure to be sent via UART.
        """
        checksum_MSB, checksum_LSB = self.__checksum(cmd, p_msb, p_lsb)
        commandLine = bytes([b & 0xFF for b in [
            START, VERSION, LENGTH, cmd, FEEDBACK,
            p_msb, p_lsb, checksum_MSB, checksum_LSB, END
        ]])

        return commandLine
    
    
    def volume(self, volume):
        """
            Here will be set up the volume level.
        """
        volume_filtered = volume if (volume <= 30) and (volume >= 0) else 30
        command = self.__command(0x06, 0x00, volume_filtered)
        
        sleep_ms(200)
        self.__uart.write(command)
        
        
    def eq(self, equalizer):
        """
            Here will be set up the equalize mode.
        """
        command = self.__command(0x07, 0x00, equalizer)
        
        sleep_ms(200)
        self.__uart.write(command)
        
        
    def play_folder(self, folder, file):
        """
            This method will be play a file into
            a specifi folder.
        """
        command = self.__command(0x0F, folder, file)
        
        sleep_ms(200)    
        self.__uart.write(command)
        
        
    def play(self):
        """
            Play the current playback.
        """
        command = self.__command(0x0D, 0x00, 0x00)
        
        sleep_ms(200)
        self.__uart.write(command)
    
    
    def pause(self):
        """
            Pause the current playback.
        """
        command = self.__command(0x0E, 0x00, 0x00)
        
        sleep_ms(200)
        self.__uart.write(command)
        