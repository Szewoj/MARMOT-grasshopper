import misc.Logger as Logger, ahrs
import Sensor.imu6dof as IMU
import numpy as np
import misc.synchronizer as synchro

from misc.InterruptibleLoop import InterruptibleLoop

class OrientationReader:
    """Class for automatic orientation filtering. Runs on its own thread"""

    def __init__(self, port=6000) -> None:
        self.imu = IMU.Imu()
        self.logger = Logger.TCPLogger(port)

def main():
    imu = IMU.Imu()
    if not imu.open():
        return

    logger = Logger.TCPLogger(port=6000)
    logger.run_async()
    
    loop = InterruptibleLoop()

    # Complementary IMU filter:
    orientationFilter = ahrs.filters.madgwick.Madgwick()
    orientationFilter.Dt = 0.0048 # 208 Hz
    orientation = np.array([1., 0., 0., 0.])

    # synchronizer:
    sync = synchro.Synchro(orientationFilter.Dt)
    syncInit = False

    while loop.loop_again:
        reading:IMU.Readings = imu.getData()

        # update filter timestep
        if not syncInit:
            sync.start(reading.getTimestamp())

        # update imu position
        orientation = orientationFilter.updateIMU(orientation, reading.getGyroSI(), reading.getAccSI())
        
        # log data
        reading.setOrientation(orientation)
        logger.log(reading.getList())
        
        sync.waitNext()

    imu.close()
    logger.close()


if __name__ == "__main__":
    main()
