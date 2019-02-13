import math
import datetime
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import RPi.GPIO as GPIO
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)


#Each sample provides a total of 7 parameters: 6DOF (3 acceleration + 3 rotation) + 1 resultant acceleration. In reality the accelerometer provides only 3 and the additional 4 are calculated
class sample:
#Ideal  calibration standards for the calibration positon in use - eg 180 90 90 = standing
	cal_ideal_phi_x=180
	cal_ideal_phi_y=90
	cal_ideal_phi_z=90
#Calibration constants common to all sample instances
	cal_phi_x=0
	cal_phi_y=0
	cal_phi_z=0
	
	@staticmethod
	def calibrate(x,y,z):
		l=math.sqrt(pow(x,2)+pow(y,2)+pow(z,2)) 
		sample.cal_phi_x,sample.cal_phi_y,sample.cal_phi_z=sample.cal_ideal_phi_x-(180/math.pi)*math.acos(x/l),sample.cal_ideal_phi_y-(180/math.pi)*math.acos(y/l),sample.cal_ideal_phi_z-(180/math.pi)*math.acos(z/l)


	def __init__(self,x,y,z):
		self.acc_x=x
		self.acc_y=y
		self.acc_z=z
		self.timestamp = datetime.datetime.now()

	def resultant(self):
		return math.sqrt(pow(self.acc_x,2)+pow(self.acc_y,2)+pow(self.acc_z,2))

	def getAngle(self):
		l = self.resultant()
		return (180/math.pi)*math.acos(self.acc_x/l)+sample.cal_phi_x,(180/math.pi)*math.acos(self.acc_y/l)+sample.cal_phi_y,(180/math.pi)*math.acos(self.acc_z/l)+sample.cal_phi_z


#Each feature( eg mean) can be for one of these parameters
class W_feature_paramters:
	def __init__(self,a,b,c,d,e,f,g):
		self.acc_x = a
		self.acc_y= b
		self.acc_z=c
		self.angle_x = d
		self.angle_y = e
		self.angle_z = f
		self.resultant = g

#class of all features 
class W_features:
	def __init__(self,a,b,c,d):
		self.samples = a
		self.mean = b
		self.std = c
		self.ddt = d		



def vib_init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.OUT)
	return


def vib_on():
	GPIO.output(26, GPIO.HIGH)
	return



def vib_off():
	GPIO.output(26, GPIO.LOW)
	return	
	
class feature:

#Size of window in number of samples
	window_size = 10
#sample period
	sample_period= 0.125

	def __init__(self):		
		self.samples=[]

#Private method for the actual samples to be taken in the window
	def __sample(self):
		for i in range(feature.window_size):	
			x,y,z= lis3dh.acceleration
			s= sample(x,y,z)
			self.samples.append(s)
			time.sleep(feature.sample_period)
	
#Mean of of the 7 parameters in the window
	def Wmean(self):
		mean_acc_x=sum(sample.acc_x for sample in self.samples)/len(self.samples)
		mean_acc_y=sum(sample.acc_y for sample in self.samples)/len(self.samples)
		mean_acc_z=sum(sample.acc_z for sample in self.samples)/len(self.samples)
		mean_angle_x=sum(sample.getAngle()[0] for sample in self.samples)/len(self.samples)
		mean_angle_y=sum(sample.getAngle()[1] for sample in self.samples)/len(self.samples)
		mean_angle_z=sum(sample.getAngle()[2] for sample in self.samples)/len(self.samples)
		mean_resultant=sum(sample.resultant() for sample in self.samples)/len(self.samples)
		W_mean = W_feature_paramters(mean_acc_x,mean_acc_y,mean_acc_z,mean_angle_x,mean_angle_y,mean_angle_z,mean_resultant)
		return W_mean

#STD of of the 7 parameters in the window
	def Wstd(self):
		std_acc_x=math.sqrt(sum(math.pow(sample.acc_x-self.Wmean().acc_x,2) for sample in self.samples)/len(self.samples))
		std_acc_y=math.sqrt(sum(math.pow(sample.acc_y-self.Wmean().acc_y,2) for sample in self.samples)/len(self.samples))
		std_acc_z=math.sqrt(sum(math.pow(sample.acc_z-self.Wmean().acc_z,2) for sample in self.samples)/len(self.samples))
		std_angle_x=math.sqrt(sum(math.pow(sample.getAngle()[0]-self.Wmean().angle_x,2) for sample in self.samples)/len(self.samples))
		std_angle_y=math.sqrt(sum(math.pow(sample.getAngle()[1]-self.Wmean().angle_y,2) for sample in self.samples)/len(self.samples))
		std_angle_z=math.sqrt(sum(math.pow(sample.getAngle()[2]-self.Wmean().angle_z,2) for sample in self.samples)/len(self.samples))
		std_resultant=math.sqrt(sum(math.pow(sample.resultant()-self.Wmean().resultant,2) for sample in self.samples)/len(self.samples))
		W_std = W_feature_paramters(std_acc_x,std_acc_y,std_acc_z,std_angle_x,std_angle_y,std_angle_z,std_resultant)
		return W_std

#Average absolute two point derivative of the 7 parameters in the window
	def Wddt(self):
		ddt_acc_x = sum([x.acc_x-y.acc_x for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)  
		ddt_acc_y= sum([x.acc_y-y.acc_y for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)  
		ddt_acc_z= sum([x.acc_z-y.acc_z for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)   
		ddt_angle_x = sum([x.getAngle()[0]-y.getAngle()[0] for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)  
		ddt_angle_y =sum([x.getAngle()[1]-y.getAngle()[1] for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)  
		ddt_angle_z = sum([x.getAngle()[2]-y.getAngle()[2] for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)    
		ddt_resultant = sum([x.resultant()-y.resultant() for x, y in zip(self.samples, self.samples[1:])])/(feature.sample_period*feature.window_size)  
		W_ddt = W_feature_paramters(ddt_acc_x,ddt_acc_y,ddt_acc_z,ddt_angle_x,ddt_angle_y,ddt_angle_z,ddt_resultant)
		return W_ddt

#Samples and returns a list of lists containing samples, Wmean, Wrms, Wstd, Wdldt
	def extract(self):
		self.__sample()
		f  = W_features(self.samples,self.Wmean(),self.Wstd(),self.Wddt())
		return f




	
vib_init()	
vib_off()		


print("Please stand upright and wait for calibration to finish")
time.sleep(3)
x,y,z = lis3dh.acceleration
sample.calibrate(x,y,z)
print("Calibration coefficients: ",sample.cal_phi_x,sample.cal_phi_y,sample.cal_phi_z)


last_slouch_time = datetime.datetime.now()
slouching = False


while True:   
	f= feature()
	myfeatures = f.extract()
	curr_time =f.samples[len(f.samples)-1].timestamp
	delta_time = (curr_time - last_slouch_time).seconds
	current_angle_z= myfeatures.mean.angle_z
	print("Std of Z angle ", myfeatures.std.angle_z, "Std of resultant acc ", myfeatures.std.resultant,"Current Z angle", myfeatures.samples[len(myfeatures.samples)-1].getAngle()[2])
	batt_v = ((470+330)/(330))*(1.8/1024)*((lis3dh.read_adc_raw(2) & 0xffc0)>>6) - 0.32
	print("Battery Level: ", batt_v)
	if (current_angle_z > 40 and current_angle_z  < 80) or (current_angle_z >110):
		if not slouching:
			last_slouch_time = curr_time
		slouching = True
	else:
		slouching = False
		
	if slouching:
		if delta_time >8:
			print("Slouching")
			vib_on()
			time.sleep(0.1)
			vib_off() 
	else:
		last_slouch_time = curr_time

    
	
	

   # adc1_raw = lis3dh.read_adc_raw(2) adc1_raw = (adc1_raw & 0xFFC0) >> 6
   # print(adc1_raw)
# Or read the ADC value in millivolts:
#    adc1_mV = lis3dh.read_adc_mV(2) print('ADC 1 = {} ({} mV)'.format(adc1_raw, adc1_mV))
  
	

		
