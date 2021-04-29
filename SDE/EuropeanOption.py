from Option import *
from BSEuler1D import *
from BSEulerND import *

class EuropeanBasketOption(Option):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, VarianceReduction):
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
        self.VarianceReduction = VarianceReduction

    def ComputePrice(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)

        if self.VarianceReduction:
            basket_var = np.dot(self.alpha.T,np.dot(self.vol, self.alpha))[0,0]
            sigma_squared = (self.model.B ** 2)

            S_0 = np.prod([self.spot[i,0]**self.alpha[i,0] for i in range(self.dim)])
            K = self.strike
            r = self.rate - 0.5 * np.dot(self.alpha.T, sigma_squared.sum(axis = 1))[0] + 0.5 * basket_var
            sigma = np.sqrt(basket_var)
            T = self.maturity

            E_Y = self.BSClosedForm(S_0, K, r, sigma, T, True)
            price = np.exp(-self.rate * self.maturity) * sum(
                [self.f_PCV(np.dot(self.alpha.T, path.GetValue(self.maturity))[0, 0]) for path in self.model.Paths]) / NbSim + E_Y
        else:
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

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, VarianceReduction = False):
        super(EuropeanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, VarianceReduction)
        self.f = lambda s: max(s - self.strike, 0)
        self.f_PCV = lambda x: np.exp(-rate * maturity) * (
                    max(np.dot(alpha.T, x)[0, 0] - strike, 0) - max(np.exp(np.dot(alpha.T, np.log(x))[0, 0]) - strike, 0))



class EuropeanSingleNameCall(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        super(EuropeanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.f = lambda s: max(s - self.strike, 0)



class EuropeanBasketPut(EuropeanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, VarianceReduction = False):
        super(EuropeanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, VarianceReduction)
        self.f = lambda s: max(self.strike - s, 0)


class EuropeanSingleNamePut(EuropeanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        super(EuropeanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.f = lambda s: max(self.strike - s, 0)

