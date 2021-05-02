from RandomProcess import  *
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

    def SimulateAntithetic(self, StartTime, EndTime):
        Path1 = SinglePath(StartTime, EndTime, 1)
        Path2 = SinglePath(StartTime, EndTime, 1)
        Path1.AddValue(self.spot)
        Path2.AddValue(self.spot)
        dt = Path1.timeStep
        lastInserted = self.spot

        W1 = self.Gen.GenerateVector(self.dim)
        W2 = - W1
        nextValue1 = lastInserted * np.exp(
            (self.rate - 0.5 * (self.B ** 2).sum(1)) * dt + np.dot(self.B, W1) * np.sqrt(dt))
        nextValue2 = lastInserted * np.exp(
            (self.rate - 0.5 * (self.B ** 2).sum(1)) * dt + np.dot(self.B, W2) * np.sqrt(dt))
        Path1.AddValue(nextValue1)
        Path2.AddValue(nextValue2)

        self.Paths.append(Path1)
        self.Paths.append(Path2)