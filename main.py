import sys
sys.path.insert(0, './RandomGenerator')
sys.path.insert(1, './SDE')

from SinglePath import *
from BSEuler1D import *
from EuropeanOption import *
from BermudanOption import *

from BoxMuller import *
from CentralLimit import *

import warnings

warnings.filterwarnings("ignore")
####### Testing options ###########

#Option type variables
Eur_Berm = "Bermudan" #'European' for European option or 'Bermudan' for Bermudan
SN_Basket = "Basket" #'SN' for single name option or 'Basket' for basket option
Call_Put = "Call" #'Call' for call option and 'Put' for put option

#Common parameters (some in the single name option type only)

uniform_method = 'lc'  #'lc', 'ec', 'vdc' or 'dl'. To use quasi random simulations, use 'dl' or 'vdc'
Gen = BoxMuller(uniform_method) #BoxMuller or CentralLimit

spot = 100
vol = 0
rate = 0.01
strike = 100
maturity = 1
#model to simulate the evolutioon of the asset prices
model = "euler" #"euler" or "milstein"

#Parameters in the multi-asset case
spots = np.array([[100],[100]])
var_covar = np.array([[0.09,.05],[0.05, 0.09]])
dim = 2
alpha = np.array([[0.3],[0.7]]) #weights matrix

#Parameters to use for the Bermudan options
exercise_dates = [0.25, 0.5, 0.75, 1]
L = 10  #number of basis functions of L2(R)

#Parameters for the time frame of the option
StartTime = 0
EndTime = maturity
NbSteps = 252 * maturity
NbSim = 500

#Variance reduction variables when using pseudo control variate
usePCV = False
eps = 0.2 #precision of the confidence interval
ConfidenceLevel = 5/100 #confidence level of the confidence interval

#Possibility to simulate the price paths using antithetic variables thus reducing Variance
antithetic = False #can be True or False

def get_my_option(Eur_Berm, SN_Basket, Call_Put):
    if Eur_Berm == "European":
        if SN_Basket == "SN":
            if Call_Put == "Call":
                myOption = EuropeanSingleNameCall(spot, strike, rate, vol, maturity, Gen, model, eps, ConfidenceLevel, antithetic)
            elif Call_Put == "Put":
                myOption = EuropeanSingleNamePut(spot, strike, rate, vol, maturity, Gen, model, eps, ConfidenceLevel, antithetic)
        elif SN_Basket == "Basket":
            if Call_Put == "Call":
                myOption = EuropeanBasketCall(spots, strike, rate, var_covar, maturity, Gen, model, dim, alpha, eps, ConfidenceLevel, antithetic)
            elif Call_Put == "Put":
                myOption = EuropeanBasketPut(spots, strike, rate, var_covar, maturity, Gen, model, dim, alpha, eps, ConfidenceLevel, antithetic)
    elif Eur_Berm == "Bermudan":
        if SN_Basket == "SN":
            if Call_Put == "Call":
                myOption = BermudanSingleNameCall(spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps, ConfidenceLevel, antithetic)
            elif Call_Put == "Put":
                myOption = BermudanSingleNamePut(spot, strike, rate, vol, maturity, Gen, model, exercise_dates, L, eps, ConfidenceLevel, antithetic)
        elif SN_Basket == "Basket":
            if Call_Put == "Call":
                myOption = BermudanBasketCall(spots, strike, rate, var_covar, maturity, Gen, model, dim, alpha, exercise_dates, L, eps, ConfidenceLevel, antithetic)
            elif Call_Put == "Put":
                myOption = BermudanBasketPut(spots, strike, rate, var_covar, maturity, Gen, model, dim, alpha, exercise_dates, L, eps, ConfidenceLevel, antithetic)

    return myOption

print("######################################### Variance Reduction #########################################")
myOption = get_my_option(Eur_Berm, SN_Basket, Call_Put)
print("Using Quasi Montecarlo: {}".format(uniform_method in ['vdc', 'dl']))
print("Using antithetic variables for price simulation: {}".format(antithetic))
print("Using Pseudo Control Variate: {}".format(usePCV))
print("############################################### Pricing ###############################################")
if usePCV:
    if SN_Basket != "Basket" or Call_Put != "Call":
        raise Exception("Pseudo control variate not implemented for {} {} {} options".format(Eur_Berm, SN_Basket, Call_Put))
    else:
        price = myOption.ComputePricePCV(StartTime, NbSteps, NbSim)
        print("{} {} {} option price: {:.2f}".format(Eur_Berm, SN_Basket, Call_Put, price))
        print("{} {} {} variance: {:.2f}".format(Eur_Berm, SN_Basket, Call_Put, myOption.VariancePCV))
        print("{} {} {} minimum number of simulation to be in the "
              "interval TRUE PRICE +/-{} with {}% confidence level: {}".format(Eur_Berm, SN_Basket, Call_Put, eps,
                                                                                   ConfidenceLevel * 100, myOption.MinSimPCV))
else:
    price = myOption.ComputePrice(StartTime, NbSteps, NbSim)
    print("{} {} {} option price: {:.2f}".format(Eur_Berm, SN_Basket, Call_Put, price))
    print("{} {} {} variance: {:.2f}".format(Eur_Berm, SN_Basket, Call_Put,myOption.Variance))
    print("{} {} {} minimum number of simulation to be in the "
          "interval TRUE PRICE +/-{} with {}% confidence level: {}".format(Eur_Berm, SN_Basket, Call_Put, eps, ConfidenceLevel * 100, myOption.MinSim))
print("################################################# End #################################################")