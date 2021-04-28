from abc import abstractmethod

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
