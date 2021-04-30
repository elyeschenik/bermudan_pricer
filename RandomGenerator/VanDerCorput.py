from QuasiGenerator import *
from Primes import *

class VanDerCorput(QuasiGenerator):

    def __init__(self, n, d):
        super(VanDerCorput, self).__init__(0)
        self.n = n
        self.d = d
        self.primes = Primes().GetNPrimes(d)
        self.i = 0

    def Generate(self):
        
        n_rec = self.n
        k = 0
        p = self.primes[self.i]
        phi = 0
        
        while n_rec != 0:
            ak = n_rec % p
            n_rec = (n_rec - ak) / p
            k += 1
            phi += ak/p**k
        
        if self.i < self.d - 1 :
            self.i += 1
            p = self.primes[self.i]
        else:
            self.i = 0
            self.n += 1
        
        self.Current = phi
        
        return phi


class DeLuca(QuasiGenerator):
    
    def __init__(self, n):
        QuasiGenerator.__init__(self, 0)
        self.n = n
        self.i = 0
        self.nums = np.linspace(0, 1, n)
        np.random.shuffle(self.nums)

    def Generate(self):
        
        result = self.nums[self.i]
        
        while result == 0 or result == 1:
            self.i += 1
            result = self.nums[self.i]
                    
        if self.i < self.n - 1:
            self.i += 1
        else:
            np.random.shuffle(self.nums)
            self.i = 0
        
        return result
      