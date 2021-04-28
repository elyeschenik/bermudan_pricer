from PseudoGenerator import *
from LinearCongruential import *

class EcuyerCombined(PseudoGenerator):

    def __init__(self, Seed1, Seed2):
        super(EcuyerCombined, self).__init__(0, 0)
        self.FirstLinear = LinearCongruential(400014, 0, 2014704830563, Seed1)
        self.SecondLinear = LinearCongruential(400692, 0, 2014704830399, Seed2)
        self.x1 = self.FirstLinear.GetCurrent()
        self.x2 = self.SecondLinear.GetCurrent()
        self.m1 = 2014704830563

    def Generate(self):
        unif1 = self.x1
        unif2 = self.x2

        R = (unif1 - unif2) % (self.m1 - 1)
        result =  R/self.m1 * (R > 0) + R/(self.m1 + 1) * (R < 0) ((self.m1 - 1)/self.m1) * (R == 0)

        self.FirstLinear.Generate()
        self.SecondLinear.Generate()
        self.x1 = self.FirstLinear.GetCurrent()
        self.x2 = self.SecondLinear.GetCurrent()

        return result

