from RandomProcess import  *
from SinglePath import *
import numpy as np

class BlackScholes1D(RandomProcess):

    def __init__(self, Gen, spot, rate, vol):
        super(BlackScholes1D, self).__init__(Gen)
        self.spot = spot
        self.rate = rate
        self.vol = vol

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass