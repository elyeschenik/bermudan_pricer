from PseudoGenerator import *

class LinearCongruential(PseudoGenerator):

    def __init__(self, Multiplier, Increment, Modulus, Seed):
        super(LinearCongruential, self).__init__(Seed, Seed)
        self.Multiplier = Multiplier
        self.Increment = Increment
        self.Modulus = Modulus


    def Generate(self):
        result = self.Current / self.Modulus
        self.Current = (self.Multiplier * self.Current + self.Increment) % self.Modulus
        return result

