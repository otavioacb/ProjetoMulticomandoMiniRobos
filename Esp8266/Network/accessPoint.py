import network


class AccessPoint():
    """
        This class will create a WLAN Access
        Point to other devices.
    """
    def __init__(self, ssid, pwd):
        self.ssid = ssid
        self.pwd = pwd
        self.net = network.WLAN(network.AP_IF)
    
    
    def connect(self):
        """
            Activate the interface to allow
            the access.
        """
        self.net.active(True)
        self.net.config(essid=self.ssid, password=self.pwd, channel=3)

        while not self.net.active():
            pass

        self.net.ifconfig(("192.168.4.5", "255.255.255.0", "192.168.4.1", "208.67.222.222"))
        
        
    def disconnect(self):
        """
            Close the WLAN access point.
        """
        
        self.net.active(False)
        
    
    def __str__(self):
        """
            Return the information about
            IP, Mask and other connections' settings.
        """
        
        return self.net.ifconfig()