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


class aggregatedSamplingData:
    def __init__(self, samples):
        self.samples = samples



class samplingAggregator:

    def __init__(self, size)
        self.samples = []
        self.size = size
        self.adcV = 0

    def register(sample):
        if(len(self.samples) > self.size):
            #TODO: send
            self.samples = []    
        samples.append(sampleData(sample.timestamp, sample.meanAngleZ, sample.stdAcc)
        self.adcV = self.adcV + sample.adcV / self.size
    
    
