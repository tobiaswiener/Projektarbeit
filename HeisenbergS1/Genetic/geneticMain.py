import numpy as np
import math
import os
import Individual
import Population
import matplotlib.pyplot as plt
import geneticPlot
import netket as nk
import configparser
import time

config = configparser.ConfigParser()
config.read("config.ini")

# setting global seed
_SEED = int(config["misc"]["_SEED"])
_FUNCTION = config["misc"]["_FUNCTION"]
np.random.seed(_SEED)
_FOLDER = config["misc"]["_FOLDER"]
# specify genes
MAX_NEURONS_PER_LAYER = int(config["genes"]["MAX_NEURONS_PER_LAYER"])
MAX_HIDDEN_LAYERS = int(config["genes"]["MAX_HIDDEN_LAYERS"])
ACTIVATION_FUNCTION = config["genes"]["ACTIVATION_FUNCTION"]
# calculate bit lengths of genes
BIT_LENGTH_NO_LAYER = int(math.log2(MAX_NEURONS_PER_LAYER))
BIT_LENGTH_HIDDEN_LAYER = int(math.log2(MAX_HIDDEN_LAYERS))
BIT_LENGTH_CHROMOSOME = BIT_LENGTH_NO_LAYER + BIT_LENGTH_HIDDEN_LAYER
# reproduction details


TOURNAMENT_SIZE = int(config["reproduction"]["TOURNAMENT_SIZE"])
POPULATION_SIZE = int(config["reproduction"]["POPULATION_SIZE"])
MUTATE_PROB = float(config["reproduction"]["MUTATE_PROB"])
SELECTION_METHOD = config["reproduction"]["SELECTION_METHOD"]
CROSSOVER_PROP = float(config["reproduction"]["CROSSOVER_PROP"])
GENERATIONS = int(config["reproduction"]["GENERATIONS"])

# specify details of network optimization
L = int(config["model"]["L"])  # 6-18
J = int(config["model"]["J"])
# optimizer
OPTIMIZER = config["optimizer"]["OPTIMIZER"]
ALPHA = float(config["optimizer"]["ALPHA"])
BETA1 = float(config["optimizer"]["BETA1"])
BETA2 = float(config["optimizer"]["BETA2"])
EPSCUT = float(config["optimizer"]["EPSCUT"])

# sampler
SAMPLER = config["sampler"]["SAMPLER"]
D_MAX = config["sampler"]["D_MAX"]
# VMC
DISCARDED_SAMPLES = int(config["VMC"]["DISCARDED_SAMPLES"])
DISCARDED_SAMPLES_ON_INIT = int(config["VMC"]["DISCARDED_SAMPLES_ON_INIT"])
METHOD = config["VMC"]["METHOD"]
N_SAMPLES = int(config["VMC"]["N_SAMPLES"])
DIAG_SHIFT = int(config["VMC"]["DIAG_SHIFT"])
USE_ITERATIVE = config["VMC"].getboolean("USE_ITERATIVE")
USE_CHOLESKY = config["VMC"].getboolean("USE_CHOLESKY")
TARGET = config["VMC"]["TARGET"]
N_ITER = int(config["VMC"]["N_ITER"])

# exact Solutions
_EXACT_GS_L6 = float(config["exactSolutions"]["_EXACT_GS_L6"])
_EXACT_GS_L8 = float(config["exactSolutions"]["_EXACT_GS_L8"])
_EXACT_GS_L10 = float(config["exactSolutions"]["_EXACT_GS_L10"])
_EXACT_GS_L12 = float(config["exactSolutions"]["_EXACT_GS_L12"])
_EXACT_GS_L14 = float(config["exactSolutions"]["_EXACT_GS_L14"])
_EXACT_GS_INFINITY = float(config["exactSolutions"]["_EXACT_GS_INFINITY"])

if L == 6:
    EXACT_GS = L * _EXACT_GS_L6
elif L == 8:
    EXACT_GS = L * _EXACT_GS_L8
elif L == 10:
    EXACT_GS = L * _EXACT_GS_L10
elif L == 12:
    EXACT_GS = L * _EXACT_GS_L12
elif L == 14:
    EXACT_GS = L * _EXACT_GS_L14
else:
    EXACT_GS = L * _EXACT_GS_INFINITY

# global working directory
# DIRECTORY = "%s/L%d_%d_%d_I%d_S%d_%s_TS%d_PS%d" %(_FOLDER,L,MAX_NEURONS_PER_LAYER,MAX_HIDDEN_LAYERS,N_ITER,N_SAMPLES,METHOD,TOURNAMENT_SIZE,POPULATION_SIZE)
DIRECTORY = "%s/L%d_%d_%d" % (_FOLDER, L, MAX_NEURONS_PER_LAYER, MAX_HIDDEN_LAYERS)
try:
    os.mkdir(_FOLDER)
except:
    pass
try:
    os.mkdir(DIRECTORY)
except:
    pass


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

    print("Total Number Networks: ", len(Individual.CALCULATED_NETWORKS))


def tournament_plot_all():
    pop = Population.Population.create_random_population()
    pop.print_genes()

    for gen in range(GENERATIONS):
        pop.new_generation()
        pop.print_genes()
    fittest_genome = pop.give_fittest_individual().give_genes().bin

    geneticPlot.plot_folder_in_same_plot(DIRECTORY, "machine")
    geneticPlot.plot_file(fittest_genome + ".log", DIRECTORY)
    print("Possible Networks", 2 ** BIT_LENGTH_CHROMOSOME)
    print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))
    print(pop.give_fittest_individual().decode_genome())


def tournament_cluster():
    pop = Population.Population.create_random_population()
    if (nk.MPI.rank() == 0):
        pop.print_genes()
    for gen in range(GENERATIONS):
        pop.new_generation()
        if (nk.MPI.rank() == 0):
            pop.print_genes()
    if (nk.MPI.rank() == 0):
        print("Possible Networks", 2 ** BIT_LENGTH_CHROMOSOME)
        print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))


def test_hyper():
    # pop = Population.Population.create_random_population()
    # pop.print_genes()
    # list = []
    # list.append(pop.give_fittest_individual().give_fitness())
    # for gen in range(GENERATIONS):
    #     pop.new_generation()
    #     pop.print_genes()
    #     list.append(pop.give_fittest_individual().give_fitness())
    # print("Possible Networks", 2 ** BIT_LENGTH_CHROMOSOME)
    # print("Calculated Networks: ", len(Individual.CALCULATED_NETWORKS))
    # plt.plot(list)
    # plt.show()
    list_of_steps = []

    for popsize in range(6, 40, 2):
        for toursize in range(2, 20):
            for mutateprob in [0., 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:
                for crossprob in [0., 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375,
                                  0.4375, 0.5, 0.5625, 0.625, 0.6875, 0.75, 0.8125,
                                  0.875, 0.9375, 1]:
                    try:
                        global TOURNAMENT_SIZE
                        global POPULATION_SIZE
                        global MUTATE_PROB
                        global CROSSOVER_PROP
                        list = []
                        POPULATION_SIZE = popsize
                        TOURNAMENT_SIZE = toursize
                        MUTATE_PROB = mutateprob
                        CROSSOVER_PROP = crossprob
                        pop = Population.Population.create_random_population()
                        list.append(pop.give_fittest_individual().give_fitness())
                        for gen in range(GENERATIONS):
                            pop.new_generation()
                            list.append(pop.give_fittest_individual().give_fitness())

                        steps = 0
                        most = list[0]

                        for i in list:
                            if (most < i):
                                most = i
                                steps += 1

                        name = "PS%d_TS%d_MP%f_CP%f_most%f_steps%d" % (
                            popsize, toursize, mutateprob, crossprob, most, steps)
                        # plt.plot(list,label=name)
                        element = [steps, most, "CalculatedNetworks: " + str(len(Individual.CALCULATED_NETWORKS)),
                                   "PopulationSize" + str(popsize), "TourSize" + str(toursize),
                                   "Mutation" + str(mutateprob), "Crossover" + str(crossprob)]
                        list_of_steps.append(element)
                        print(element)
                    except:
                        pass
                    finally:
                        Individual.CALCULATED_NETWORKS = []

    # plt.legend()
    # plt.show()
    print("sort by steps")
    print("----------------------------------------")
    sorted_by_steps = sorted(list_of_steps, key=lambda tup: tup[0], reverse=True)
    for i in sorted_by_steps:
        print(i)
    print("sort by fitness")
    print("----------------------------------------")
    sorted_by_fitness = sorted(list_of_steps, key=lambda tup: tup[1], reverse=True)
    for i in sorted_by_fitness:
        print(i)

    file_steps = DIRECTORY + "/sorted_by_steps.txt"
    file_fitness = DIRECTORY + "/sorted_by_fitness.txt"

    with open(file_steps, 'w') as f:
        for item in sorted_by_steps:
            f.write("%s\n" % item)

    with open(file_fitness, 'w') as f:
        for item in sorted_by_fitness:
            f.write("%s\n" % item)


def main():
    if _FUNCTION == "tournament_cluster":
        tournament_cluster()
    elif _FUNCTION == "tournament_plot_all":
        tournament_plot_all()
    elif _FUNCTION == "create_all":
        Population.Population.create_all()
    elif _FUNCTION == "test_hyper":
        test_hyper()


if __name__ == "__main__":
    main()
