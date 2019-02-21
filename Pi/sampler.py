import math
import datetime
import time
import board
import digitalio
import busio
import ES_LIS3DH
import RPi.GPIO as GPIO
import mqttconnector as mqtt
import vibrcontrol as vc
from functools import reduce
import statistics

lis3dh = ES_LIS3DH.ES_LIS3DH()
rad_to_deg = 180 / math.pi

#Each sample provides a total of 7 parameters: 6DOF (3 acceleration + 3 rotation) + 1 resultant acceleration. In reality the accelerometer provides only 3 and the additional 4 are calculated
class SampleCalibrator:
    #Ideal  calibration standards for the calibration positon in use 
    # eg 180 90 90 = standing
    cal_ideal_phi_x=180
    cal_ideal_phi_y=90
    cal_ideal_phi_z=90
    #Calibration constants common to all sample instances
    cal_phi_x=0
    cal_phi_y=0
    cal_phi_z=0
    
    def __init__(self, x, y, z):
        l = math.sqrt(x ** 2 + y ** 2 + z ** 2) 
        self.cal_phi_x = self.cal_ideal_phi_x - rad_to_deg * math.acos(x / l)
        self.cal_phi_y = self.cal_ideal_phi_y - rad_to_deg * math.acos(y / l)
        self.cal_phi_z = self.cal_ideal_phi_z - rad_to_deg * math.acos(z / l)

    def getCalibratedSample(self, x, y, z):
        return SampleCalibrator.Sample(x, y, z, self)

    class Sample:
        def __init__(self, x, y, z, sample_calibrator):
            self.acc_x=x
            self.acc_y=y
            self.acc_z=z
            self.timestamp = datetime.datetime.now()
            self.sample_calibrator = sample_calibrator

        def resultant(self):
            return math.sqrt(self.acc_x ** 2 + self.acc_y ** 2 + self.acc_z ** 2)

        def getAngle(self):
            l = self.resultant()
            return (rad_to_deg * math.acos(self.acc_x/l) + self.sample_calibrator.cal_phi_x, 
        rad_to_deg * math.acos(self.acc_y/l) + self.sample_calibrator.cal_phi_y,
        rad_to_deg * math.acos(self.acc_z/l) + self.sample_calibrator.cal_phi_z)


#Each feature( eg mean) can be for one of these parameters
class W_feature_parameters:
    def __init__(self, acX, acY, acZ, anX, anY, anZ, res):
        self.acc_x = acX
        self.acc_y = acY
        self.acc_z = acZ  
        self.angle_x = anX
        self.angle_y = anY
        self.angle_z = anZ
        self.resultant = res

#class of all features 
class W_features:
    def __init__(self, samples, mean, std, ddt):
        self.samples = samples
        self.mean = mean
        self.std = std
        self.ddt = ddt		



class Sampler:

    #Size of window in number of samples
    window_size = 10
    #sample period
    sample_period= 0.125

    def __init__(self, window_size, sample_period):		
        self.samples=[]
        self.window_size = window_size
        self.sample_period = sample_period
        calX, calY, calZ = lis3dh.read_accel()
        self.sample_calibrator = SampleCalibrator(calX, calY, calZ)
    
    #Private method for the actual samples to be taken in the window
    def __sample(self):
        self.samples=[]
        for i in range(self.window_size):	
            x,y,z = lis3dh.read_accel()
            s = self.sample_calibrator.getCalibratedSample(x,y,z)
            self.samples.append(s)
            time.sleep(self.sample_period)


    def __getMean(self, fun):
        s = reduce(lambda x, y: x + y, map(fun, self.samples))
        return s / len(self.samples)
        
    def __getStdev(self, fun):
        ll = map(fun, self.samples)
        return statistics.stdev(ll)
        
    def __getDdt(self, fun):
        ll = zip(self.samples, self.samples[1:])
        ll = [fun(x) - fun(y) for x, y in ll]
        total_time = self.sample_period * self.window_size
        return sum(ll) / total_time

    #Mean of of the 7 parameters in the window
    def __Wmean(self):
        mean_acc_x = self.__getMean(lambda s: s.acc_x)
        mean_acc_y = self.__getMean(lambda s: s.acc_y)
        mean_acc_z = self.__getMean(lambda s: s.acc_z)
        mean_angle_x = self.__getMean(lambda s: s.getAngle()[0])
        mean_angle_y = self.__getMean(lambda s: s.getAngle()[1])
        mean_angle_z = self.__getMean(lambda s: s.getAngle()[2])
        mean_resultant = self.__getMean(lambda s: s.resultant())
        W_mean = W_feature_parameters(mean_acc_x,mean_acc_y,mean_acc_z,mean_angle_x,mean_angle_y,mean_angle_z,mean_resultant)
        return W_mean

    #STD of of the 7 parameters in the window
    def __Wstd(self):
        std_acc_x = self.__getStdev(lambda s: s.acc_x)
        std_acc_y = self.__getStdev(lambda s: s.acc_y)
        std_acc_z = self.__getStdev(lambda s: s.acc_z)
        std_angle_x = self.__getStdev(lambda s: s.getAngle()[0])
        std_angle_y = self.__getStdev(lambda s: s.getAngle()[1])
        std_angle_z = self.__getStdev(lambda s: s.getAngle()[2])
        std_resultant = self.__getStdev(lambda s: s.resultant())
        W_std = W_feature_parameters(std_acc_x,std_acc_y,std_acc_z,std_angle_x,std_angle_y,std_angle_z,std_resultant)
        return W_std

    #Average absolute two point derivative of the 7 parameters in the window
    def __Wddt(self):
        ddt_acc_x = self.__getDdt(lambda s: s.acc_x)
        ddt_acc_y = self.__getDdt(lambda s: s.acc_y)
        ddt_acc_z = self.__getDdt(lambda s: s.acc_z)
        ddt_angle_x = self.__getDdt(lambda s: s.getAngle()[0])
        ddt_angle_y = self.__getDdt(lambda s: s.getAngle()[1])
        ddt_angle_z = self.__getDdt(lambda s: s.getAngle()[2])
        ddt_resultant = self.__getDdt(lambda s: s.resultant())
        W_ddt = W_feature_parameters(ddt_acc_x,ddt_acc_y,ddt_acc_z,ddt_angle_x,ddt_angle_y,ddt_angle_z,ddt_resultant)
        return W_ddt

    #Samples and returns a list of lists containing samples, Wmean, Wrms, Wstd, Wdldt
    def getSamples(self):
        self.__sample()
        f  = W_features(self.samples, self.__Wmean(),self.__Wstd(),self.__Wddt())
        adc_v  = lis3dh.read_adc_scaled(2)
        batt_v = ((470 + 330) / 330) * adc_v
        return (f, batt_v)








