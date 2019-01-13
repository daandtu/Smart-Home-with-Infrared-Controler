from utime import sleep_us
from machine import Pin

class IR_OUT:

    SHORT = 562
    LONG = 1686  # A long pulse burst is 1686us long, thats 3 times a short pulse burst

    def __init__(self):
        self.pin = Pin(4, Pin.OUT)

    @micropython.viper
    def pulse2(self, cycles):  # Probably a very hacky solution, should be improved later
        GPIO_BASE = ptr32(0x60000300)  # GPIO base register
        for i in range(int(cycles)):  # Generate 38kHz pulse burst
            GPIO_BASE[1] = 0x10  # Turn on pin 4
            for _ in range(67):
                pass
            GPIO_BASE[2] = 0x10  # Turn off pin 4
            for _ in range(139):
                pass

    def pulse(self, time):
        self.pulse2(int(time/26))  # We need circa (time/26ms) cycles, because every 38kHz signal pulse is 26ms long

    def send(self, data):
        print(data)
        data = ''.join(data.split())  # Remove all whitespaces
        self.pulse(9000) # 9ms leading pulse burst
        sleep_us(4500)  # 4.5ms space
        for bit in data:
            self.pulse(IR_OUT.SHORT)  # Every bit starts with an 562us puse burst
            sleep_us(IR_OUT.SHORT) if bit is '0' else sleep_us(IR_OUT.LONG)  # space depending on '0' or '1'
        self.pulse(IR_OUT.SHORT) # Finish message with a final pulse burst
        sleep_us(100000) # Sleep some time after message
		
    def repeat(self):  # Send repeat code
        self.pulse(9000)  # 9ms leading pulse burst
        sleep_us(2250)  # 2.25ms space
        self.pulse(IR_OUT.SHORT)  # 562us pulse burst to mark the end of the space
        sleep_us(100000) # Sleep some time after message