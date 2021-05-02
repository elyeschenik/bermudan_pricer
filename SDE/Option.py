from abc import abstractmethod
import numpy as np
from scipy.stats import norm
from BSEuler1D import *
from BSEulerND import *
from BSMilstein1D import *


class Option:
    def __init__(self, spot, strike, rate, vol, maturity, Gen, eps, ConfidenceLevel, antithetic):
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.vol = vol
        self.maturity = maturity

        self.Gen = Gen

        #Pseudo Control Variate method variables
        self.eps = eps
        self.ConfidenceLevel = ConfidenceLevel
        self.Variance = 0
        self.VariancePCV = 0
        self.MinSim = 0
        self.MinSimPCV = 0

        self.antithetic = antithetic

    @abstractmethod
    def ComputePrice(self):
        pass



    def BSClosedForm(self, S_0, K, r, sigma, T, isCall):
        d1 = (np.log(S_0/K) + (r + 0.5 * sigma**2)*T)/(sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if isCall:
            return S_0 * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
        else:
            return -S_0 * norm.cdf(-d1) + np.exp(-r * T) * K * norm.cdf(-d2)

    def VarReductionInfo(self, price):
        print("Thanks to the use of Pseudo Control Variate, the variance of the simulated paths payoffs went from {:.2f} to {:.2f}".format(self.Variance, self.VariancePCV))
        print("The minimum number of simulations for the computed "
              "price to be in the interval "
              "TRUE PRICE +/- {} with {}% confidence level went from {} to {} ".format(self.eps, self.ConfidenceLevel * 100,
                                                                            self.MinSim, self.MinSimPCV))
