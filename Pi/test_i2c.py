import time
import ES_LIS3DH as el

s = el.ES_LIS3DH()

while True:
    x, y, z = s.read_accel()
    v = s.read_adc_scaled(2)
    print("%.3f %.3f %.3f %d" % (x, y, z, v))
    time.sleep(0.5) 
