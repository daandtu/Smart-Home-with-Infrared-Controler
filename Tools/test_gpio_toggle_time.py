from utime import ticks_us, ticks_diff, sleep_us
from machine import Pin

p = Pin(4, Pin.OUT, value=0)

# Toggle 3
@micropython.viper
def toggle3(n):
    GPIO_BASE = ptr32(0x60000300)
    for i in range(int(n)):
        GPIO_BASE[1] = 0x10  # Turn on pin 4
        for _ in range(33):
            pass
        GPIO_BASE[2] = 0x10  # Turn off pin 4
        for _ in range(73):
            pass

# Toggle 2
@micropython.asm_xtensa
def toggle2():
    movi(a2, 0x60000300) # GPIO Base address
    movi(a5, 0x10) # set/clear bit 4
    movi(a4, 1) # loop decrement
    movi(a3, 346)
    label(LOOP)
    s8i(a5, a2, 4)
    s8i(a5, a2, 8)
    sub(a3, a3, a4)
    bnez(a4, LOOP)


# Toggle 1
def toggle1(num):
    for i in range(num):
        p.on()
        p.off()
    

# Evaluation
counter = const(346)
t1 = ticks_us()
toggle3(counter)
t2 = ticks_us()
print("Average delay:",ticks_diff(t2, t1)/counter)