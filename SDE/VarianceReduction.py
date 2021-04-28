from BlackScholesND import  *
from SinglePath import *
import numpy as np


class VarianceReduction(BlackScholesND):

    def __init__(self, Gen, dim = 1):
        super(VarianceReduction, self).__init__(Gen, dim)
        pass

    @abstractmethod
    def Generate(self):
        pass

    def Mean(self, nbSim):
        return sum([self.Generate() for i in range(nbSim)]) / nbSim

    def Variance(self, nbSim):
        Mean = self.Mean(nbSim)
        return sum([(self.Generate() - Mean)**2 for i in range(nbSim)]) / (nbSim - 1)