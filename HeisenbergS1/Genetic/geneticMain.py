import testmod
import numpy as np
import math
import os
import Individual
import Population


CLUSTER = False  #True,False
#setting global seed
_SEED = 1235
np.random.seed(_SEED)
#specify genes
MAX_NEURONS_PER_LAYER = 64         #must be mod 2
MAX_HIDDEN_LAYERS = 4              #must be mod 2
ACTIVATION_FUNCTION = "tanh"       #tanh, relu, lncosh
#calculate bit lengths of genes
BIT_LENGTH_NO_LAYER =int(math.log2(MAX_NEURONS_PER_LAYER))
BIT_LENGTH_HIDDEN_LAYER = int(math.log2(MAX_HIDDEN_LAYERS))
BIT_LENGTH_CHROMOSOME = BIT_LENGTH_NO_LAYER + BIT_LENGTH_HIDDEN_LAYER
#reproduction details
TOURNAMENT_SIZE = 8
POPULATION_SIZE = 10
MUTATE_PROB = 0.01
SELECTION_METHOD = "tournament"     #tournament, roulette

CROSSOVER_PROP = 0.75



#specify details of network optimization
L = 8
J = 1
#optimizer
OPTIMIZER = "AdaMax"
ALPHA=0.001 #0.001
BETA1=0.9 #0.9
BETA2=0.999 #0.999
EPSCUT=1e-07 #1e-07
#sampler
SAMPLER = "MetropolisHop"    #["MetropolisLocal","MetropolisHop"]
D_MAX = 5
#VMC
DISCARDED_SAMPLES = 100
DISCARDED_SAMPLES_ON_INIT = 0
METHOD = "Sr"               #["Gd","Sr"]
N_SAMPLES = 100
DIAG_SHIFT = 10
USE_ITERATIVE = True   #[False,True]
USE_CHOLESKY = True         #[False,True]
TARGET = "energy"
N_ITER = 1

#exact Solutions
_EXACT_GS_L6 = -1.020297256150904
_EXACT_GS_L8 = -1.167949517433288
_EXACT_GS_L10 = -1.2458475990024203
_EXACT_GS_L12 = -1.2904796001439305
_EXACT_GS_L14 = -1.315908522095936
_EXACT_GS_INFINITY = -1.401484038970

if L==6:
    EXACT_GS = L*_EXACT_GS_L6
elif L==8:
    EXACT_GS = L * _EXACT_GS_L8
elif L==10:
    EXACT_GS = L * _EXACT_GS_L10
elif L==12:
    EXACT_GS = L * _EXACT_GS_L12
elif L==14:
    EXACT_GS = L * _EXACT_GS_L14
else:
    EXACT_GS = L * _EXACT_GS_INFINITY


#global working directory
DIRECTORY = "logs/L%d_%d_%d_%s" %(L,MAX_NEURONS_PER_LAYER,MAX_HIDDEN_LAYERS,ACTIVATION_FUNCTION)
if not (os.path.exists(DIRECTORY)):
    os.mkdir(DIRECTORY)











def main():
    p1 = Population.Population.create_random_population()
    p1.print_genes()
    for _ in range(40):
        p1.new_generation()
        p1.print_genes()


if __name__=="__main__":
    main()