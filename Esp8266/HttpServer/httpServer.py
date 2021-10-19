try:
    import usocket as soc
except:
    import socket as soc
    
from wifiConnection import WifiConnection
    
class HttpServer():
    """
        This class will be in charge to
        handle the HTTP requests.
    """
    
    def __init__(self):
        self.soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)    
        self.soc.bind(("", 80))
        self.soc.listen(1)
        
        self.wifi = WifiConnection()
        self.wifi.connect("Mi", "esp12345")
        
    def listening(self):
        """
            Set up the HTTP Headers and
            send the HTML page.
        """
        conn, addr = self.soc.accept()
        print('Got a connection from %s' % str(addr))
        request = str(conn.recv(1024))
          
        self.controller(request)
  
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(self.web_page())
        conn.close()
        
    def web_page(self):
        """
            Read the HTML file to send
            the page to be loading.
        """
        try:
          with open("network.html", "r") as file:
              file = file.read()
              
              return file.replace("%s", "false")
        except Exception as error:
            if error.value == 2:
                return "<h1>This route doesn't have a template to send!</h1>"
    
    
    def controller(self, request):
        """
            Filter request's method to
            send the correct response.
        """
        req_parts = request.split()
        
        if "POST" in request:
            start = req_parts[-1].find("{")
            stop = req_parts[-1].find("}")
            
            wifi_info = req_parts[-1][start+1:stop].split(",")
            
            ssid = wifi_info[0].split(":")[-1]
            pwd = wifi_info[1].split(":")[-1]
            print(ssid, pwd)
            self.wifi.connect(ssid, pwd)
        elif "GET" in request:
            print("Waiting confirmation...")


