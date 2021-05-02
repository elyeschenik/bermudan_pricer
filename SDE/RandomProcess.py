from abc import abstractmethod
import sys
from scipy.stats import t
sys.path.insert(1, '../RandomGenerator')
from RandomGenerator import *
from SinglePath import *

class RandomProcess:

    def __init__(self, Gen, dim = 1):
        self.Gen = Gen
        self.dim = dim
        self.Paths = []

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass

    @abstractmethod
    def SimulateAntithetic(self, StartTime, EndTime, NbSteps):
        pass

    def ClearPaths(self):
        self.Paths = []

    def SimulateMultiplePaths(self, StartTime, EndTime, NbSteps, NbSim):
        self.ClearPaths()
        for i in range(NbSim):
            self.Simulate(StartTime, EndTime, NbSteps)

    def SimulateMultiplePathsAntithetic(self, StartTime, EndTime, NbSteps, NbSim):
        self.ClearPaths()
        for i in range(NbSim):
            self.SimulateAntithetic(StartTime, EndTime, NbSteps)

    def GetPath(self, dimension):
        try:
            out = self.Paths[dimension]
        except:
            raise Exception("Simulation out of range")
        return out

    def GetVariance(self, f, time):
        if len(self.Paths) > 1:
            return np.var([f(path.GetValue(time)) for path in self.Paths])
        else:
            raise Exception("Not enough simulations to compute the variance")

    def GetIterationNumber(self, eps, alpha, f, time):
        #alpha = 5% for instance
        n = len(self.Paths)
        Sn = self.GetVariance(f, time)
        t_alpha = t.cdf(1 - 0.5 * alpha, n - 1)
        return int((t_alpha**2 * Sn) / eps**2)
