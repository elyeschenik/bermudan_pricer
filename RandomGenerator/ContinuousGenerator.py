from RandomGenerator import *

class ContinuousGenerator(RandomGenerator):
    def __init__(self, targetMean, targetVariance):
        super(ContinuousGenerator, self).__init__()
        self.targetMean = targetMean
        self.targetVariance = targetVariance

    @abstractmethod
    def Generate(self):
        pass

