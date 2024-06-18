import Actuator.PCA9685 as PCA9685
import Actuator.motors as motors

SERVO_MIN = 0.8 #ms
SERVO_MAX = 2.2 #ms

def calcPositionMagnifier(freq):
    return (SERVO_MAX - SERVO_MIN) * freq * 4096 / 100000

def calcPositionOffset(freq):
    return SERVO_MIN * freq * 4096 / 1000

def main():
    # TODO init PCA9685, setup one servo, turn in sinus wave
    motors.initPCA9685(freq=50)

    motor1 = motors.ServoMotor(10)


if __name__ == "__main__":
    main()