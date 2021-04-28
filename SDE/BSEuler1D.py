from BlackScholes1D import  *

class BSEuler1D(BlackScholes1D):

    def __init__(self, Gen, spot, rate, vol):
        super(BSEuler1D, self).__init__(Gen, spot, rate, vol)

    def Simulate(self, StartTime, EndTime, NbSteps):
        Path = SinglePath(StartTime, EndTime, NbSteps)
        Path.AddValue(self.spot)
        dt = Path.timeStep
        lastInserted = self.spot
        for i in range(NbSteps):
            nextValue = lastInserted + lastInserted * (self.rate * dt + self.vol * self.Gen.Generate() * np.sqrt(dt))
            Path.AddValue(nextValue)
            lastInserted = nextValue
        self.Paths.append(Path)
