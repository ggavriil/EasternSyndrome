import mqttconnector as mqtt
import json
import datetime
import time


# Aggregates multiple data points together. This reduces network overhead.
# We eventually send the slouch angles, the total "activity" metric and
# the battery voltage.

class samplingData:
    def __init__(self, meanAngleZ, stdAcc, adcV, timestamp):
        self.meanAngleZ = meanAngleZ
        self.stdAcc = stdAcc
        self.timestamp = timestamp
        self.adcV = adcV
   
class sampleData:
    def __init__(self, timestamp, meanAngleZ, stdAcc):
        self.meanAngleZ = meanAngleZ
        self.stdAcc = stdAcc
        self.timestamp = timestamp
    def getDict(self):
        return {"meanAngleZ": self.meanAngleZ, "stdAcc": self.stdAcc, "timestamp": time.mktime(self.timestamp.timetuple()),}

class aggregatedSamplingData:
    def __init__(self, samples):
        self.samples = samples



class samplingAggregator:
    def __init__(self, size):
        self.samples = []
        self.size = size
        self.adcV = 0

    def register(self, sample):
        if(len(self.samples) >= self.size):
            samplesDicts = [s.getDict() for s in self.samples]
            aggregatedData = { "samples": samplesDicts, "size": self.size, "adcV": self.adcV, }
            jsons = json.dumps(aggregatedData)
            #print(jsons)
            mqtt.publish(jsons)
            self.samples = []    
            self.adcV = 0
        self.samples.append(sampleData(sample.timestamp, sample.meanAngleZ, sample.stdAcc))
        self.adcV = self.adcV + sample.adcV / self.size
    
    
