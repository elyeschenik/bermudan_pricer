from SinglePath import *
from BSEuler1D import *
from EuropeanOption import *
from BermudanOption import *

from BoxMuller import *

import warnings

warnings.filterwarnings("ignore")
####### Testing options ###########

#common params
Gen = BoxMuller()

spot = 100
vol = 0.3
rate = 0.01
strike = 100
maturity = 1

#basket case
spots = np.array([[100],[100]])
var_covar = np.array([[0.09,0.09],[0.09, 0.09]])
dim = 2
alpha = np.array([[0.3],[0.7]])

#Bermudan case
exercise_dates = [0.25, 0.5, 0.75, 1]
L = 5


#time frame
StartTime = 0
EndTime = maturity
NbSteps = 100
NbSim = 1000


Call = EuropeanSingleNameCall(spot, strike, rate, vol, maturity, Gen)
print("Single name call price: {}".format(Call.ComputePrice(StartTime, NbSteps, NbSim)))

BasketCall = EuropeanBasketCall(spots, strike, rate, var_covar, maturity, Gen, dim, alpha)
print("Basket call price: {}".format(BasketCall.ComputePrice(StartTime, NbSteps, NbSim)))

Put = EuropeanSingleNamePut(spot, strike, rate, vol, maturity, Gen)
print("Single name put price: {}".format(Put.ComputePrice(StartTime, NbSteps, NbSim)))

BasketPut = EuropeanBasketPut(spots, strike, rate, var_covar, maturity, Gen, dim, alpha)
print("Basket put price: {}".format(BasketPut.ComputePrice(StartTime, NbSteps, NbSim)))

BermudanCall = BermudanSingleNameCall(spot, strike, rate, vol, maturity, Gen, exercise_dates, L)
print("Bermudan single name call price: {}".format(BermudanCall.ComputePrice(StartTime, NbSteps, NbSim)))

BBasketCall = BermudanBasketCall(spots, strike, rate, var_covar, maturity, Gen, dim, alpha, exercise_dates, L)
print("Bermudan Basket call price: {}".format(BBasketCall.ComputePrice(StartTime, NbSteps, NbSim)))

BermudanPut = BermudanSingleNamePut(spot, strike, rate, vol, maturity, Gen, exercise_dates, L)
print("Bermudan single name put price: {}".format(BermudanPut.ComputePrice(StartTime, NbSteps, NbSim)))

BBasketPut = BermudanBasketPut(spots, strike, rate, var_covar, maturity, Gen, dim, alpha, exercise_dates, L)
print("Bermudan Basket put price: {}".format(BBasketPut.ComputePrice(StartTime, NbSteps, NbSim)))

