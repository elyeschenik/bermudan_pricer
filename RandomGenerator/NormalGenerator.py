from ContinuousGenerator import *

class NormalGenerator(ContinuousGenerator):

    def __init__(self, Current):
        super(NormalGenerator, self).__init__(0, 1)
        self.Current = Current

    def GetCurrent(self):
        return self.Current

    @abstractmethod
    def Generate(self):
        pass
    



