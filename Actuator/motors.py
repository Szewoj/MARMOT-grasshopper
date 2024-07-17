# Designed for PowerHD 3001HB servomotor

import Actuator.PCA9685 as PCA9685
import time, smbus2


###
# functions:

def initPCA9685(freq=50, bus=PCA9685.BUS):
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
    i2cbus.write_byte_data(PCA9685.ADDR, PCA9685.MODE1, mode1reg & (~PCA9685.MODE1_SLEEP))
    time.sleep(1)

    i2cbus.close()

###
# Functions to rescale PCA9685 signals to 0%-100% scale

def PRIVATE_calcPositionMagnifier(freq, motor_min, motor_max):
    return (motor_max - motor_min) * freq * 4096 / 100000

def PRIVATE_calcPositionOffset(freq, motor_min):
    return motor_min * freq * 4096 / 1000


###
# classes:

class GenericMotor(object):
    """Class for generic servo using PCA9685 in I2C mode for PWM control"""
    SIGNAL_MIN = 1.0 #ms
    SIGNAL_MAX = 2.0 #ms

    def __init__(self, channel, bus=PCA9685.BUS, freq=-1) -> None:
        self.i2cbus:smbus2.SMBus = smbus2.SMBus(bus)
        """i2c bus communication object"""
        if freq < 40 or freq > 1000:
            # check real frequency
            freq = PCA9685.calcFreq(self.i2cbus.read_byte_data(PCA9685.ADDR, PCA9685.PRE_SCALAR))

        print(self.SIGNAL_MAX)

        self.K = PRIVATE_calcPositionMagnifier(freq, self.SIGNAL_MIN, self.SIGNAL_MAX)
        """Magnitude ratio to calculate PWM signal length from 0% to 100% input"""
        self.OFF = PRIVATE_calcPositionOffset(freq, self.SIGNAL_MIN)
        """Offset to calculate PWM signal length from 0% to 100% input"""

        self.CHL = PCA9685.getChannelAddr(channel)
        """PWM channel on PCA9685 control board"""

        self.lastPos = round(50.0 * self.K + self.OFF)
        """Last position in pwm signal scale"""

        self.turnedOn = False
        """PWM signal power status"""

        if self.CHL == PCA9685.PWM_INV_REG:
            print("Could not set channel. Servo init failed!")
        else:
            pt_l = self.lastPos & PCA9685.SERVO_L_MASK
            pt_h = (self.lastPos >> 8) & PCA9685.SERVO_H_MASK
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL, 0)
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+1, 0)
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+2, pt_l)
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+3, PCA9685.SERVO_ON_OFF | pt_h)


    def turnOff(self) -> None:
        if self.CHL != PCA9685.PWM_INV_REG and self.turnedOn:
            reg = self.i2cbus.read_byte_data(PCA9685.ADDR, self.CHL+3)
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+3, reg | PCA9685.SERVO_ON_OFF)
            self.turnedOn = False


    def turnOn(self) -> None:
        if self.CHL != PCA9685.PWM_INV_REG and not self.turnedOn:
            reg = self.i2cbus.read_byte_data(PCA9685.ADDR, self.CHL+3)
            self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+3, reg & (~PCA9685.SERVO_ON_OFF))
            self.turnedOn = True


    def setOutputAI(self, pos:float) -> float:
        """Set servo position from 0% to 100% (float) using I2C Auto Increment."""
        if self.CHL != PCA9685.PWM_INV_REG:
            cpos = min(100, max(0, pos))

            pwm_pt:int = round(cpos * self.K + self.OFF)

            if not self.turnedOn or abs(pwm_pt - self.lastPos) > 1:
                #print("Setting position " + str(cpos) + "%: " + str(pwm_pt))
                pwm_pt_l = pwm_pt & PCA9685.SERVO_L_MASK
                pwm_pt_h = (pwm_pt >> 8) & PCA9685.SERVO_H_MASK
                data = [0, 0, pwm_pt_l, pwm_pt_h]
                self.i2cbus.write_i2c_block_data(PCA9685.ADDR, self.CHL, data)
                self.turnedOn = True
                self.lastPos = pwm_pt
            
            # for back-calculation
            if cpos != pos:
                return pos - cpos
            else:
                return 0.


    def setOutput(self, pos:float) -> None:
        """Set servo position from 0% to 100% (float) 
            - does not require Auto Increment mode to function
            
            It is recomended to use setOutputAI() function, but it requires to set AI bit in PCA9685 MODE1 register."""
        if self.CHL != PCA9685.PWM_INV_REG:
            cpos = min(100, max(0, pos))

            pwm_pt:int = round(cpos * self.K + self.OFF)

            if not self.turnedOn or abs(pwm_pt - self.lastPos) > 1:
                #print("Setting position " + str(cpos) + "%: " + str(pwm_pt))
                pwm_pt_l = pwm_pt & PCA9685.SERVO_L_MASK
                pwm_pt_h = (pwm_pt >> 8) & PCA9685.SERVO_H_MASK
                self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL, 0)
                self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+1, 0)
                self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+2, pwm_pt_l)
                self.i2cbus.write_byte_data(PCA9685.ADDR, self.CHL+3, PCA9685.SERVO_ON_OFF | pwm_pt_h)
                self.turnedOn = True
                self.lastPos = pwm_pt

            # for back-calculation
            if cpos != pos:
                return pos - cpos
            else:
                return 0.

##

class ServoMotor(GenericMotor):
    """Class for servo motor control for PowerHD 3001HB of active suspension"""

    SIGNAL_MIN = 0.65 #ms
    SIGNAL_MAX = 2.40 #ms

    def __init__(self, channel, bus=PCA9685.BUS, freq=-1) -> None:
        super(ServoMotor, self).__init__(channel, bus, freq)


##

class ServoMotorInv(ServoMotor):
    """Class for inverted servo motor control for PowerHD 3001HB of active suspension"""

    def setOutput(self, pos: float) -> float:
        pt = 100. - pos
        return super().setOutput(pt)

    def setOutputAI(self, pos: float) -> float:
        pt = 100. - pos
        return super().setOutputAI(pt)
##

class BrushedMotor(GenericMotor):

    def __init__(self, channel, bus=PCA9685.BUS, freq=-1) -> None:
        super().__init__(channel, bus, freq)
        super().turnOn()

    def turnOff(self) -> None:
        """Reset position to medium point (motor turned off)"""
        super().setOutputAI(50)

    def turnOn(self) -> None:
        """Reset position to medium point (motor turned off)"""
        self.turnOff()


###
# servo test:

def main():
    # TODO init PCA9685, setup one servo, turn in sinus wave
    freq = 50 #Hz
    K = PRIVATE_calcPositionMagnifier(freq, GenericMotor.SIGNAL_MIN, GenericMotor.SIGNAL_MAX)
    OFF = PRIVATE_calcPositionOffset(freq, GenericMotor. SIGNAL_MIN)

    print("Servo setup:")
    print("  0% -> " + str(round(OFF)) + "us")
    print(" 50% -> " + str(round(50*K + OFF)) + "us")
    print("100% -> " + str(round(100*K + OFF)) + "us")


if __name__ == "__main__":
    main()