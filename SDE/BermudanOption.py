from Option import *

from Laguerre import *

class BermudanOption(Option):
    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel, antithetic):
        super(BermudanOption, self).__init__(spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel, antithetic)
        if max(exercise_dates) > maturity:
            raise Exception("Please input valid exercise dates that do not exceed the maturity of the contract")
        self.exercise_dates = exercise_dates
        self.L = L #number of basis functions to use
        self.basis = Laguerre() #basis function to use

    def FindStoppingTime(self, StartTime, NbSteps, NbSim):
        """ Algorithm to build the matrix of stopping times for each price simulation at each exercice date"""
        if self.antithetic:
            self.model.SimulateMultiplePathsAntithetic(StartTime, self.maturity, NbSim)
            NbSim = len(self.model.Paths)
        else:
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
                    self.model.GetPath(j).GetValue(Tau[j, k + 1]))
                for I in range(self.L):
                    P[j, I] = self.computeP(self.model.GetPath(j).GetValue(t_k), I)

            A[:, k] = np.linalg.lstsq(P, B)[0][:, 0]

            for j in range(NbSim):
                if self.f(self.model.GetPath(j).GetValue(t_k)) >= np.dot(P[j, :], A[:, k]):
                    Tau[j, k] = t_k
                else:
                    Tau[j, k] = Tau[j, k + 1]
        return Tau

    def ComputePrice(self, StartTime, NbSteps, NbSim):
        """ Compute the price of the option """
        Tau = self.FindStoppingTime(StartTime, NbSteps, NbSim)
        NbSim = len(self.model.Paths)
        price = np.mean([np.exp(-self.rate * Tau[j, 0]) * self.f(self.model.GetPath(j).GetValue(Tau[j, 0])) for j in
                             range(NbSim)])
        self.Variance = self.model.GetVariance(self.f, Tau[:,0].mean())
        self.MinSim = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f, Tau[:,0].mean())
        return price

    def ComputePricePCV(self, StartTime, NbSteps, NbSim):
        """ Compute the price using Pseudo control variate to reduce variance """
        Tau = self.FindStoppingTime(StartTime, NbSteps, NbSim)
        NbSim = len(self.model.Paths)
        basket_var = np.dot(self.alpha.T, np.dot(self.vol, self.alpha))[0, 0]
        sigma_squared = (self.model.B ** 2)

        S_0 = np.prod([self.spot[i, 0] ** self.alpha[i, 0] for i in range(self.dim)])
        K = self.strike
        r = self.rate - 0.5 * np.dot(self.alpha.T, sigma_squared.sum(axis=1))[0] + 0.5 * basket_var
        sigma = np.sqrt(basket_var)
        T = Tau[:,0].mean()

        ExpectationY = self.BSClosedForm(S_0, K, r, sigma, T, True)

        price = np.mean([np.exp(-self.rate * Tau[j, 0]) * self.f_PCV(self.model.GetPath(j).GetValue(Tau[j, 0])) for j in
                     range(NbSim)]) + ExpectationY

        self.Variance = self.model.GetVariance(self.f, Tau[:,0].mean())
        self.VariancePCV = self.model.GetVariance(self.f_PCV, Tau[:,0].mean())
        self.MinSim = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f, Tau[:,0].mean())
        self.MinSimPCV = self.model.GetIterationNumber(self.eps, self.ConfidenceLevel, self.f_PCV, Tau[:,0].mean())

        self.VarReductionInfo(price)

        return price

class BermudanBasketOption(BermudanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, dim, alpha, exercise_dates, L, eps, ConfidenceLevel, antithetic):
        super(BermudanBasketOption, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        try:
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
        except:
            raise Exception("Please make sure that the spot, var-covar and alpha are numpy arrays")

        self.dim = dim
        self.alpha = alpha
        self.model = BSEulerND(Gen, spot, rate, vol, dim)

    def computeP(self, s, I):
        return self.basis.compute(np.dot(self.alpha.T, s)[0, 0], I)







class BermudanSingleNameOption(BermudanOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps, ConfidenceLevel, antithetic):
        super(BermudanSingleNameOption, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        if model == "euler":
            self.model = BSEuler1D(Gen, spot, rate, vol)
        elif model == "milstein":
            self.model = BSMilstein1D(Gen, spot, rate, vol)
        else:
            raise Exception("Wrong model name, please input either 'euler' or 'milstein'")

    def computeP(self, s, I):
        return self.basis.compute(s, I)



class BermudanBasketCall(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, dim, alpha, exercise_dates, L, eps = 0, ConfidenceLevel = 0, antithetic = False):
        super(BermudanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, model, dim, alpha, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        self.f = lambda s: max(np.dot(alpha.T, s)[0, 0] - strike, 0)
        self.f_PCV = lambda s: self.f(s) - max(np.exp(np.dot(alpha.T, np.log(s))[0, 0]) - strike, 0)





class BermudanSingleNameCall(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps = 0, ConfidenceLevel = 0, antithetic = False):
        super(BermudanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        self.f = lambda s: max(s - strike, 0)


class BermudanBasketPut(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, dim, alpha, exercise_dates, L, eps = 0, ConfidenceLevel = 0, antithetic = False):
        super(BermudanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, model, dim, alpha, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        self.f = lambda s: max(strike - np.dot(alpha.T, s)[0, 0], 0)


class BermudanSingleNamePut(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps = 0, ConfidenceLevel = 0, antithetic = False):
        super(BermudanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        self.f = lambda s: max(strike - s, 0)

