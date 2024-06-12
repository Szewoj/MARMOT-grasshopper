import Logger, time, ahrs
import Sensor.imu6dof as IMU
import numpy as np

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
    orientation = np.array([1., 0., 0., 0.])

    # timestamps:
    t_now = 0
    t_then = 0

    while loop.loop_again:
        reading:IMU.Readings = imu.getData()

        # update filter timestep
        t_now = reading.timestamp
        if t_then == 0:
            orientationFilter.Dt = 0.05
        else:
            orientationFilter.Dt = t_now - t_then

        # update imu position
        orientation = orientationFilter.updateIMU(orientation, reading.getGyroSI(), reading.getAccSI())
        
        # log data
        reading.setOrientation(orientation)
        logger.log(reading.getList())
        #reading.print()
        t_then = t_now
        time.sleep(0.005)

    imu.close()
    logger.close()


if __name__ == "__main__":
    main()
