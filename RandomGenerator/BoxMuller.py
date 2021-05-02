from NormalGenerator import *
from LinearCongruential import *
from EcuyerCombined import *
from VanDerCorput import *

class BoxMuller(NormalGenerator):

    def __init__(self, gen = 'lc'):
        super(BoxMuller, self).__init__(0)
        
        if type(gen) != str : raise TypeError
    
        if gen == 'lc':
            self.gen = LinearCongruential(27637, 40014, 0, 2147483563)
        elif gen == 'ec':
            self.gen = EcuyerCombined(27637, 40014, 0, 2147483563, 172635, 40692, 0, 2147483399, 2147483563)
        elif gen == 'vdc':
            self.gen = VanDerCorput(100,12)
        elif gen == 'dl':
            self.gen = DeLuca(10000)
        else:
            raise ValueError

        self.requirenewsim = True

        self.X = 0
        self.Y = 0


    def Generate(self):

        if self.requirenewsim:
            
            unif1 = self.gen.Generate()
            unif2 = self.gen.Generate()

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





