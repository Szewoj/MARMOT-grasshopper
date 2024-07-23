import misc.Logger as Logger
import ahrs
import Sensor.imu6dof as IMU
import numpy as np
import misc.synchronizer as synchro

from misc.InterruptibleLoop import InterruptibleLoop

import threading

G_QUAT = ahrs.Quaternion([0., 0., 0., 1.])

ACC_Z_HOLD = .05
ACC_Z_MOVE = .95

class OrientationReader:
    """Class for automatic orientation filtering. Runs on its own thread"""

    def __init__(self, freq:float=208, port:int=-1) -> None:
        """- freq - frequency of IMU reading in Hz
           - port - TCP/IP port for debugging IMU -- to be used with Matlab/LogIMU.m script"""
        self.imu = IMU.Imu()

        self.FREQ = freq

        self.logger = None
        if port < 1:
            self.doLog = False
        else:
            self.doLog = True
            self.logger = Logger.TCPLogger(port=port)

        # starting aproximated position of IMU (given the car is on the ground)
        self._orientation = np.array([1., 0., 0., 0.])
        self._quatOrientation = ahrs.Quaternion(self._orientation)
        self._accZ = 0.
        self._velZ = 0.

        # setup orientation filter:
        self._orientationFilter = ahrs.filters.madgwick.Madgwick()
        self._orientationFilter.Dt = 1./freq

        self._synchro = synchro.Synchro(freq)

        self._loop = False
        """Asynchronous running flag"""

        # memory protection lock:
        self._atomicOut = np.copy(self._orientation)
        self._atomicAccZ = 0.
        self._atomicVelZ = 0.
        self._lock = threading.Lock()



    def PRIVATE_updateOutput(self) -> None:
        if self._lock.locked():
            return # do not wait to acquire lock
        self._lock.acquire()
        self._atomicOut = np.copy(self._orientation)
        self._atomicAccZ = self._accZ
        self._atomicVelZ = self._velZ
        self._lock.release()
        

    def PRIVATE_calculateZ(self, accSI:np.ndarray) -> None:
        self._quatOrientation = ahrs.Quaternion(self._orientation)
        gRot = ahrs.Quaternion(self._quatOrientation * G_QUAT) * self._quatOrientation.conj
        self._accZ = ACC_Z_HOLD * self._accZ + ACC_Z_MOVE * (accSI[2] - ahrs.MEAN_NORMAL_GRAVITY * gRot[3])
        self._velZ = self._velZ + self._accZ/self.FREQ

    def getRPY(self) -> np.ndarray:
        self._lock.acquire()
        tmp = np.copy(self._atomicOut)
        self._lock.release()

        q = ahrs.Quaternion(tmp)
        return q.to_angles()
    

    def getAccZ(self) -> float:
        self._lock.acquire()
        tmp = self._atomicAccZ
        self._lock.release()

        return tmp
    

    def getVelZ(self) -> float:
        self._lock.acquire()
        tmp = self._atomicVelZ
        self._lock.release()

        return tmp
    

    def getZ(self) -> tuple[float, float, float]:
        self._lock.acquire()
        tmp = (self._atomicAccZ, self._atomicVelZ)
        self._lock.release()

        return tmp


    def PRIVATE_run(self) -> None:
        """Private method. Only for run async use!"""

        if not self.imu.open():
            return
        
        syncInit = False

        while self._loop:
            reading:IMU.Readings = self.imu.getData()

            # update filter timestep
            if not syncInit:
                self._synchro.start()
                syncInit = True

            # update imu position
            self._orientation = self._orientationFilter.updateIMU(self._orientation, reading.getGyroSI(), reading.getAccSI())
            
            # update Z axis filtered acceleration
            self.PRIVATE_calculateZ(reading.getAccSI())

            # update output
            self.PRIVATE_updateOutput()
            
            self._synchro.waitNext()

        self.imu.close()



    def run_async(self) -> None:
        """Run orientation reader on separate thread (asynchronous method). To finish reading use '.close()' method.
           Will not log IMU readings. Instead you can access resulting RPY angles with .getRPY() method."""
        self._loop = True
        self._th = threading.Thread(target=self.PRIVATE_run)
        self._th.start()



    def close(self) -> None:
        self._loop = False



    def run(self) -> None:
        """Run orientation reader on current thread (Method blocks untill program is interrupted with '^C').  
           Allows to debug IMU with Matlab/LogIMU.m script."""
        if self.doLog:
            self.logger.run_async()

        if not self.imu.open():
            return

        loop = InterruptibleLoop()
        syncInit = False

        while loop.loop_again:
            reading:IMU.Readings = self.imu.getData()

            # update filter timestep
            if not syncInit:
                self._synchro.start()
                syncInit = True

            # update imu position
            self._orientation = self._orientationFilter.updateIMU(self._orientation, reading.getGyroSI(), reading.getAccSI())

            # update Z axis filtered acceleration
            self.PRIVATE_calculateAccZ(reading.getAccSI())
            
            # log data
            if self.doLog:
                reading.setOrientation(self._orientation)
                self.logger.log(reading.getList())
            
            self._synchro.waitNext()

        self.imu.close()
        if self.doLog:
            self.logger.close()




def main():
    position = OrientationReader(port=6000)
    position.run()


if __name__ == "__main__":
    main()
