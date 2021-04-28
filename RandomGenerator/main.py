from LinearCongruential import *
from BoxMuller import *

nbSim = 10**5
tol = 10**-4

print("Linear Congruential:")
Multiplier, Increment, Modulus, Seed = 17, 43, 100, 27
print("-"*80)
print("Seed = {}".format(Seed))
print("Multiplier = {}".format(Multiplier))
print("Increment = {}".format(Increment))
print("Modulus = {}".format(Modulus))
print("-"*80)
r = LinearCongruential(Multiplier, Increment, Modulus, Seed)
#print("The mean of {} simulations is equal to {}".format(nbSim, r.Mean(nbSim)))
#print("The mean of {} simulations with a {} tolerance level is equal to 0.5: {}".format(nbSim, tol, r.TestMean(nbSim, tol)))
print("#"*80)

norm_1 = BoxMuller()
print(norm_1.Generate())