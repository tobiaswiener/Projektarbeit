import numpy as np
import netket as nk
from bitstring import BitArray, BitStream, BitString
import math
import os
import json
import matplotlib.pyplot as plt
import copy
directory = "test"
try:
    os.mkdir(directory)
except(FileExistsError):
    pass

_POPULATION_SIZE = 100

_MAX_HIDDEN_LAYERS = 10
_MAX_NEURONS_PER_LAYER = 8
_ACTIVATION_FUNCTION = "tanh"

if(_MAX_NEURONS_PER_LAYER % 2 == 0):
    BIT_LENGTH_PER_LAYER = int(math.log2(_MAX_NEURONS_PER_LAYER))
else:
    BIT_LENGTH_PER_LAYER = math.floor(math.log2(_MAX_NEURONS_PER_LAYER)) + 1
BIT_LENGTH_CHROMOSOME = BIT_LENGTH_PER_LAYER *_MAX_HIDDEN_LAYERS


"""variables to specify"""
_L = 30
_J = 1
_seed = 12345
"""Optimizer"""
_optimizer = ["AdaMax"]
_alpha=0.001 #0.001
_beta1=0.9 #0.9
_beta2=0.999 #0.999
_epscut=1e-07 #1e-07
"""Sampler"""
_sampler = "MetropolisHop"    #["MetropolisLocal","MetropolisHop"]
_d_max = 5
"""VMC"""
_discarded_samples = 500
_discarded_samples_on_init = 0
_method = "Gd"               #["Gd","Sr"]
_n_samples = 2000
_diag_shift = 0.01
_use_iterative = False   #[False,True]
_use_cholesky = False         #[False,True]
_target = "energy"
_n_iter = 5000




class Individual:

    if(_MAX_NEURONS_PER_LAYER % 2 == 0):
        bit_length_per_layer = int(math.log2(_MAX_NEURONS_PER_LAYER))
    else:
        bit_length_per_layer = math.floor(math.log2(_MAX_NEURONS_PER_LAYER)) + 1
    bit_length_chromosome = bit_length_per_layer *_MAX_HIDDEN_LAYERS

    def __init__(self, genes:BitArray):
        self.genes = genes
        self.fitness = self.eval_fitness()


    def give_layer(self, counter:int):
        begin = counter * Individual.bit_length_per_layer
        end = (counter+1) * Individual.bit_length_per_layer
        layer = self.genes[begin:end].uint
        return layer


    def give_config_json(self):
        # config = [_ACTIVATION_FUNCTION,[]]
        # for i in range(_MAX_HIDDEN_LAYERS):
        #     config[1].append(self.give_layer(i))
        # return config
        return 5
    def create_ip(self):
        _model = self.give_config_json()
        dicc = {
            "input": {
                "L": _L, "J": _J,
                "machine": {"type": "FFNN", "model": _model},
                "sampler": {"type": _sampler, "d_max": _d_max},
                "optimizer": {"type": _optimizer, "alpha": _alpha, "beta1": _beta1, "beta2": _beta2, "epscut": _epscut},
                "VMC": {"n_samples": _n_samples, "discarded_samples": _discarded_samples, "discarded_samples_on_init": _discarded_samples_on_init,
                        "target": _target, "method": _method,
                        "diag_shift": _diag_shift, "use_iterative": _use_iterative, "use_cholesky": _use_iterative},
                "n_iter": _n_iter}
        }
        n=1
        filename = str(self.generation) + "_" + str(n)
        filenamelog = str(self.generation) + "_" + str(n)

        while (os.path.isfile(filename) or os.path.isfile(filenamelog)):
            n +=1
            filename = str(self.generation) + "_" + str(n)
            filenamelog = str(self.generation) + "_" + str(n)

        with open(directory +"/"+filename, 'w') as outfile:
            json.dump(dicc, outfile)

    def eval_fitness(self):
        f = 0
        for i in self.genes:
            if(i):
                f += 1
        return f

    def act_fitness(self):
        self.fitness = self.eval_fitness()


    @staticmethod
    def random_individual(seed=1235):
        bit_string = ""
        np.random.seed(seed)
        for _ in range(Individual.bit_length_chromosome):
            bit_string += str(np.random.randint(0,2))

        individual = Individual(BitArray("0b" + bit_string))

        return individual

    def mutate(self, mut_prob = 0.01):
        for i in range(BIT_LENGTH_CHROMOSOME):
            if(mut_prob > np.random.rand()):
                self.genes[i] = not(self.genes[i])
        return self





class Population:

    def __init__(self,population:[Individual]):
        self.individual_list = population
        self.generation = 0

    @staticmethod
    def random_population_list(pop_size:int = _POPULATION_SIZE):
        list_individuals = []
        for _ in range(pop_size):
            list_individuals.append(Individual.random_individual())

        return list_individuals
    def give_fitness_list(self):
        fitness_list = []
        for indiv in self.individual_list:
            fitness_list.append(indiv.fitness)
        return fitness_list





    def selection_tournament(self, mating_pool_size = _POPULATION_SIZE ,tournament_size = 2):
        mating_pool = []
        for i in range(mating_pool_size):
            tournament_pool = []

            for _ in range(tournament_size):
                r = np.random.randint(0,_POPULATION_SIZE)
                tournament_pool.append(self.individual_list[r])

            fittest_indiv = tournament_pool[0]

            for indiv in tournament_pool:           #find fittest individual in tournament pool
                if(indiv.fitness > fittest_indiv.fitness):
                    fittest_indiv = indiv

            mating_pool.append(fittest_indiv)
        return mating_pool

    def selection_roullete(self, mating_pool_size:_POPULATION_SIZE):
        mating_pool = []
        fitness_list = self.give_fitness_list()
        fitness_sum = 0
        for ind in fitness_list:
            fitness_sum += ind

        prob_list = []
        for ind in fitness_list:
            prob_list.append(ind/fitness_sum)

        prob_commulativ = np.cumsum(np.array(prob_list))


        for _ in range(mating_pool_size):
            r = np.random.rand()
            for i,qi in enumerate(prob_commulativ):
                if(r <= qi):
                    mating_pool.append(self.individual_list[i])
                    break
        return mating_pool


    @staticmethod
    def two_point_crossover(parent1:Individual, parent2:Individual, crossover=0.75):
        length = BIT_LENGTH_CHROMOSOME
        parent_1_genes = parent1.genes
        parent_2_genes = parent2.genes

        if (crossover > np.random.rand()):
            first = np.random.randint(0,length)
            second = np.random.randint(0,length)

            if(first > second):
                temp = first
                first = second
                second = temp

            p1 = [parent_1_genes[0:first],parent_1_genes[first:second],parent_1_genes[second:length]]
            p2 = [parent_2_genes[0:first], parent_2_genes[first:second], parent_2_genes[second: length]]

            genes_offspring_1 = p1[0]
            genes_offspring_1.append(p2[1])
            genes_offspring_1.append(p1[2])

            genes_offspring_2 = p2[0]
            genes_offspring_2.append(p1[1])
            genes_offspring_2.append(p2[2])

            return True, Individual(genes_offspring_1),Individual(genes_offspring_2)
        else:
            return False, parent1, parent2



    def new_generation(self,selection_method:str,tournament_size=2):
        new_population = []

        if(selection_method == "tournament"):
            mating_pool = self.selection_tournament(mating_pool_size=_POPULATION_SIZE,tournament_size=tournament_size)
        elif(selection_method == "roullete"):
            mating_pool = self.selection_roullete(mating_pool_size=_POPULATION_SIZE)


        for _ in range(int(_POPULATION_SIZE/2)):
            r1 = np.random.randint(0,len(mating_pool))
            r2 = np.random.randint(0,len(mating_pool))
            mated, new1, new2 = self.two_point_crossover(mating_pool[r1],mating_pool[r2])
            new_population.append(new1)
            new_population.append(new2)

        for indiv in new_population:
            indiv.mutate()
            indiv.act_fitness()

        self.individual_list = new_population
        self.generation += 1



    def sum_fitness(self):
        sum_fitness = 0
        for indiv in self.individual_list:
            sum_fitness += indiv.fitness

        return sum_fitness

    def print_genes(self):
        sum_fitness = 0
        print("generation " + str(self.generation))
        for counter, indiv in enumerate(self.individual_list):
            print(str(counter)+": " + "genome: " +str(indiv.genes)[2:] + " fitness: " + str(indiv.fitness))
            sum_fitness += indiv.fitness
        print("sum fitness: " + str(sum_fitness))
        print("---------------------------------")













def tournament_vs_roullete():
    pop1 = Population(Population.random_population_list())
    pop2 = Population(Population.random_population_list())
    fitnesslist1 = [[pop1.generation],[pop1.sum_fitness()]]
    fitnesslist2 = [[pop1.generation],[pop1.sum_fitness()]]

    for i in range(100):
        pop1.new_generation("tournament")
        fitnesslist1[0].append(pop1.generation)
        fitnesslist1[1].append(pop1.sum_fitness())

        pop2.new_generation("roullete")
        fitnesslist2[0].append(pop2.generation)
        fitnesslist2[1].append(pop2.sum_fitness())


    plt.plot(fitnesslist1[0],fitnesslist1[1],label="tournament")
    plt.plot(fitnesslist2[0], fitnesslist2[1],label="roullete")
    plt.legend()
    plt.show()

def tournament_pool_size():



    for tour_size in range(10):
        pop = Population(Population.random_population_list())
        fitnesslist = [[pop.generation],[pop.sum_fitness()]]
        for gen in range(100):
            pop.new_generation("tournament",tour_size+1)
            fitnesslist[0].append(gen+1)
            fitnesslist[1].append(pop.sum_fitness())
        plt.plot(fitnesslist[0],fitnesslist[1],label="Tournament size" + str(tour_size+1))

    plt.legend()
    plt.show()

def main():
    tournament_pool_size()

if __name__ == "__main__":
    main()