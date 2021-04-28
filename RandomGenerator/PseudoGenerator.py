from UniformGenerator import *

class PseudoGenerator(UniformGenerator):

    def __init__(self, Seed, Current):
        super(PseudoGenerator, self).__init__()
        self.Seed = Seed
        self.Current = Current

    def GetCurrent(self):
        return self.Current

    @abstractmethod
    def Generate(self):
        pass


