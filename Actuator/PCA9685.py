# PCA9685 addresses:
ADDR    = 0x40
BUS     = 6

# PCA9685 registers:

MODE1   = 0x00
MODE2   = 0x01

PWM_INV_REG = -1

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

SERVO_ON_OFF = 0b00010000
SERVO_H_MASK = 0b00001111
SERVO_L_MASK = 0b11111111


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

    if ch == 0:
        return PWM_00_REG
    elif ch == 1:
        return PWM_01_REG
    elif ch == 2:
        return PWM_02_REG
    elif ch == 3:
        return PWM_03_REG
    elif ch == 4:
        return PWM_04_REG
    elif ch == 5:
        return PWM_05_REG
    elif ch == 6:
        return PWM_06_REG
    elif ch == 7:
        return PWM_07_REG
    elif ch == 8:
        return PWM_08_REG
    elif ch == 9:
        return PWM_09_REG
    elif ch == 10:
        return PWM_10_REG
    elif ch == 11:
        return PWM_11_REG
    elif ch == 12:
        return PWM_12_REG
    elif ch == 13:
        return PWM_13_REG
    elif ch == 14:
        return PWM_14_REG
    elif ch == 15:
        return PWM_15_REG
    else:
        print("error: unknown PWM channel")
        return -1
        