from Option import *
from BSEuler1D import *
from BSEulerND import *
from Laguerre import *

class BermudanOption(Option):
    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel):
        super(BermudanOption, self).__init__(spot, strike, rate, vol, maturity, Gen)
        if max(exercise_dates) > maturity:
            raise Exception("Please input valid exercise dates that do not exceed the maturity of the contract")
        self.exercise_dates = exercise_dates
        self.L = L
        self.basis = Laguerre()

        # PCV Variance reduction
        self.eps = eps
        self.ConfidenceLevel = ConfidenceLevel
        self.Variance = 0
        self.VariancePCV = 0
        self.MinSim = 0
        self.MinSimPCV = 0

    @abstractmethod
    def FindStoppingTime(self):
        pass

    def ComputePrice(self, StartTime, NbSteps, NbSim):
        Tau = self.FindStoppingTime(StartTime, NbSteps, NbSim)
        price = sum([np.exp(-self.rate * Tau[j, 0]) * self.f(self.model.Paths[j].GetValue(Tau[j,0])) for j in
                     range(NbSim)]) / NbSim
        return price

    def ComputePricePCV(self, StartTime, NbSteps, NbSim):
        Tau = self.FindStoppingTime(StartTime, NbSteps, NbSim)
        basket_var = np.dot(self.alpha.T, np.dot(self.vol, self.alpha))[0, 0]
        sigma_squared = (self.model.B ** 2)

        S_0 = np.prod([self.spot[i, 0] ** self.alpha[i, 0] for i in range(self.dim)])
        K = self.strike
        r = self.rate - 0.5 * np.dot(self.alpha.T, sigma_squared.sum(axis=1))[0] + 0.5 * basket_var
        sigma = np.sqrt(basket_var)
        T = sum([Tau[j,0] for j in range(NbSim)]) / NbSim

        ExpectationY = self.BSClosedForm(S_0, K, r, sigma, T, True)

        price = sum([np.exp(-self.rate * Tau[j, 0]) * self.f_PCV(self.model.Paths[j].GetValue(Tau[j, 0])) for j in
                     range(NbSim)]) / NbSim + ExpectationY

        self.Variance = self.model.GetVariance(self.f, self.maturity)
        self.VariancePCV = self.model.GetVariance(self.f_PCV, self.maturity)
        self.MinSim = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f, self.maturity)
        self.MinSimPCV = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f_PCV, self.maturity)

        self.VarReductionInfo(price)

        return price

class BermudanBasketOption(BermudanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L, eps, ConfidenceLevel):
        super(BermudanBasketOption, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel)
        if dim <= 1 or dim%1 != 0:
            raise Exception("Please input an integer dimension with values >= 2. If dim=1, use a single name class instead")
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




    def FindStoppingTime(self,StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)
        n = len(self.exercise_dates)

        Tau = np.zeros((NbSim, n))
        Tau[:, n - 1] = self.maturity

        A = np.zeros((self.L, n - 1))

        for k in range(n - 2, -1, -1):
            t_k = self.exercise_dates[k]

            P = np.zeros((NbSim, self.L))
            B = np.zeros((NbSim, 1))

            for j in range(NbSim):
                B[j, 0] = np.exp(-self.rate * (Tau[j, k + 1] - t_k)) * self.f(
                    self.model.Paths[j].GetValue(Tau[j, k + 1]))
                for I in range(self.L):
                    P[j, I] = self.basis.compute(np.dot(self.alpha.T, self.model.Paths[j].GetValue(t_k))[0, 0], I)

            A[:, k] = np.linalg.lstsq(P, B)[0][:, 0]

            for j in range(NbSim):
                if self.f(self.model.Paths[j].GetValue(t_k)) >= np.dot(P[j, :], A[:, k]):
                    Tau[j, k] = t_k
                else:
                    Tau[j, k] = Tau[j, k + 1]
        return Tau




class BermudanSingleNameOption(BermudanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel):
        super(BermudanSingleNameOption, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel)
        self.model = BSEuler1D(Gen, spot, rate, vol)

    def FindStoppingTime(self, StartTime, NbSteps, NbSim):
        self.model.SimulateMultiplePaths(StartTime, self.maturity, NbSteps, NbSim)
        n = len(self.exercise_dates)

        Tau = np.zeros((NbSim, n))
        Tau[:, n - 1] = self.maturity

        A = np.zeros((self.L, n - 1))

        for k in range(n - 2, -1, -1):
            t_k = self.exercise_dates[k]

            P = np.zeros((NbSim, self.L))
            B = np.zeros((NbSim, 1))

            for j in range(NbSim):
                B[j, 0] = np.exp(-self.rate * (Tau[j, k + 1] - t_k)) * self.f(
                    self.model.Paths[j].GetValue(Tau[j, k + 1]))
                for I in range(self.L):
                    P[j, I] = self.basis.compute(self.model.Paths[j].GetValue(t_k), I)

            A[:, k] = np.linalg.lstsq(P, B)[0][:, 0]

            for j in range(NbSim):
                if self.f(self.model.Paths[j].GetValue(t_k)) >= np.dot(P[j, :], A[:, k]):
                    Tau[j, k] = t_k
                else:
                    Tau[j, k] = Tau[j, k + 1]
        return Tau


class BermudanBasketCall(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L, eps = 0, ConfidenceLevel = 0):
        super(BermudanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L, eps, ConfidenceLevel)
        self.f = lambda s: max(np.dot(alpha.T, s)[0, 0] - strike, 0)
        self.f_PCV = lambda s: self.f(s) - max(np.exp(np.dot(alpha.T, np.log(s))[0, 0]) - strike, 0)


class BermudanSingleNameCall(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps = 0, ConfidenceLevel = 0):
        super(BermudanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel)
        self.f = lambda s: max(s - strike, 0)


class BermudanBasketPut(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L, eps = 0, ConfidenceLevel = 0):
        super(BermudanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L, eps, ConfidenceLevel)
        self.f = lambda s: max(strike - np.dot(alpha.T, s)[0, 0], 0)


class BermudanSingleNamePut(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps = 0, ConfidenceLevel = 0):
        super(BermudanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel)
        self.f = lambda s: max(strike - s, 0)

