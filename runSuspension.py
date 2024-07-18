from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time
from Actuator import motors
import position
from Regulation import Splitter, Algorithms, Parameters

F_SUSPENSION = 10. # Hz

REGULATOR = Parameters.PID_P

class Suspension:
    """Suspension class for batch servo motor management."""

    def __init__(self) -> None:
        self._uArr = np.empty(4)
        self._uClamp = np.empty((4,1))
        self.uFL = motors.ServoMotorInv(6)
        self.uFR = motors.ServoMotor(5)
        self.uBL = motors.ServoMotor(10)
        self.uBR = motors.ServoMotorInv(11)

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
    logger = Logger.TCPLogger(skip=2)
    sync = synchronizer.Synchro(F_SUSPENSION)
    
    # regulation components:
    u = np.empty((4,1))
    u.fill(50.)
    e = np.empty((2,1))
    uPID = np.empty((2,1))

    uClamp = np.empty((4,1))
    uClampPID = np.empty((2,1))


    pid2d = Algorithms.PID2D(Dt=1./F_SUSPENSION, 
                             Kp_xy=REGULATOR.P, 
                             Ki_xy=REGULATOR.I, 
                             Td_xy=REGULATOR.D, 
                             Kb_xy=REGULATOR.B)
    pidSplitter = Splitter.Splitter()
    pidEqualizer = Splitter.Equalizer()

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
        e[1][0] = -angXY[1]

        # equalize output
        u[:] = u * pidEqualizer.center(u)

        # calculate output:
        uPID[:] = pid2d.update(e)
        u[:] = u + pidSplitter.splitEven(uPID)
        
        # anti windup:
        uClamp[:] = suspension.setOutputs(u)
        uClampPID[:] = pidSplitter.join(uClamp)
        pid2d.antiWindup(uClampPID)

        # log data to remote
        msg = [time.time()] + angXY + [z] + uPID.tolist() + u.tolist()
        logger.log(msg)

        sync.waitNext()

    suspension.turnOff()
    poseOR.close()
    logger.close()


if __name__ == "__main__":
    main()