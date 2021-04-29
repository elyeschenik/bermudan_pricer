from abc import abstractmethod
import numpy as np
from scipy.stats import norm

class Option:
    def __init__(self, spot, strike, rate, vol, maturity, Gen):
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.vol = vol
        self.maturity = maturity

        self.Gen = Gen

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
