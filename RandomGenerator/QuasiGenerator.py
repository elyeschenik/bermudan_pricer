from UniformGenerator import *

class QuasiGenerator(UniformGenerator):

    def __init__(self, Current):
        super(QuasiGenerator, self).__init__()
        self.Current = Current

    def GetCurrent(self):
        return self.Current

    @abstractmethod
    def Generate(self):
        pass
