from machine import Pin
from ir_nec_encode import IR_OUT

class Sender():

    codes = {
    'ro' : "00011110 11100001 11110000 00001111",  # Radio on/off	
    'rp' : "00011110 11100001 11111011 00000100",  # Radio Modus Portable
    'rr' : "00011110 11100001 11010010 00101101",  # Radio Modus Radio
    'ru' : "00011110 11100001 01111000 10000111",  # Radio volume up
    'rd' : "00011110 11100001 11111000 00000111",  # Radio volume down
    'rl' : "00011110 11100001 00111000 11000111",  # Radio preset left
    'rh' : "00011110 11100001 11011000 00100111",  # Radio Preset right
     }

    def __init__(self):
        self.IR = IR_OUT()
        self.message = ""

    def got_data(self, data):
        if data is "s":  # Start of message
            self.message = ""
        elif data is "\n":  # End of message
            print("Data:", self.message)
            self.got_message(self.message)
        else:
            self.message += data

    def got_message(self, message):
         if message in Sender.codes:
            self.IR.send(Sender.codes[self.message])
        elif len(message) >= 3 and message[-1] is "l" and message[:-1] in Sender.codes:  # Send message with repeat codes
            print("Repeat")
            for _ in range(5):
                self.IR.send(Sender.codes[self.message[:-1]])
        elif len(message) > 6:
            self.message = ""  # Reset