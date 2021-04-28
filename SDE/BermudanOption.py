from Option import *
from BSEuler1D import *
from BSEulerND import *
from Laguerre import *

class BermudanBasketOption(Option):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L):
        super(BermudanBasketOption, self).__init__(spot, strike, rate, vol, maturity, Gen)
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

        if max(exercise_dates) > maturity:
            raise Exception("Please input valid exercise dates that do not exceed the maturity of the contract")
        self.dim = dim
        self.alpha = alpha
        self.model = BSEulerND(Gen, spot, rate, vol, dim)
        self.exercise_dates = exercise_dates
        self.L = L
        self.basis = Laguerre()

    def ComputePrice(self, StartTime, NbSteps, NbSim):
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
                B[j, 0] = np.exp(-self.rate * (Tau[j, k + 1] - t_k)) * self.f(np.dot(self.alpha.T,
                                                                                     self.model.Paths[j].GetValue(Tau[j, k + 1]))[0, 0])
                for I in range(self.L):
                    P[j, I] = self.basis.compute(np.dot(self.alpha.T, self.model.Paths[j].GetValue(t_k))[0, 0], I)

            A[:, k] = np.linalg.lstsq(P, B)[0][:, 0]

            for j in range(NbSim):
                if self.f(np.dot(self.alpha.T, self.model.Paths[j].GetValue(t_k))[0, 0]) >= np.dot(P[j, :], A[:, k]):
                    Tau[j, k] = t_k
                else:
                    Tau[j, k] = Tau[j, k + 1]

        price = sum([np.exp(-self.rate * Tau[j, 0]) * self.f(np.dot(self.alpha.T, self.model.Paths[j].GetValue(Tau[j,0]))[0, 0]) for j in
                     range(NbSim)]) / NbSim

        return price

class BermudanSingleNameOption(Option):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L):
        super(BermudanSingleNameOption, self).__init__(spot, strike, rate, vol, maturity, Gen)
        self.model = BSEuler1D(Gen, spot, rate, vol)
        self.exercise_dates = exercise_dates
        self.L = L
        self.basis = Laguerre()

    def ComputePrice(self, StartTime, NbSteps, NbSim):
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

        price = sum([np.exp(-self.rate * Tau[j, 0]) * self.f(self.model.Paths[j].GetValue(Tau[j, 0])) for j in
                     range(NbSim)]) / NbSim

        return price


class BermudanBasketCall(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L):
        super(BermudanBasketCall, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L)
        self.f = lambda s: max(s - self.strike, 0)


class BermudanSingleNameCall(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L):
        super(BermudanSingleNameCall, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L)
        self.f = lambda s: max(s - self.strike, 0)


class BermudanBasketPut(BermudanBasketOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L):
        super(BermudanBasketPut, self).__init__(spot, strike, rate, vol, maturity, Gen, dim, alpha, exercise_dates, L)
        self.f = lambda s: max(self.strike - s, 0)


class BermudanSingleNamePut(BermudanSingleNameOption):

    def __init__(self, spot, strike, rate, vol, maturity, Gen, exercise_dates, L):
        super(BermudanSingleNamePut, self).__init__(spot, strike, rate, vol, maturity, Gen, exercise_dates, L)
        self.f = lambda s: max(self.strike - s, 0)

