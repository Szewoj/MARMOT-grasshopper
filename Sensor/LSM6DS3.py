# LSM6DS3 address:
ADDR = 0x6A

# LSM6DS3 registers:
WHO_AM_I    = 0x0F
CTRL1_XL    = 0x10
CTRL2_G     = 0x11

OUTX_L_G    = 0x22
OUTX_H_G    = 0x23
OUTY_L_G    = 0x24
OUTY_H_G    = 0x25
OUTZ_L_G    = 0x26
OUTZ_H_G    = 0x27
OUTX_L_XL   = 0x28
OUTX_H_XL   = 0x29
OUTY_L_XL   = 0x2A
OUTY_H_XL   = 0x2B
OUTZ_L_XL   = 0x2C
OUTZ_H_XL   = 0x2D

# Measurement range:
XL_FS_2     = 0b00000000
XL_FS_4     = 0b00001000
XL_FS_8     = 0b00001100
XL_FS_16    = 0b00000100

G_FS_125    = 0b00000010
G_FS_245    = 0b00000000
G_FS_500    = 0b00000100
G_FS_1000   = 0b00001000
G_FS_2000   = 0b00001100

# ODR settings

XL_ODR_OFF  = 0b00000000
XL_ODR_12   = 0b00010000
XL_ODR_26   = 0b00100000
XL_ODR_52   = 0b00110000
XL_ODR_104  = 0b01000000
XL_ODR_208  = 0b01010000
XL_ODR_416  = 0b01100000
XL_ODR_833  = 0b01110000
XL_ODR_1666 = 0b10000000
XL_ODR_3332 = 0b10010000
XL_ODR_6664 = 0b10100000

G_ODR_OFF  = 0b00000000
G_ODR_12   = 0b00010000
G_ODR_26   = 0b00100000
G_ODR_52   = 0b00110000
G_ODR_104  = 0b01000000
G_ODR_208  = 0b01010000
G_ODR_416  = 0b01100000
G_ODR_833  = 0b01110000
G_ODR_1666 = 0b10000000

# Anti aliasing filter

XL_AABW_400 = 0b00000000
XL_AABW_200 = 0b00000001
XL_AABW_100 = 0b00000010
XL_AABW_50  = 0b00000011
