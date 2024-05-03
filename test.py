import Actuator.PCA9685 as PCA9685

SERVO_MIN = 0.8 #ms
SERVO_MAX = 2.2 #ms

def calcPositionMagnifier(freq):
    return (SERVO_MAX - SERVO_MIN) * freq * 4096 / 100000

def calcPositionOffset(freq):
    return SERVO_MIN * freq * 4096 / 1000

def main():
    # TODO init PCA9685, setup one servo, turn in sinus wave
    freq = 50 #Hz
    K = calcPositionMagnifier(freq)
    OFF = calcPositionOffset(freq)

    print("  0% -> " + str(round(OFF)))
    print(" 50% -> " + str(round(50*K + OFF)))
    print("100% -> " + str(round(100*K + OFF)))


if __name__ == "__main__":
    main()