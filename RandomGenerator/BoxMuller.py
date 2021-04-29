from NormalGenerator import *
from LinearCongruential import *

class BoxMuller(NormalGenerator):

    def __init__(self):
        super(BoxMuller, self).__init__()
        #self.FirstLinear = LinearCongruential(3524, 40014, 4, 2147483563)
        self.FirstLinear = LinearCongruential(2 ** 10, 154224, 4557, 182)
        #self.SecondLinear = LinearCongruential(1263, 40692, 8, 2147483399)
        self.SecondLinear = LinearCongruential(2 ** 9, 137843, 4645, 148)

        self.requirenewsim = True

        self.X = 0
        self.Y = 0


    def Generate_bis(self):

        if self.requirenewsim:
            unif1 = self.FirstLinear.Generate()
            unif2 = self.SecondLinear.Generate()

            R = np.sqrt(-2 * np.log(unif1))
            theta = 2 * np.pi * unif2

            self.X = R * np.cos(theta)
            self.Y = R * np.sin(theta)

            result = self.X
            self.requirenewsim = False

        else:
            result = self.Y
            self.requirenewsim = True

        return result

    def Generate(self):
        return np.random.normal()




