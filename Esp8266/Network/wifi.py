import network
from led import Led
from time import sleep

class Wifi():
    """
        This class simplify the Wi-fi
        connection and deliver more configurations
        to the ESP's user.
    """
    
    def __init__(self):
        """
            Just create a Wifi and network instance
            and the configurations will set up
            next by the user.
        """
        self.net = network.WLAN(network.STA_IF)
        self.led = Led()
        self.byte = '00000000'
        self.net.active(True)
        
            
    def connect(self, ssid, pwd):
        """
            Try to connect with Wifi's information
            was passed as parameters.
        """
        self.net.connect(ssid, pwd)
            
        self.status()
        
        
    def status(self):
        """
            Represent the current status of
            the wirelles connection.
        """
        
        while self.net.isconnected() == False:                       
            self.led_load()    
        
        self.led.shift('00000000')
        
        print("\nConnection successful!")
        print(self.net.ifconfig())
        
        
    def led_load(self):
        """
            Change some Led's state to sinalize
            ESP is trying to connecting to Wifi.
        """
        byte_list = list(self.byte)
        if byte_list[0] == '1':
            byte_list[0] = '0'
        
        i = self.byte.find('1') - 1 if '1' in byte_list else 7  
        
        byte_list[i] = '1'
        if i != 7:
            byte_list[i+1] = '0'
        
        self.byte = "".join(byte_list)
        self.led.shift(self.byte)
        sleep(1)
