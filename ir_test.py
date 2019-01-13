from utime import sleep_us
from machine import Pin

pin = Pin(4, Pin.OUT)

@micropython.viper
def pulse2(cycles):  # Probably a very hacky solution, should be improved later
    GPIO_BASE = ptr32(0x60000300)  # GPIO base register
    for i in range(int(cycles)):  # Generate 38kHz pulse burst
        GPIO_BASE[1] = 0x10  # Turn on pin 4
        for _ in range(67):
            pass
        GPIO_BASE[2] = 0x10  # Turn off pin 4
        for _ in range(139):
            pass

def pulse(time):
        pulse2(int(time/26))

for i in range(5):
    pulse(562)
    sleep_us(1687)
    pulse(562)
    sleep_us(562)
