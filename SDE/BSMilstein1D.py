from BlackScholes1D import  *

class BSMilstein1D(BlackScholes1D):

    def __init__(self, Gen, spot, rate, vol):
        super(BSMilstein1D, self).__init__(Gen, spot, rate, vol)

    def Simulate(self, StartTime, EndTime, NbSteps):
        Path = SinglePath(StartTime, EndTime, NbSteps)
        Path.AddValue(self.spot)
        dt = Path.timeStep
        lastInserted = self.spot
        for i in range(NbSteps):

            DeltaB = self.Gen.Generate() * np.sqrt(dt)
            nextValue = lastInserted + lastInserted * ((self.rate - 0.5 * self.vol**2) * dt
                                                       + self.vol * (1 + 0.5 * self.vol * DeltaB) * DeltaB)
            Path.AddValue(nextValue)
            lastInserted = nextValue
        self.Paths.append(Path)
