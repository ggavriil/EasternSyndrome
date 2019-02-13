import time
import board
import digitalio
import busio
import adafruit_lis3dh
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
while True:
    x, y, z = lis3dh.acceleration
    print(x, y, z)
    adc1_raw = lis3dh.read_adc_raw(2)
    adc1_raw = (adc1_raw & 0xFFC0) >> 6
    print(adc1_raw)
# Or read the ADC value in millivolts:
#    adc1_mV = lis3dh.read_adc_mV(2)
#    print('ADC 1 = {} ({} mV)'.format(adc1_raw, adc1_mV))
    time.sleep(5)
