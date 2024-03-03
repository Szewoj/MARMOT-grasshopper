import Logger
import Sensor.imu6dof as IMU
import time


def main():
    imu = IMU.Imu()
    if not imu.open():
        return

    logger = Logger.TCPLogger()
    logger.connect()
        

    for i in range(100):
        reading:IMU.Readings = imu.getData()
        logger.log(reading.getList())
        reading.print()
        time.sleep(0.1)

    imu.close()
    logger.close()


if __name__ == "__main__":
    main()