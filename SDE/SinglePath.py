from abc import abstractmethod

class SinglePath:

    def __init__(self, StartTime, EndTime, NbSteps):
        super(SinglePath, self).__init__()
        self.Values = []
        self.Times = []
        self.StartTime = StartTime
        self.EndTime = EndTime
        if NbSteps%1 != 0 or NbSteps<0:
            raise Exception("Wrong NbSteps value")
        self.NbSteps = NbSteps
        self.timeStep = (self.EndTime - self.StartTime)/self.NbSteps

    def AddValue(self, val):
        self.Values.append(val)
        if len(self.Times) == 0:
            self.Times.append(self.StartTime)
        else:
            self.Times.append(self.Times[-1] + self.timeStep)

    def GetValue(self, time):
        if time < self.StartTime:
            #print("Value on initial time")
            return self.Values[0]
        if time > self.EndTime:
            #print("Value on terminal time")
            return self.Values[-1]

        if time in self.Times:
            idx = self.Times.index(time)
            return self.Values[idx]
        else:
            for t in range(len(self.Times) - 1):
                if self.Times[t] < time < self.Times[t+1]:
                    time - self.Times[t]
                    return ((self.Values[t+1] - self.Values[t])/self.timeStep) * (time - self.Times[t]) + self.Values[t]
