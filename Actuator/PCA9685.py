# PCA9685 addresses:
ADDR    = 0x40

# PCA9685 registers:

MODE1   = 0x00
MODE2   = 0x01


PWM_00_REG  = 0x06
PWM_01_REG  = 0x0A
PWM_02_REG  = 0x0E
PWM_03_REG  = 0x12

PWM_04_REG  = 0x16
PWM_05_REG  = 0x1A
PWM_06_REG  = 0x1E
PWM_07_REG  = 0x22

PWM_08_REG  = 0x26
PWM_09_REG  = 0x2A
PWM_10_REG  = 0x2E
PWM_11_REG  = 0x32

PWM_12_REG  = 0x36
PWM_13_REG  = 0x3A
PWM_14_REG  = 0x3E
PWM_15_REG  = 0x42


PRE_SCALAR  = 0xFE


# PCA9685 register values:

OSC_CLOCK   = 25000000

MODE1_SLEEP = 0b00010000
MODE1_AI    = 0b00100000


# helper functions:

def calcPreScalar(freq:int) -> int:
    """Calculate PCA9685 clock prescalar based on desired output PWM frequency."""

    if freq > 1000:
        print("error: frequency is too high for PCA9685")
        return -1
    if freq < 40:
        print("error: frequency is too low for PCA9685")
        return -1

    return round(OSC_CLOCK / 4096 / freq) - 1



def calcFreq(prescal:int) -> int:
    """Calculate PWM frequency based on prescalar."""

    return round(OSC_CLOCK / 4096 / (prescal + 1)) 



def getChannelAddr(ch:int):
    """Get main address of PWM channel
    
    Register Addresses:
    * PWM_XX_ON_L  [+0]
    * PWM_XX_ON_H  [+1]
    * PWM_XX_OFF_L [+2]
    * PWM_XX_OFF_H [+3]"""

    match(ch):
        case 0:
            return PWM_00_REG
        case 1:
            return PWM_01_REG
        case 2:
            return PWM_02_REG
        case 3:
            return PWM_03_REG
        case 4:
            return PWM_04_REG
        case 5:
            return PWM_05_REG
        case 6:
            return PWM_06_REG
        case 7:
            return PWM_07_REG
        case 8:
            return PWM_08_REG
        case 9:
            return PWM_09_REG
        case 10:
            return PWM_10_REG
        case 11:
            return PWM_11_REG
        case 12:
            return PWM_12_REG
        case 13:
            return PWM_13_REG
        case 14:
            return PWM_14_REG
        case 15:
            return PWM_15_REG
        case _:
            print("error: unknown PWM channel")
            return -1
        