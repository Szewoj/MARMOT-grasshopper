# Designed for PowerHD 3001HB servomotor

import Actuator.PCA9685 as PCA9685
import time, smbus2

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


def PRIVATE_calcPositionMagnifier(freq):
    return (SERVO_MAX - SERVO_MIN) * freq * 4096 / 100000

def PRIVATE_calcPositionOffset(freq):
    return SERVO_MIN * freq * 4096 / 1000


###
# classes:

class ServoMotor:
    """Class for servo motor control for PowerHD 3001HB"""
    def __init__(self, channel, bus=1, freq=-1) -> None:
        self.i2cbus:smbus2.SMBus = smbus2.SMBus(bus)

        if freq < 40 or freq > 1000:
            # check real frequency
            freq = PCA9685.calcFreq(self.i2cbus.read_byte_data(PCA9685.ADDR, PCA9685.PRE_SCALAR))

        self.K = PRIVATE_calcPositionMagnifier(freq)
        self.OFF = PRIVATE_calcPositionOffset(freq)

        self.CHL = PCA9685.getChannelAddr(channel)

        if self.CHL == -1:
            print("Could not set channel. Servo init failed!")

        # TODO setup servo, turn off channel



###
# servo test:

def main():
    # TODO init PCA9685, setup one servo, turn in sinus wave
    freq = 50 #Hz
    K = PRIVATE_calcPositionMagnifier(freq)
    OFF = PRIVATE_calcPositionOffset(freq)



    print("Servo setup:")
    print("  0% -> " + str(round(OFF)) + "us")
    print(" 50% -> " + str(round(50*K + OFF)) + "us")
    print("100% -> " + str(round(100*K + OFF)) + "us")




if __name__ == "__main__":
    main()