from abc import abstractmethod
import sys
sys.path.insert(1, 'C:/Users/Elyès Chenik/Documents/Dauphine/M2/Numerical Finance/BermudanPricing/RandomGenerator')
from RandomGenerator import *

class RandomProcess:

    def __init__(self, Gen, dim = 1):
        self.Gen = Gen
        self.dim = dim
        self.Paths = []

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass

    def SimulateMultiplePaths(self, StartTime, EndTime, NbSteps, NbSim):
        for i in range(NbSim):
            self.Simulate(StartTime, EndTime, NbSteps)

    def GetPath(self, dimension):
        try:
            out = self.Paths[dimension]
        except:
            raise Exception("Simulation out of range")
        return out
