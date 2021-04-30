from Option import *
from BSEuler1D import *
from BSEulerND import *

class EuropeanOption(Option):
    def __init__(self, spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel):
        super(EuropeanOption, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel)



    def ComputePrice(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)
        price = np.exp(-self.rate * self.maturity) * sum(
            [self.f(path.GetValue(self.maturity)) for path in self.model.Paths]) / NbSim
        self.Variance = self.model.GetVariance(self.f, self.maturity)
        return price

    def ComputePricePCV(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)
        basket_var = np.dot(self.alpha.T, np.dot(self.vol, self.alpha))[0, 0]
        sigma_squared = (self.model.B ** 2)

        S_0 = np.prod([self.spot[i, 0] ** self.alpha[i, 0] for i in range(self.dim)])
        K = self.strike
        r = self.rate - 0.5 * np.dot(self.alpha.T, sigma_squared.sum(axis=1))[0] + 0.5 * basket_var
        sigma = np.sqrt(basket_var)
        T = self.maturity

        ExpectationY = self.BSClosedForm(S_0, K, r, sigma, T, True)

        price = np.exp(-self.rate * self.maturity) * sum(
            [self.f_PCV(path.GetValue(self.maturity)) for path in self.model.Paths]) / NbSim + ExpectationY

        self.Variance = self.model.GetVariance(self.f, self.maturity)
        self.VariancePCV = self.model.GetVariance(self.f_PCV, self.maturity)
        self.MinSim = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f, self.maturity)
        self.MinSimPCV = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f_PCV, self.maturity)

        self.VarReductionInfo(price)

        return price

class EuropeanBasketOption(EuropeanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, eps, ConfidenceLevel):
        super(EuropeanBasketOption, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel)
        try:
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
        except:
            raise Exception("Please make sure that the spot, var-covar and alpha are numpy arrays")

        self.dim = dim
        self.alpha = alpha
        self.model = BSEulerND(Gen, spot, rate, vol, dim)


class EuropeanSingleNameOption(EuropeanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel):
        super(EuropeanSingleNameOption, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel)
        self.model = BSEuler1D(Gen, spot, rate, vol)


class EuropeanBasketCall(EuropeanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, eps = 0, ConfidenceLevel = 0):
        super(EuropeanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, eps, ConfidenceLevel)
        self.f = lambda s: max(np.dot(alpha.T, s)[0, 0] - strike, 0)
        self.f_PCV = lambda s:  self.f(s) - max(np.exp(np.dot(alpha.T, np.log(s))[0, 0]) - strike, 0)



class EuropeanSingleNameCall(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, eps = 0, ConfidenceLevel = 0):
        super(EuropeanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel)
        self.f = lambda s: max(s - strike, 0)



class EuropeanBasketPut(EuropeanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, eps = 0, ConfidenceLevel = 0):
        super(EuropeanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, eps, ConfidenceLevel)
        self.f = lambda s: max(strike - np.dot(alpha.T, s)[0, 0] , 0)


class EuropeanSingleNamePut(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, eps = 0, ConfidenceLevel = 0):
        super(EuropeanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel)
        self.f = lambda s: max(strike - s, 0)

