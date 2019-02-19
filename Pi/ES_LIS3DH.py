import smbus

BOOT     = 0x80
Z_EN     = 0x04
Y_EN     = 0x02
X_EN     = 0x01
RATE_400 = 0b01110000
BDU_EN   = 0x80
HR_EN    = 0x08
ADC_EN   = 0x80

CTRL_REG1    = 0x20
CTRL_REG4    = 0x23
CTRL_REG5    = 0x24
TEMP_CFG_REG = 0x1F

OUT_X_L = 0x28
OUT_X_H = 0x29
OUT_Y_L = 0x2A
OUT_Y_H = 0x2B
OUT_Z_L = 0x2C
OUT_Z_H = 0x2D

LIS3DH_ADDR  = 0x18

G_TO_MPSS = 9.80665

SCALE_FACTOR = 2 << 14

class ES_LIS3DH:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Reboot memory content (8.12/32)
        self.write_byte(CTRL_REG5, BOOT)
        time.sleep(0.5) #TODO
        # Enable X, Y and Z axes, 400Hz update rate, Normal Power Mode (8.8/29)
        self.write_byte(CTRL_REG1, Z_EN | Y_EN | X_EN | RATE_400)
        # Enable Block Data Update and HiRes mode. Little endian. (8.11/31)
        # BDU avoids race conditions when reading LSB/MSB (not between axes)
        # Scale is the default +/- 2g
        self.write_byte(CTRL_REG4, BDU_EN | HR_EN)
        # Enable ADCs (8.7/29)
        self.write_byte(TEMP_CFG_REG, ADC_EN)

    def read_accel(self):
        xyz = [self.read_short(OUT_X_L), y = self.read_short(OUT_Y_L),
               self.read_short(OUT_Z_L)]
        xyz = (v / SCALE_FACTOR) * G_TO_MPSS for v in xyz
        return (xyz[0], xyz[1], xyz[2])
         

    def write_byte(self, reg, data):
        bus.write_byte_data(LIS3DH_ADDR, reg, data)

    def read(self, reg, size):
        arr = []
        for i in range(len(size)):
                arr.append(self.bus.read_byte_data(LIS3DH_ADDR, reg + i))
        return arr

    def read_short(self, reg):
        data = self.read(reg, 2)
        num = data[0] & (data[1] << 4)
        # Convert 2s complement to decimal
        num = num - (2 << 15) * ((num & 0x8000) >> 15)
        return num

