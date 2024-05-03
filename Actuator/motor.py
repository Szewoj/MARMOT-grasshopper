# Designed for PowerHD 3001HB servomotor

import Actuator.PCA9685 as PCA9685
import smbus2, time

###
# constants:

SERVO_MIN = 0.8 #ms
SERVO_MAX = 2.2 #ms

###
# functions:

def initPCA9685(freq=50, bus=1):
    i2cbus:smbus2.SMBus = smbus2.SMBus(bus)
    mode1reg = i2cbus.read_byte_data(PCA9685.ADDR, PCA9685.MODE1)
    
    # enable sleep mode
    i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.MODE1, mode1reg | PCA9685.MODE1_SLEEP)
    time.sleep(1)

    # set prescalar
    prescale = PCA9685.calcPreScalar(freq)
    if prescale < 0:
        print("Prescalar was NOT modified!")
    else:
        i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.PRE_SCALAR, prescale)

    # set auto-increment mode
    mode1reg = mode1reg | PCA9685.MODE1_AI

    # disable sleep mode
    i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.MODE1, mode1reg | PCA9685.MODE1_SLEEP)
    time.sleep(1)

    i2cbus.close()


def calcPositionMagnifier(freq):
    pass # TODO

def calcPositionOffset(freq):
    pass # TODO

###
# classes:

class ServoMotor:
    """Class for servo motor control for PowerHD 3001HB"""
    def __init__(self, channel, bus=1, freq=-1) -> None:
        self.ch = channel
        self.i2cbus:smbus2.SMBus = smbus2.SMBus(bus)
        # TODO setup servo, turn off channel, calculate limits




###
# servo test:

def main():
    # TODO init PCA9685, setup one servo, turn in sinus wave
    pass


if __name__ == "__main__":
    main()