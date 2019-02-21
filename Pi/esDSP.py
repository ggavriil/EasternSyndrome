import math
import datetime
import time
import board
import digitalio
import busio
import RPi.GPIO as GPIO
import sampling_aggregator as sd
import mqttconnector as mqtt
import vibrcontrol as vc
from functools import reduce
import statistics
from sampler import Sampler


print("Please stand upright and wait for calibration to finish")
time.sleep(3)
sampler = Sampler(10, 0.125)
print("Calibration coefficients: ", sampler.sample_calibrator.cal_phi_x, 
        sampler.sample_calibrator.cal_phi_y, sampler.sample_calibrator.cal_phi_z)


last_slouch_time = datetime.datetime.now()
slouching = False

samplingAggregator = sd.samplingAggregator(5)

while True:   
    features, batt_v = sampler.getSamples()
    curr_time = features.samples[len(features.samples) - 1].timestamp
    delta_time = (curr_time - last_slouch_time).seconds
    current_angle_z = features.mean.angle_z
    # The line below is only needed for the interactive demo
    # mqtt.publish_angle(current_angle_z)
    print("Z-angle Stdev: %.3f Res Acc Stdev: %.3f Z-angle: %.3f Batt: %.2f" % 
            (features.std.angle_z, 
            features.std.resultant, 
            features.samples[len(features.samples)-1].getAngle()[2], batt_v))
    if (current_angle_z > 40 and current_angle_z  < 80) or (current_angle_z >110):
        if not slouching:
            last_slouch_time = curr_time
            slouching = True
    else:
        slouching = False

    if slouching:
        if delta_time > 4:
            print("Slouching")
            vc.vibrate(0.1, 4, -1)
            time.sleep(0.4)
    else:
        last_slouch_time = curr_time

    samplingAggregator.register(sd.samplingData(current_angle_z, features.std.resultant, batt_v, curr_time))






