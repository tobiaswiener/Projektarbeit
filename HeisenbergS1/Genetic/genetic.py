import numpy as np
import netket as nk
from bitstring import BitArray, BitStream, BitString
import math
import os
import json
import copy
directory = "test"
try:
    os.mkdir(directory)
except(FileExistsError):
    pass

_POPULATION_SIZE = 10

_MAX_HIDDEN_LAYERS = 3
_MAX_NEURONS_PER_LAYER = 8
_ACTIVATION_FUNCTION = "tanh"




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

    def __init__(self, genes:BitArray,generation:int):
        self.genes = genes
        self.generation = generation
        self.f = np.random.randint(0,100)


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

    def fitness(self):
        return self.f


    @staticmethod
    def random_individual():
        bit_string = ""
        for _ in range(Individual.bit_length_chromosome):
            bit_string += str(np.random.randint(0,2))

        individual = Individual(BitArray("0b" + bit_string),0)

        return individual





class Population:

    def __init__(self,population:[Individual]):
        self.individual_list = population

    @staticmethod
    def random_population_list(pop_size:int):
        list_individuals = []
        for _ in range(pop_size):
            list_individuals.append(Individual.random_individual())

        return list_individuals
    def give_fitness_list(self):
        fitness_list = []
        for indiv in self.individual_list:
            fitness_list.append(indiv.fitness())
        return fitness_list


    def selection_roullete(self, mating_pool_size:int):
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
        print(fitness_list)
        print(prob_list)
        print(prob_commulativ)
        for i in mating_pool:
            print(i.fitness())
        return mating_pool


    @staticmethod
    def two_point_crossover(parent1:Individual, parent2:Individual, crossover: float):
        length = parent1.bit_length_chromosome

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

            return True, genes_offspring_1,genes_offspring_2
        else:
            return False, parent_1_genes, parent_2_genes












def main():
    pop1 = Population(Population.random_population_list(10))
    parent1 = pop1.individual_list[0]
    parent2 = pop1.individual_list[2]
    a, b, c = Population.two_point_crossover(parent1, parent2, 0.5)
    print(parent1.genes)
    print(parent2.genes)
    print(a)
    print(b)
    print(c)

if __name__ == "__main__":
    main()