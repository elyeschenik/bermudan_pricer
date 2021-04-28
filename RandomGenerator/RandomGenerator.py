from abc import abstractmethod
import numpy as np

class RandomGenerator:

    def __init__(self):
        pass

    @abstractmethod
    def Generate(self):
        pass

    def GenerateVector(self, size):
        return np.array([[self.Generate()] for i in range(size)])

    def Mean(self, nbSim):
        return sum([self.Generate() for i in range(nbSim)]) / nbSim

    def Variance(self, nbSim):
        Mean = self.Mean(nbSim)
        return sum([(self.Generate() - Mean)**2 for i in range(nbSim)]) / (nbSim - 1)