from PseudoGenerator import *
from LinearCongruential import *

class EcuyerCombined(PseudoGenerator):

    def __init__(self, Seed1, Multiplier_1, Increment_1, Modulus_1,
                Seed2, Multiplier_2, Increment_2, Modulus_2, m1):
        
        PseudoGenerator.__init__(self,0,0)
        self.FirstLinear = LinearCongruential(Seed1, Multiplier_1, Increment_1, Modulus_1)
        self.SecondLinear = LinearCongruential(Seed2, Multiplier_2, Increment_2, Modulus_2)
        self.x1 = self.FirstLinear.Generate()
        self.x2 = self.SecondLinear.Generate()
        self.m1 = m1

    def Generate(self):
        unif1 = self.x1
        unif2 = self.x2

        X = (unif1 - unif2) % (self.m1 - 1)
        
        if X > 0:
            result =  X/self.m1
        else:
            result = (self.m1 - 1)/self.m1
            
        self.Current = result
        self.FirstLinear.Generate()
        self.SecondLinear.Generate()
        self.x1 = self.FirstLinear.GetCurrent()
        self.x2 = self.SecondLinear.GetCurrent()

        return result

