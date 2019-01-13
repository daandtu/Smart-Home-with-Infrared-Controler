from utime import ticks_diff,ticks_us
from machine import Pin

class IR:

    EDGES_NORMAL = 68  # 68 edges for a normal message
    EDGES_REPEAT = 4  # Four edges for a repeat code
    REPEAT = -1
    ERROR = -2

    def __init__(self, cb, pin = 13):
        self.data = []
        self.cb = cb
        self.last_time_update = 0
        self.count = 0
        self.loop = True
        self.edges = IR.EDGES_NORMAL
        self.pin = Pin(pin, Pin.IN)
    def _decode(self):
        if len(self.data) == IR.EDGES_REPEAT:  # Repeat code
            self.cb(IR.REPEAT)
        else:
            pulses = [ticks_diff(self.data[i + 1], self.data[i]) for i in range(self.edges - 1)]
            result = ""
            for i in range(3, len(pulses), 2):
                if pulses[i] < 1000:  # 562.5us for '0' and 1687.5us for a '1'
                    result += "0"
                else:
                    result += "1"
                if len(result.replace(" ","")) % 8 == 0: result += " "
            self.cb(result)
        self.edges = IR.EDGES_NORMAL
        self.count = 0
        self.data = []
    def callback(self, p):
        self.data.append(ticks_us())
        if self.edges == IR.EDGES_NORMAL and len(self.data) >= 3 and ticks_diff(self.data[2],self.data[1]) < 3000:
            self.edges = IR.EDGES_REPEAT
    def start(self):
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda p: self.callback(p))  # wait for first edge
        while self.loop:  # Loop forever
            if len(self.data) >= self.edges:
                self._decode()
    def interupt(self):
        self.loop = False

        
def cb(result):
    print(result)
a = IR(cb)
a.start()