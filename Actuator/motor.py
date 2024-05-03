# Designed for PowerHD 3001HB servomotor

import Actuator.PCA9685 as PCA9685
import smbus2, time

###
# constants:

SERVO_MIN = 0.8 #ms
SERVO_MAX = 2.2 #ms

###
# functions:

def initPCA9685(freq=200, bus=1):
    i2cbus:smbus2.SMBus = smbus2.SMBus(bus)
    mode1reg = i2cbus.read_byte_data(PCA9685.ADDR, PCA9685.MODE1)
    
    # enable sleep mode
    i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.MODE1, mode1reg | PCA9685.MODE1_SLEEP)
    time.sleep(1)

    # set auto-increment mode
    

    # disable sleep mode
    i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.MODE1, mode1reg | PCA9685.MODE1_SLEEP)
    time.sleep(1)


###
# classes:

class ServoMotor:
    """Class for servo motor control for PowerHD 3001HB"""
    def __init__(self, channel, bus=1, freq=-1) -> None:
        self.ch = channel
        self.i2cbus:smbus2.SMBus = smbus2.SMBus(bus)
