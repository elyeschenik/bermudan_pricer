from PseudoGenerator import *

class LinearCongruential(PseudoGenerator):

    def __init__(self, Seed, Multiplier, Increment, Modulus):
        super(LinearCongruential, self).__init__(Seed, Seed)
        self.Multiplier = Multiplier
        self.Increment = Increment
        self.Modulus = Modulus
    
    def Generate(self):
        
        self.Current = (self.Multiplier * self.Current + self.Increment) % self.Modulus
        result = self.Current / self.Modulus

        return result
    
    def GetCurrent(self):
        return self.Current
