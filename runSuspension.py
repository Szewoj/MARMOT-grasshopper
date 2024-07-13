from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time
from Actuator.motors import ServoMotor, ServoMotorInv
import position
from Regulation.Splitter import Splitter
from Regulation.Algorithms import PID2D

class Suspension:
    """Suspension class for batch servo motor management."""

    def __init__(self) -> None:
        self._uArr = np.empty(4)
        self.uFL = ServoMotorInv(6)
        self.uFR = ServoMotor(5)
        self.uBL = ServoMotor(10)
        self.uBR = ServoMotorInv(11)

    def turnOff(self) -> None:
        self.uFL.turnOff()
        self.uFR.turnOff()
        self.uBL.turnOff()
        self.uBR.turnOff()

    def setOutputs(self, outputArray:np.ndarray) -> tuple[float]:
        if outputArray.size != 4:
            print("Servo output array should must contain 4 output values.")
            return
        self._uArr[:] = np.squeeze(np.asarray(outputArray))
        bcFL = self.uFL.setOutputAI(self._uArr[0])
        bcFR = self.uFR.setOutputAI(self._uArr[1])
        bcBL = self.uBL.setOutputAI(self._uArr[2])
        bcBR = self.uBR.setOutputAI(self._uArr[3])

        return (bcFL, bcFR, bcBL, bcBR)


def main():
    # ready subcomponents:
    loop = InterruptibleLoop.InterruptibleLoop()
    poseOR = position.OrientationReader()
    logger = Logger.TCPLogger(skip=2)
    sync = synchronizer.Synchro(10)
    
    # regulation components:
    u = np.empty((1,4))
    u.fill(50.)
    e = np.empty((1,2))
    uPID = np.empty((1,2))
    pid2d = PID2D(Dt=0.1, Kp_xy=(.0, .2))
    pidSplitter = Splitter()

    # start threads
    poseOR.run_async()
    logger.run_async()


    # ready 
    suspension = Suspension()
    suspension.turnOff()

    
    sync.start()
    while loop.loop_again:
        out = poseOR.getRPY()
        z = poseOR.getAccZ()

        angXY = [100*out[0], 100*out[1]] #[roll, pitch]

        e[0][0] = -angXY[0]
        e[0][1] = -angXY[1]


        uPID[:] = pid2d.update(e)
        u[:] = u + pidSplitter.splitEven(uPID)

        suspension.setOutputs(u)

        msg = [time.time()] + angXY + [z, 0., 0.] + u.tolist()
        logger.log(msg)

        sync.waitNext()

    suspension.turnOff()
    poseOR.close()
    logger.close()


if __name__ == "__main__":
    main()