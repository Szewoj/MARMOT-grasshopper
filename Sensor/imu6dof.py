import smbus2, time
import Sensor.LSM6DS3 as LSM6DS3
import numpy as np
import ahrs


def toSigned16(n:int) -> int:
    n = n & 0xFFFF
    return (n ^ 0x8000) - 0x8000

#---

class Readings:
    """Class for IMU 6DOF reading data"""
    def __init__(self, ts=0, gx=0, gy=0, gz=0, xlx=0, xly=0, xlz=0) -> None:
        self.timestamp = ts
        self.g_x = gx
        self.g_y = gy
        self.g_z = gz
        self.xl_x = xlx
        self.xl_y = xly
        self.xl_z = xlz
        self.quat_w = 1.0
        self.quat_i = 0.0
        self.quat_j = 0.0
        self.quat_k = 0.0

    def setOrientation(self, quat:np.ndarray):
        self.quat_w = quat.item(0)
        self.quat_i = quat.item(1)
        self.quat_j = quat.item(2)
        self.quat_k = quat.item(3)

    def print(self) -> None:
        print("Gyro: "+ "{0:8.2f} x; ".format(self.g_x)  + 
                        "{0:8.2f} y; ".format(self.g_y)  + 
                        "{0:8.2f} z ".format(self.g_z)  +
              "Accl: "+ "{0:6.2f} x; ".format(self.xl_x) + 
                        "{0:6.2f} y; ".format(self.xl_y) + 
                        "{0:6.2f} z ".format(self.xl_z))
        
    def getTimestamp(self) -> float:
        return self.timestamp
        
    def getList(self) -> list:
        return [self.timestamp, self.g_x, self.g_y, self.g_z, self.xl_x, self.xl_y, self.xl_z, self.quat_w, self.quat_i, self.quat_j, self.quat_k]
    
    def getOrientation(self) -> np.ndarray:
        return np.array([self.quat_w, self.quat_i, self.quat_j, self.quat_k])

    def getGyroSI(self) -> np.ndarray:
        return np.array([self.g_x, self.g_y, self.g_z]) * ahrs.DEG2RAD
    
    def getAccSI(self) -> np.ndarray:
        return np.array([self.xl_x, self.xl_y, self.xl_z]) * ahrs.MEAN_NORMAL_GRAVITY
#---


class Imu:
    """Class for IMU 6DOF actions handling"""
    def __init__(self) -> None:
        self.i2cBus:smbus2.SMBus = None
        self.is_connected = False

    ###
        
    def open(self, bus=1) -> bool:
        self.i2cBus = smbus2.SMBus(bus)
        flag = self.i2cBus.read_byte_data(LSM6DS3.ADDR, LSM6DS3.WHO_AM_I)
        
        if flag != 0x69:
            print("Opening LSM6DS3 failed! WHO_AM_I=", hex(flag))
            self.i2cBus.close()
            return False
        
        self.is_connected = True

        # init LSM6DS3:

        xl_settings = LSM6DS3.XL_ODR_208 | LSM6DS3.XL_FS_4
        g_settings  = LSM6DS3.G_ODR_208 | LSM6DS3.G_FS_1000

        self.i2cBus.write_byte_data(LSM6DS3.ADDR, LSM6DS3.CTRL1_XL, xl_settings)
        self.i2cBus.write_byte_data(LSM6DS3.ADDR, LSM6DS3.CTRL2_G, g_settings)

        return True

    ###

    def close(self) -> None:
        self.i2cBus.close()
        self.is_connected = False

    ###

    def isConnected(self) -> bool:
        return self.is_connected
    
    ###

    def getData(self) -> Readings:
        if not self.is_connected:
            readings = Readings()
            return readings

        ts = time.time()
        data = self.i2cBus.read_i2c_block_data(LSM6DS3.ADDR, LSM6DS3.OUTX_L_G, 12)
        readings = Readings(
                        ts,
                        toSigned16(data[0]  | (data[1] << 8)) * 1000 / 0x7fff - LSM6DS3.G_FS_1000_DRIFT[0],
                        toSigned16(data[2]  | (data[3] << 8)) * 1000 / 0x7fff - LSM6DS3.G_FS_1000_DRIFT[1],
                        toSigned16(data[4]  | (data[5] << 8)) * 1000 / 0x7fff - LSM6DS3.G_FS_1000_DRIFT[2],
                        toSigned16(data[6]  | (data[7] << 8)) * 4   / 0x7fff  * LSM6DS3.XL_FS_4_RESCALE[0],
                        toSigned16(data[8]  | (data[9] << 8)) * 4   / 0x7fff  * LSM6DS3.XL_FS_4_RESCALE[1],
                        toSigned16(data[10] | (data[11] << 8))* 4   / 0x7fff  * LSM6DS3.XL_FS_4_RESCALE[2]
                        )

        return readings

#---


def main():
    
    imu:Imu = Imu()

    if imu.open():
        print("Init OK!")
    time.sleep(1)

    for i in range(100):
        readings = imu.getData()
        readings.print()
        time.sleep(0.1)
        
    imu.close()


#---


if __name__ == "__main__":
    main()
