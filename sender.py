from machine import Pin
from ir_nec_encode import IR_OUT

class Sender():

    codes = {
    'ro' : "00011110 11100001 11110000 00001111",  # Radio on/off
    'rp' : "00011110 11100001 11111011 00000100",  # Radio Modus Portable #gitignore
    'rr' : "00011110 11100001 11010010 00101101",  # Radio Modus Radio #gitignore
    'ru' : "00011110 11100001 01111000 10000111",  # Radio lauter #gitignore
    'rd' : "00011110 11100001 11111000 00000111",  # Radio leiser #gitignore
    'rl' : "00011110 11100001 00111000 11000111",  # Radio preset left #gitignore
    'rh' : "00011110 11100001 11011000 00100111",  # Radio Preset right #gitignore
     }

    def __init__(self):
        self.IR = IR_OUT()
        self.message = ""

    def got_data(self, data):
        if data is "s":  # Start of message
            self.message = ""
        elif data is "\n":  # End of message
            print("Data:", self.message)
            if self.message in Sender.codes:
                self.IR.send(Sender.codes[self.message])
            elif len(self.message) >= 3 and self.message[-1] is "l" and self.message[:-1] in Sender.codes:  # Send message with repeat codes
                print("Repeat")
                for _ in range(5):
                    self.IR.send(Sender.codes[self.message[:-1]])
            elif len(self.message) > 6:
                self.message = ""
        else:
            self.message += data