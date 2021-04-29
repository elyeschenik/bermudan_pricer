from VarianceReduction import *
from scipy.stats import norm

class PseudoControlVariate(VarianceReduction):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha):
        super(PseudoControlVariate, self).__init__()
        self.model = BSEulerND(Gen, spot, rate, vol, dim)
        self.f_CV = lambda x: np.exp(-rate * maturity) * (max(np.dot(alpha.T, x)[0,0] - strike, 0) - max(np.exp(np.dot(alpha.T, np.log(x))[0,0]), 0))

    def compute(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)
        price = sum([self.f_CV(path.GetValue(self.maturity)) for path in self.model.Paths])/NbSim



