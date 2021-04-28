
class Laguerre:
    def __init__(self):
        pass

    def compute(self, x ,I):
        if I == 0:
            return 1
        elif I == 1:
            return 1 - x
        else:
            return ((2 * I + 1 - x) * self.compute(x, I - 1) - I * self.compute(x, I - 2))/(I + 1)



