import smbus2, time
import LSM6DS3


def toSigned16(n:int) -> int:
    n = n & 0xFFFF
    return (n ^ 0x8000) - 0x8000


class Readings:
    """Class for IMU 6DOF reading data"""
    def __init__(self) -> None:
        self.g_x = 0
        self.g_y = 0
        self.g_z = 0
        self.xl_x = 0
        self.xl_y = 0
        self.xl_z = 0

    def print(self) -> None:
        print("Gyro: "+ "{0:8.2f} x; ".format(self.g_x)  + 
                        "{0:8.2f} y; ".format(self.g_y)  + 
                        "{0:8.2f} z ".format(self.g_z)  +
              "Accl: "+ "{0:6.2f} x; ".format(self.xl_x) + 
                        "{0:6.2f} y; ".format(self.xl_y) + 
                        "{0:6.2f} z ".format(self.xl_z))



def init(bus:smbus2.SMBus) -> bool:

    xl_settings = LSM6DS3.XL_ODR_416 | LSM6DS3.XL_FS_4
    g_settings  = LSM6DS3.G_ODR_416 | LSM6DS3.G_FS_1000

    bus.write_byte_data(LSM6DS3.ADDR, LSM6DS3.CTRL1_XL, xl_settings)
    bus.write_byte_data(LSM6DS3.ADDR, LSM6DS3.CTRL2_G, g_settings)
    
    return True

#---

def read(bus:smbus2.SMBus) -> Readings:

    
    data = bus.read_i2c_block_data(LSM6DS3.ADDR, LSM6DS3.OUTX_L_G, 12)
    readings = Readings()
    readings.g_x  = toSigned16(data[0]  | (data[1] << 8)) * 1000 / 0x7fff
    readings.g_y  = toSigned16(data[2]  | (data[3] << 8)) * 1000 / 0x7fff
    readings.g_z  = toSigned16(data[4]  | (data[5] << 8)) * 1000 / 0x7fff
    readings.xl_x = toSigned16(data[6]  | (data[7] << 8)) * 4   / 0x7fff
    readings.xl_y = toSigned16(data[8]  | (data[9] << 8)) * 4   / 0x7fff
    readings.xl_z = toSigned16(data[10] | (data[11] << 8))* 4   / 0x7fff

    return readings


#---


def main():
    with smbus2.SMBus(1) as bus:
        flag = bus.read_byte_data(LSM6DS3.ADDR, LSM6DS3.WHO_AM_I)
        print("WHO_AM_I value is: " + hex(flag))
        if init(bus):
            print("Init OK!")

        time.sleep(1)

        for i in range(100):
            readings = read(bus)
            readings.print()
            time.sleep(0.1)

        



#---


if __name__ == "__main__":
    main()
