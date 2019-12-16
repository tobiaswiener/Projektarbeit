import numpy as np
import math
import os
import Individual
import Population
import matplotlib.pyplot as plt
import geneticPlot
import netket as nk
import configparser
import shutil


config = configparser.ConfigParser()
config.read("mainconfig.ini")


_CONFIG = config["misc"]["_CONFIG"]
_FUNCTION = config["misc"]["_FUNCTION"]
_FOLDER = config["misc"]["_FOLDER"]


if _FUNCTION == "tournament_plot_all":
    nconfig =config["misc"]["_FOLDER"] + "/" + _CONFIG
    config.clear()
    config.read(nconfig)


#setting global seed
_SEED = int(config["misc"]["_SEED"])

np.random.seed(_SEED)


#specify genes
MAX_NEURONS_PER_LAYER = int(config["genes"]["MAX_NEURONS_PER_LAYER"])
MAX_HIDDEN_LAYERS = int(config["genes"]["MAX_HIDDEN_LAYERS"])
ACTIVATION_FUNCTION = config["genes"]["ACTIVATION_FUNCTION"]
#calculate bit lengths of genes
BIT_LENGTH_NO_LAYER =int(math.log2(MAX_NEURONS_PER_LAYER))
BIT_LENGTH_HIDDEN_LAYER = int(math.log2(MAX_HIDDEN_LAYERS))
BIT_LENGTH_CHROMOSOME = BIT_LENGTH_NO_LAYER + BIT_LENGTH_HIDDEN_LAYER
#reproduction details
TOURNAMENT_SIZE = int(config["reproduction"]["TOURNAMENT_SIZE"])
POPULATION_SIZE = int(config["reproduction"]["POPULATION_SIZE"])
MUTATE_PROB = float(config["reproduction"]["MUTATE_PROB"])
SELECTION_METHOD = config["reproduction"]["SELECTION_METHOD"]
CROSSOVER_PROP = float(config["reproduction"]["CROSSOVER_PROP"])
GENERATIONS = int(config["reproduction"]["GENERATIONS"])



#specify details of network optimization
L = int(config["model"]["L"])       #6-18
J = int(config["model"]["J"])
#optimizer
OPTIMIZER = config["optimizer"]["OPTIMIZER"]
ALPHA= float(config["optimizer"]["ALPHA"])
BETA1= float(config["optimizer"]["BETA1"])
BETA2= float(config["optimizer"]["BETA2"])
EPSCUT=float(config["optimizer"]["EPSCUT"])

#sampler
SAMPLER = config["sampler"]["SAMPLER"]
D_MAX = config["sampler"]["D_MAX"]
#VMC
DISCARDED_SAMPLES = int(config["VMC"]["DISCARDED_SAMPLES"])
DISCARDED_SAMPLES_ON_INIT = int(config["VMC"]["DISCARDED_SAMPLES_ON_INIT"])
METHOD = config["VMC"]["METHOD"]
N_SAMPLES = int(config["VMC"]["N_SAMPLES"])
DIAG_SHIFT = int(config["VMC"]["DIAG_SHIFT"])
USE_ITERATIVE = config["VMC"].getboolean("USE_ITERATIVE")
USE_CHOLESKY = config["VMC"].getboolean("USE_CHOLESKY")
TARGET = config["VMC"]["TARGET"]
N_ITER = int(config["VMC"]["N_ITER"])

#exact Solutions
_EXACT_GS_L6 = float(config["exactSolutions"]["_EXACT_GS_L6"])
_EXACT_GS_L8 = float(config["exactSolutions"]["_EXACT_GS_L8"])
_EXACT_GS_L10 = float(config["exactSolutions"]["_EXACT_GS_L10"])
_EXACT_GS_L12 = float(config["exactSolutions"]["_EXACT_GS_L12"])
_EXACT_GS_L14 = float(config["exactSolutions"]["_EXACT_GS_L14"])
_EXACT_GS_INFINITY = float(config["exactSolutions"]["_EXACT_GS_INFINITY"])

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
#DIRECTORY = "%s/L%d_%d_%d_I%d_S%d_%s" %(_FOLDER,L,MAX_NEURONS_PER_LAYER,MAX_HIDDEN_LAYERS,N_ITER,N_SAMPLES,METHOD)
DIRECTORY =_FOLDER
try:
    os.mkdir(_FOLDER)
except:
    pass
try:
    os.mkdir(DIRECTORY)
except:
    pass




def save_config():
    n=1
    while os.path.isfile(DIRECTORY+"/"+"config"+str(n)+".ini"):
        n+=1
    shutil.copy("config.ini",DIRECTORY+"/"+"config"+str(n)+".ini")


def tournament_test():
    pop = Population.Population.create_random_population()
    pop.print_genes()
    fitnesslist = [[pop.give_generation()], [pop.sum_fitness()]]
    for gen in range(GENERATIONS):
        pop.new_generation()
        fitnesslist[0].append(gen + 1)
        fitnesslist[1].append(pop.sum_fitness())
        pop.print_genes()

    plt.plot(fitnesslist[0], fitnesslist[1], label="Tournament size" + str(3))

    print("Total Number Networks: " , len(Individual.CALCULATED_NETWORKS))

def tournament_plot_all():
    pop = Population.Population.create_random_population()
    pop.print_genes()

    for gen in range(GENERATIONS):
        pop.new_generation()
        pop.print_genes()
    fittest_genome = pop.give_fittest_individual().give_genes().bin

    geneticPlot.plot_folder_in_same_plot(DIRECTORY,"machine")
    geneticPlot.plot_file(fittest_genome+".log",DIRECTORY)
    print("Possible Networks", 2**BIT_LENGTH_CHROMOSOME)
    print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))
    print(pop.give_fittest_individual().decode_genome())

def tournament_cluster():
    if(nk.MPI.rank()==0):
        save_config()
    pop = Population.Population.create_random_population()
    if(nk.MPI.rank()==0):
        pop.print_genes()
    for gen in range(GENERATIONS):
        pop.new_generation()
        if (nk.MPI.rank() == 0):
            pop.print_genes()
    if(nk.MPI.rank()==0):
        print("Possible Networks", 2 ** BIT_LENGTH_CHROMOSOME)
        print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))



def main():
    if _FUNCTION == "tournament_cluster":
        tournament_cluster()
    elif _FUNCTION == "tournament_plot_all":
        tournament_plot_all()
    elif _FUNCTION == "create_all":
        Population.Population.create_all()

if __name__=="__main__":
    main()