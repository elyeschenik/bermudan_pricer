from ContinuousGenerator import *

class NormalGenerator(ContinuousGenerator):

    def __init__(self):
        super(NormalGenerator, self).__init__(0, 1)

    def GetCurrent(self):
        return self.Current

    @abstractmethod
    def Generate(self):
        pass


