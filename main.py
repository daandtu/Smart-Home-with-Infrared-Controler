import socket
from ussl import wrap_socket
from network import WLAN, STA_IF
from machine import Pin, freq
from utime import sleep
import sys
from sender import Sender

freq(160000000)  # Set frequenzy to 160MHz for a more acurate ir decoding and encoding

try:    
    pS = Pin(2, Pin.OUT)
    pS.on()
    
    sta_if = WLAN(STA_IF)
    while not sta_if.isconnected():
        pass
    pS.off()
    
    s = socket.socket()  # Create socket
    #ad = socket.getaddrinfo('000.000.000.000', 4444)[0][-1]  # Change your IP and Port here
    s.connect(ad)
    ss = wrap_socket(s)  # Wrap as a ssl socket
    #ss.write("aPASSWORD".encode())  # Set your password here
    ss.write("tu".encode())
    pS.on()
    irSender = Sender()
    sens = Sensor(ss, irSender)
    while True:
        data = ss.read(1).decode()  # Read one byte
        pS.off()
        if data is "q":
            ss.write("q".encode())
            utime.sleep(0.4)
            break
        elif (ord(data) >= 97 and ord(data) <= 122) or ord(data) == 10:
            irSender.got_data(data)
        sleep(0.1)
        pS.on()
    ss.close()
    s.close()
except Exception as e:
    print("Fehler", e)
finally:
    ss.write("q".encode())
    sleep(0.4)
    ss.close()
    s.close()
    pS.on()