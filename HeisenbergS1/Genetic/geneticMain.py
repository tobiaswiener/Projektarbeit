import numpy as np
import math
import os
import Individual
import Population
import matplotlib.pyplot as plt
import geneticPlot
import netket as nk


CLUSTER = True  #True,False
#setting global seed
_SEED = 1234
np.random.seed(_SEED)
#specify genes
MAX_NEURONS_PER_LAYER = 128         #must be mod 2
MAX_HIDDEN_LAYERS = 8              #must be mod 2
ACTIVATION_FUNCTION = "tanh"       #tanh, relu, lncosh
#calculate bit lengths of genes
BIT_LENGTH_NO_LAYER =int(math.log2(MAX_NEURONS_PER_LAYER))
BIT_LENGTH_HIDDEN_LAYER = int(math.log2(MAX_HIDDEN_LAYERS))
BIT_LENGTH_CHROMOSOME = BIT_LENGTH_NO_LAYER + BIT_LENGTH_HIDDEN_LAYER
#reproduction details
TOURNAMENT_SIZE = 4                 #4
POPULATION_SIZE = 10                #30
MUTATE_PROB = 0.01                  #0.01
SELECTION_METHOD = "tournament"     #tournament, roulette
CROSSOVER_PROP = 0.75               #0.75



#specify details of network optimization
L = 6       #6-18
J = 1
#optimizer
OPTIMIZER = "AdaMax"
ALPHA=0.001 #0.001
BETA1=0.9 #0.9
BETA2=0.999 #0.999
EPSCUT=1e-07 #1e-07
#sampler
SAMPLER = "MetropolisLocal"    #["MetropolisLocal","MetropolisHop"]
D_MAX = 5
#VMC
DISCARDED_SAMPLES = 100
DISCARDED_SAMPLES_ON_INIT = 0
METHOD = "Gd"               #["Gd","Sr"]
N_SAMPLES = 1000
DIAG_SHIFT = 10
USE_ITERATIVE = True   #[False,True]
USE_CHOLESKY = True         #[False,True]
TARGET = "energy"
N_ITER = 100

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
DIRECTORY = "logs/L%d_%d_%d_I%d_S%d_%s" %(L,MAX_NEURONS_PER_LAYER,MAX_HIDDEN_LAYERS,N_ITER,N_SAMPLES,METHOD)

try:
    os.mkdir(DIRECTORY)
except:
    pass






def tournament_test():
    pop = Population.Population.create_random_population()
    pop.print_genes()
    fitnesslist = [[pop.give_generation()], [pop.sum_fitness()]]
    for gen in range(50):
        pop.new_generation()
        fitnesslist[0].append(gen + 1)
        fitnesslist[1].append(pop.sum_fitness())
        pop.print_genes()

    plt.plot(fitnesslist[0], fitnesslist[1], label="Tournament size" + str(3))

    print("Total Number Networks: " , len(Individual.CALCULATED_NETWORKS))

def tournament_plot_all():
    pop = Population.Population.create_random_population()
    pop.print_genes()

    for gen in range(15):
        pop.new_generation()
        pop.print_genes()
    fittest_genome = pop.give_fittest_individual().give_genes().bin
    geneticPlot.plot_folder_in_same_plot(DIRECTORY,"machine")
    geneticPlot.plot_file(fittest_genome+".log",DIRECTORY)
    print("Possible Networks", 2**BIT_LENGTH_CHROMOSOME)
    print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))
    print(pop.give_fittest_individual().decode_genome())

def tournament_cluster():
    pop = Population.Population.create_random_population()
    if(nk.MPI.rank()==0):
        pop.print_genes()
    for gen in range(100):
        pop.new_generation()
        if (nk.MPI.rank() == 0):
            pop.print_genes()
    if(nk.MPI.rank()==0):
        print("Possible Networks", 2 ** BIT_LENGTH_CHROMOSOME)
        print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))


def main():

    #tournament_cluster()
    tournament_plot_all()
    pass
if __name__=="__main__":
    main()