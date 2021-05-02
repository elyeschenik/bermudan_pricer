from NormalGenerator import *
from LinearCongruential import *
from EcuyerCombined import *
from VanDerCorput import *

class CentralLimit(NormalGenerator):

    def __init__(self, gen = 'lc'):
        super(CentralLimit, self).__init__(0)
        
        if type(gen) != str:
            raise TypeError
    
        if gen == 'lc':
            self.gen = LinearCongruential(27637, 40014, 0, 2147483563)
        elif gen == 'ec':
            self.gen = EcuyerCombined(27637, 40014, 0, 2147483563, 172635, 40692, 0, 2147483399, 2147483563)
        elif gen == 'vdc':
            self.gen = VanDerCorput(100,12)
        elif gen == 'dl':
            self.gen = DeLuca(1000)
        else:
            raise ValueError

    def Generate(self):
        sum_u = sum([self.gen.Generate() for i in range(12)])
        self.Current = sum_u - 6

        return self.Current