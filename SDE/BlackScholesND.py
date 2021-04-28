from RandomProcess import  *
from SinglePath import *
import numpy as np

class BlackScholesND(RandomProcess):

    def __init__(self, Gen, spot, rate, var_covar, dim):
        super(BlackScholesND, self).__init__(Gen, dim)
        self.spot = spot
        self.rate = rate
        self.var_covar = var_covar

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass