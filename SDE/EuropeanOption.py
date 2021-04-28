from Option import *
from BSEuler1D import *
from BSEulerND import *

class EuropeanBasketOption(Option):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha):
        super(EuropeanBasketOption, self).__init__(spot, strike, rate, vol, maturity, Gen)

        if dim <= 1:
            raise Exception("Please input a dimension with values >= 2. If dim=1, use a single name class instead")
        if spot.shape != (dim, 1):
            raise Exception(
                "Wrong shape for the current spot price, please input a numpy array of shape ({},1)".format(dim))
        if vol.shape != (dim, dim):
            raise Exception(
                "Wrong shape for the var-covar matrix, please input a numpy array of shape ({},{})".format(dim,
                                                                                                           dim))
        if alpha.shape != (dim, 1):
            raise Exception("Wrong shape for the weights, please input a numpy array of shape ({},1)".format(dim))

        self.dim = dim
        self.alpha = alpha
        self.model = BSEulerND(Gen, spot, rate, vol, dim)

    def ComputePrice(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)

        price = np.exp(-self.rate * self.maturity) * sum([self.f(np.dot(self.alpha.T, path.GetValue(self.maturity))[0, 0]) for path in self.model.Paths]) / NbSim
        return price

class EuropeanSingleNameOption(Option):

    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        super(EuropeanSingleNameOption, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.model = BSEuler1D(Gen, spot, rate, vol)

    def ComputePrice(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)

        price = np.exp(-self.rate * self.maturity) * sum(
            [self.f(path.GetValue(self.maturity)) for path in self.model.Paths]) / NbSim
        return price


class EuropeanBasketCall(EuropeanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha):
        super(EuropeanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha)
        self.f = lambda s: max(s - self.strike, 0)



class EuropeanSingleNameCall(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        super(EuropeanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.f = lambda s: max(s - self.strike, 0)



class EuropeanBasketPut(EuropeanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha):
        super(EuropeanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha)
        self.f = lambda s: max(self.strike - s, 0)


class EuropeanSingleNamePut(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        super(EuropeanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.f = lambda s: max(self.strike - s, 0)

