import esp
esp.osdebug(None)
import gc
gc.collect()
from wifi import Wifi

ssid = 'FARB'
password = 'f4a1r4b56'

wifi = Wifi()

wifi.connect(ssid, password)        