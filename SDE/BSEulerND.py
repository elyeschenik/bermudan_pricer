from BlackScholesND import  *


class BSEulerND(BlackScholesND):

    def __init__(self, Gen, spot, rate, var_covar, dim):
        super(BSEulerND, self).__init__(Gen, spot, rate, var_covar, dim)


        if np.all(np.linalg.eigvals(var_covar) > 0): #check if var-covar matrix is positive definite
            self.B = np.linalg.cholesky(var_covar)
        else:                                        #if not, we diagonalize the matrix
            decomposition = np.linalg.eig(var_covar)
            D, O = np.diag(decomposition[0]), decomposition[1]
            self.B = np.dot(O, np.sqrt(D))

    def Simulate(self, StartTime, EndTime, NbSteps):
        Path = SinglePath(StartTime, EndTime, NbSteps)
        Path.AddValue(self.spot)
        dt = Path.timeStep
        lastInserted = self.spot
        for j in range(NbSteps):
            W = self.Gen.GenerateVector(self.dim)
            nextValue = lastInserted + lastInserted * (self.rate * dt + np.dot(self.B, W) * np.sqrt(dt))
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
            W1 = self.Gen.GenerateVector(self.dim)
            W2 = - W1
            nextValue1 = lastInserted1 + lastInserted1 * (self.rate * dt + np.dot(self.B, W1) * np.sqrt(dt))
            nextValue2 = lastInserted2 + lastInserted2 * (self.rate * dt + np.dot(self.B, W2) * np.sqrt(dt))
            Path1.AddValue(nextValue1)
            Path2.AddValue(nextValue2)
            lastInserted1, lastInserted2 = nextValue1, nextValue2
        self.Paths.append(Path1)
        self.Paths.append(Path2)
