from misc import Logger 
from misc import InterruptibleLoop
from misc import synchronizer
import numpy as np
import time
import Actuator.motors
import position
from Regulation import Splitter, Algorithms, Parameters



REGULATOR = Parameters.PID_XY_V3

F_SUSPENSION = REGULATOR.FREQ

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
    logger = Logger.TCPLogger(skip=REGULATOR.SKIP)
    sync = synchronizer.Synchro(F_SUSPENSION)
    
    # regulation components:
    u = np.empty((4,1))
    u.fill(50.)
    e = np.empty((2,1))
    uPID = np.empty((2,1))
    out = np.empty(3)
    logAngle = np.empty(2,dtype=float)

    uClamp = np.empty((4,1))
    uClampPID = np.empty((2,1))


    pid2d = Algorithms.PID2D(Dt=1./F_SUSPENSION, 
                             Kp_xy=REGULATOR.P, 
                             Ki_xy=REGULATOR.I, 
                             Td_xy=REGULATOR.D, 
                             Kb_xy=REGULATOR.B,
                             Kx_xy=REGULATOR.X)
    pidSplitter = Splitter.Splitter()
    pidEqualizer = Splitter.Equalizer()

    # start threads
    poseOR.run_async()
    logger.run_async()


    # ready 
    suspension = Suspension()
    suspension.turnOff()

    print("Regulation starting in 1 second...")
    time.sleep(1.0)
    
    sync.start()
    print("Started!")
    while loop.loop_again:
        out[:] = poseOR.getRPY()
        z = poseOR.getZ()

        angXY = [1000*out[0], 1000*out[1]] #[roll, pitch]

        e[0][0] = round(-angXY[0],1)
        e[1][0] = round(-angXY[1],1)

        # equalize output
        u[:] = u + pidEqualizer.center(u)

        # calculate output:
        uPID[:] = pid2d.update(e)

        #u[:] = u + np.round(pidSplitter.splitEven(uPID),1)
        #u[:] = u + np.round(pidSplitter.splitCentering(uPID, u),1)
        u[:] = u + np.round(pidSplitter.splitByZ(uPID, u, z[1]),1)


        # anti windup:
        uClamp[:] = suspension.setOutputs(u)
        uClampPID[:] = pidSplitter.join(uClamp)
        pid2d.antiWindup(uClampPID)
        u[:] = np.clip(u, 0, 100)

        # log data to remote
        logAngle[:] = np.array(angXY, dtype=float)
        msg = [time.time()] \
                + logAngle.squeeze().tolist() \
                + [z[1]] \
                + uPID.astype(float).squeeze().tolist() \
                + pid2d._uP.astype(float).squeeze().tolist() \
                + pid2d._uI.astype(float).squeeze().tolist() \
                + pid2d._uD.astype(float).squeeze().tolist() \
                + u.astype(float).squeeze().tolist()
        logger.log(msg)

        sync.waitNext()

    suspension.turnOff()
    poseOR.close()
    logger.close()


if __name__ == "__main__":
    main()