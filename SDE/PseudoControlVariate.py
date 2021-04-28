from VarianceReduction import *

class PseudoControlVariate(VarianceReduction):

    def __init__(self):
        super(PseudoControlVariate, self).__init__()

    def Simulate(self, StartTime, EndTime, NbSteps):
        Path = SinglePath(StartTime, EndTime, NbSteps)
        Path.AddValue(self.spot)
        dt = Path.timeStep
        lastInserted = self.spot
        for i in range(Path.NbSteps):
            nextValue = lastInserted + lastInserted * (self.rate * dt + self.vol * self.Gen.Generate() * np.sqrt(dt))
            Path.AddValue(nextValue)
            lastInserted = nextValue
        self.Paths.append(Path)

    @abstractmethod
    def Generate(self):
        pass


