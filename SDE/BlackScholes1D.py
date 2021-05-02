from RandomProcess import  *
import numpy as np

class BlackScholes1D(RandomProcess):

    def __init__(self, Gen, spot, rate, vol):
        super(BlackScholes1D, self).__init__(Gen)
        self.spot = spot
        self.rate = rate
        self.vol = vol

    @abstractmethod
    def Simulate(self, StartTime, EndTime, NbSteps):
        pass

    def SimulateAntithetic(self, StartTime, EndTime):
        Path1 = SinglePath(StartTime, EndTime, 1)
        Path2 = SinglePath(StartTime, EndTime, 1)
        Path1.AddValue(self.spot)
        Path2.AddValue(self.spot)
        dt = Path1.timeStep
        lastInserted = self.spot

        DeltaW_1 = self.Gen.Generate() * np.sqrt(dt)
        DeltaW_2 = - DeltaW_1
        nextValue1 = lastInserted * np.exp((self.rate - 0.5 * self.vol**2) * dt + self.vol * DeltaW_1)
        nextValue2 = lastInserted * np.exp((self.rate - 0.5 * self.vol**2) * dt + self.vol * DeltaW_2)
        Path1.AddValue(nextValue1)
        Path2.AddValue(nextValue2)