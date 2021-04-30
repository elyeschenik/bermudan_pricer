class LowerThanTwo(Exception):
    pass

class Primes:
    
    def __init__(self):
        pass
    
    def IsPrime(self, num):
        try:
            num = int(num)
            if num < 2: raise LowerThanTwo()
        except ValueError:
            return False, "Input a valid number"
        except LowerThanTwo:
            return False, "Input a number greater or equal than 2"
        else:
            if num > 2 and num % 2 == 0:
                return False
            for x in range(2, num // 2):
                if num % x == 0:
                    return False
        return True
    
    def GetNPrimes(self, d):
        
        nb_p = 1
        primes = []
        primes.append(2)
        num_test = 3
        
        
        while nb_p < d:
            
            if self.IsPrime(num_test):
                primes.append(num_test)
                num_test += 1
                nb_p += 1
            else:
                num_test += 1
                
        return primes
