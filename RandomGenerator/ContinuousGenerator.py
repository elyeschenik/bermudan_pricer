from RandomGenerator import *

class ContinuousGenerator(RandomGenerator):
    def __init__(self, targetMean, targetVariance):
        super(ContinuousGenerator, self).__init__()
        self.targetMean = targetMean
        self.targetVariance = targetVariance
    
    @abstractmethod
    def Generate(self):
        pass
    
    def TestMean(self, nbSim, tol):
        return abs(super().Mean(nbSim) - self.targetMean) <= tol

    def TestVariance(self, nbSim, tol):
        return abs(super().Variance(nbSim) - self.targetVariance) <= tol

    

