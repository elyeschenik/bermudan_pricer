from RandomProcess import  *
import numpy as np

class BlackScholesND(RandomProcess):

    def __init__(self, Gen, spot, rate, var_covar, dim, antithetic):
        super(BlackScholesND, self).__init__(Gen, dim)
        self.spot = spot
        self.rate = rate
        self.var_covar = var_covar
        self.antithetic = antithetic

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass

    @abstractmethod
    def SimulateAntithetic(self, StartTime, EndTime, NbSteps):
        pass