from BlackScholesND import  *


class BSMilstein(BlackScholesND):

    def __init__(self, Gen, spot, rate, var_covar, dim):
        super(BSMilstein, self).__init__(Gen, spot, rate, var_covar, dim)


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