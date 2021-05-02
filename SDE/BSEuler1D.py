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
            DeltaW = self.Gen.Generate() * np.sqrt(dt)
            nextValue = lastInserted + lastInserted * (self.rate * dt + self.vol * DeltaW)
            Path.AddValue(nextValue)
            lastInserted = nextValue
        self.Paths.append(Path)


    def SimulateAntithetic(self, StartTime, EndTime, NbSteps):
        Path1 = SinglePath(StartTime, EndTime, NbSteps)
        Path2 = SinglePath(StartTime, EndTime, NbSteps)
        Path1.AddValue(self.spot)
        Path2.AddValue(self.spot)
        dt = Path1.timeStep
        lastInserted1, lastInserted2 = self.spot, self.spot
        for i in range(NbSteps):
            DeltaW_1 = self.Gen.Generate() * np.sqrt(dt)
            DeltaW_2 = - DeltaW_1
            nextValue1 = lastInserted1 + lastInserted1 * (self.rate * dt + self.vol * DeltaW_1)
            nextValue2 = lastInserted2 + lastInserted2 * (self.rate * dt + self.vol * DeltaW_2)
            Path1.AddValue(nextValue1)
            Path2.AddValue(nextValue2)
            lastInserted1, lastInserted2 = nextValue1, nextValue2
        self.Paths.append(Path1)
        self.Paths.append(Path2)
