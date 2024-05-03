# PCA9685 addresses:
ADDR = 0x40

# PCA9685 registers:

MODE1 = 0x00
MODE2 = 0x01



PRE_SCALAR = 0xFE


# PCA9685 register values:

OSC_CLOCK = 25000000

MODE1_SLEEP = 0b00010000

MODE1_AI = 0b00100000


# helper functions:

def calcPreScalar(freq:int) -> int:
    if freq > 1000:
        print("error: frequency is too high for PCA9685")
        return -1
    if freq < 40:
        print("error: frequency is too low for PCA9685")
        return -1

    return round(OSC_CLOCK / 4096 / freq) - 1

def calcFreq(prescal:int) -> int:
    return round(OSC_CLOCK / 4096 / (prescal + 1)) 
