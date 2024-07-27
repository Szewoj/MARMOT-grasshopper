from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time
import Actuator.motors
import position

from Regulation import Splitter

F_SUSPENSION = 25. # Hz

class Suspension:
    """Suspension class for batch servo motor management."""

    def __init__(self) -> None:
        self._uArr = np.empty(4)
        self._uClamp = np.empty((4,1))

        Actuator.motors.initPCA9685()

        self.uFL = Actuator.motors.ServoMotorInv(6, -5)
        self.uFR = Actuator.motors.ServoMotor(5, -15)
        self.uBL = Actuator.motors.ServoMotor(10)
        self.uBR = Actuator.motors.ServoMotorInv(11)

    def turnOff(self) -> None:
        self.uFL.turnOff()
        self.uFR.turnOff()
        self.uBL.turnOff()
        self.uBR.turnOff()

    def setOutputs(self, outputArray:np.ndarray) -> np.ndarray:
        if outputArray.size != 4:
            print("Servo output array should must contain 4 output values.")
            return
        self._uArr[:] = np.squeeze(np.asarray(outputArray))

        self._uClamp[0][0] = self.uFL.setOutputAI(self._uArr[0])
        self._uClamp[1][0] = self.uFR.setOutputAI(self._uArr[1])
        self._uClamp[2][0] = self.uBL.setOutputAI(self._uArr[2])
        self._uClamp[3][0] = self.uBR.setOutputAI(self._uArr[3])

        return self._uClamp


def main():
    # ready subcomponents:
    loop = InterruptibleLoop.InterruptibleLoop()
    poseOR = position.OrientationReader()
    logger = Logger.TCPLogger(skip=0)
    sync = synchronizer.Synchro(F_SUSPENSION)
    pidSplitter = Splitter.Splitter()
    
    # regulation components:
    u = np.empty((4,1))
    u.fill(50.)
    uPID = np.zeros((2,1))
    
    out = np.empty(3)
    logAngle = np.empty(2,dtype=float)

    i = 0

    # start threads
    poseOR.run_async()
    logger.run_async()


    # ready 
    suspension = Suspension()
    suspension.turnOff()

    print("Step response starting in 10 seconds...")
    time.sleep(10.0)
    
    sync.start()
    print("Started!")
    while loop.loop_again:
        out[:] = poseOR.getRPY()
        z = poseOR.getVelZ()

        angXY = [1000*out[0], 1000*out[1]] #[roll, pitch]


        # preplanned steering trajectory
        if i == 50:
            print("Step response, dUy = 0")

            u[0][0] = 50
            u[1][0] = 50
            u[2][0] = 50
            u[3][0] = 50

        if i == 100:
            print("Step response, dUy = -2")
            uPID[0][0] = 0
            uPID[1][0] = -2

        if i == 110:
            print("Step response, dUy = 8")
            uPID[0][0] = 0
            uPID[1][0] = 8
        
        if i == 120:
            print("Step response, dUy = 0")
            uPID[0][0] = 0
            uPID[1][0] = 0

        if i == 150:
            print("Step response, dUy = 0")
            uPID[0][0] = 0
            uPID[1][0] = 0

            u[0][0] = 50
            u[1][0] = 50
            u[2][0] = 50
            u[3][0] = 50

        if i == 200:
            print("Step response, dUx = -2")
            uPID[0][0] = -2
            uPID[1][0] = 0

        if i == 210:
            print("Step response, dUx = 8")
            uPID[0][0] = 8
            uPID[1][0] = 0

        if i == 220:
            print("Step response, dUx = 8")
            uPID[0][0] = 8
            uPID[1][0] = 0

        if i == 250:
            print("Step response, dUx = 0")
            uPID[0][0] = 0
            uPID[1][0] = 0

            u[0][0] = 50
            u[1][0] = 50
            u[2][0] = 50
            u[3][0] = 50

        if i == 260:
            loop.breakLoop()

        # split outputs
        u[:] = u + np.round(pidSplitter.splitEven(uPID),1)

        suspension.setOutputs(u)

        # log data to remote
        logAngle[:] = np.array(angXY, dtype=float)
        msg = [time.time()] \
                + logAngle.squeeze().tolist() \
                + [z] \
                + uPID.astype(float).squeeze().tolist() \
                + u.astype(float).squeeze().tolist()
        logger.log(msg)

        sync.waitNext()

        i += 1




    suspension.turnOff()
    poseOR.close()
    logger.close()


if __name__ == "__main__":
    main()