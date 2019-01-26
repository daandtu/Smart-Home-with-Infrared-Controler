from machine import Pin
from utime import ticks_diff,ticks_ms

class Sensor:
    def __init__(self, socket, irSender, sound_pin = 14):
        self.socket = socket
        self.irSender = irSender
        self.sound_pin = Pin(sound_pin, Pin.IN)
        self.sound_pin.irq(trigger=Pin.IRQ_RISING, handler=lambda p: self.callback(p))
        self.time = ticks_ms()
    def callback(self, p):
        if ticks_diff(ticks_ms(), self.time) > 500:
            self.irSender.got_message("ro")
        self.time = ticks_ms()