from RandomGenerator import *

class UniformGenerator(RandomGenerator):
    def __init__(self):
        super(UniformGenerator, self).__init__()
        self.targetMean = 0.5
        self.targetVariance = 1/12

    @abstractmethod
    def Generate(self):
        pass

    def TestMean(self, nbSim, tol):
        return abs(super().Mean(nbSim) - self.targetMean) <= tol

    def TestVariance(self, nbSim, tol):
        return abs(super().Variance(nbSim) - self.targetVariance) <= tol

