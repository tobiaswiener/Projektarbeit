import numpy as np
import netket as nk
from bitstring import BitArray, BitStream, BitString
import math
import os
import json
import build
import time
import matplotlib.pyplot as plt
import os.path
import copy
directory = "test"
seed = 2335
np.random.seed(seed=seed)
EXACT_GS_LANCZOS_L6 = -6.121783536905424
try:
    os.mkdir(directory)
except(FileExistsError):
    pass

_POPULATION_SIZE = 100

_MAX_HIDDEN_LAYERS = 4
_MAX_NEURONS_PER_LAYER = 64
_ACTIVATION_FUNCTION = "tanh"

if(_MAX_NEURONS_PER_LAYER % 2 == 0):
    BIT_LENGTH_PER_LAYER = int(math.log2(_MAX_NEURONS_PER_LAYER))
else:
    BIT_LENGTH_PER_LAYER = math.floor(math.log2(_MAX_NEURONS_PER_LAYER)) + 1


if(_MAX_HIDDEN_LAYERS % 2 == 0):
    BIT_LENGTH_HIDDEN_LAYER = int(math.log2(_MAX_HIDDEN_LAYERS))
else:
    BIT_LENGTH_HIDDEN_LAYER = int(math.log2(_MAX_HIDDEN_LAYERS)) + 1



BIT_LENGTH_CHROMOSOME = BIT_LENGTH_PER_LAYER + BIT_LENGTH_HIDDEN_LAYER


"""variables to specify"""
_L = 6
_J = 1
_seed = 12345
"""Optimizer"""
_optimizer = "AdaMax"
_alpha=0.001 #0.001
_beta1=0.9 #0.9
_beta2=0.999 #0.999
_epscut=1e-07 #1e-07
"""Sampler"""
_sampler = "MetropolisHop"    #["MetropolisLocal","MetropolisHop"]
_d_max = 5
"""VMC"""
_discarded_samples = 100
_discarded_samples_on_init = 0
_method = "Gd"               #["Gd","Sr"]
_n_samples = 200
_diag_shift = 0.01
_use_iterative = False   #[False,True]
_use_cholesky = False         #[False,True]
_target = "energy"
_n_iter = 100




class Individual:

    # if(_MAX_NEURONS_PER_LAYER % 2 == 0):
    #     bit_length_per_layer = int(math.log2(_MAX_NEURONS_PER_LAYER))
    # else:
    #     bit_length_per_layer = math.floor(math.log2(_MAX_NEURONS_PER_LAYER)) + 1
    # bit_length_chromosome = bit_length_per_layer *_MAX_HIDDEN_LAYERS

    def __init__(self, genes:BitArray):
        self.genes = genes
        self.dicc = self.create_dicc()
        self.fitness = self.eval_fitness()



    # def give_layer(self, counter:int):
    #     begin = counter * Individual.bit_length_per_layer
    #     end = (counter+1) * Individual.bit_length_per_layer
    #     layer = self.genes[begin:end].uint
    #     return layer
    #
    #
    # def give_config_json(self):
    #     config = [_ACTIVATION_FUNCTION,[]]
    #     for i in range(_MAX_HIDDEN_LAYERS):
    #          config[1].append(self.give_layer(i))
    #     return config


    def decode_genome(self):
        config = []
        act_func = _ACTIVATION_FUNCTION
        begin_npl = 0
        end_npl = BIT_LENGTH_PER_LAYER
        neurons_per_layer = self.genes[begin_npl:end_npl].uint+1

        begin_hl = BIT_LENGTH_PER_LAYER
        end_hl = begin_hl + BIT_LENGTH_HIDDEN_LAYER+1
        hidden_layer = self.genes[begin_hl:end_hl].uint+1
        config.append(act_func)
        config.append(neurons_per_layer)
        config.append(hidden_layer)

        return config



    def create_dicc(self):
        _model = self.decode_genome()
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
        return dicc



    def run_genome(self):
        graph, hilbert, hamilton = build.generateNN(length=_L, coupling=_J)
        config = self.decode_genome()

        layers = []

        layers.append(
            nk.layer.FullyConnected(input_size=_L, output_size=int(config[1]), use_bias=True))

        for _ in range(config[2]-1):
            layers.append(nk.layer.Tanh(input_size=int(config[1])))

        layers.append(nk.layer.SumOutput(input_size=int(config[1])))
        layers = tuple(layers)  # layers must be tuple

        for layer in layers:
            layer.init_random_parameters(seed=543164684, sigma=0.01)
        ma = nk.machine.FFNN(hilbert, layers)

        if (_sampler == "MetropolisLocal"):
            sa = nk.sampler.MetropolisLocal(machine=ma)
        elif (_sampler == "MetropolisHop"):
            sa = nk.sampler.MetropolisHop(machine=ma, d_max=_d_max)
        if (_optimizer == "AdaMax"):
            opt = nk.optimizer.AdaMax(alpha=_alpha, beta1=_beta1, beta2=_beta2, epscut=_epscut)
        elif (_optimizer == "AmsGrad"):
            opt = nk.optimizer.AmsGrad(learning_rate=_alpha, beta1=_beta1, beta2=_beta2,
                                       epscut=_epscut)

        gs = nk.variational.Vmc(hamiltonian=hamilton,
                                sampler=sa,
                                optimizer=opt,
                                n_samples=_n_samples,
                                use_iterative=_use_iterative,
                                use_cholesky=_use_cholesky,
                                method=_method,
                                diag_shift=_diag_shift,
                                discarded_samples=_discarded_samples,
                                discarded_samples_on_init=_discarded_samples_on_init,
                                target=_target)

        file_name = str(self.genes.bin)
        try:
            start_time = time.time()
            gs.run(output_prefix=directory + "/" + file_name, n_iter=_n_iter)
            end_time = time.time()

            if (nk._C_netket.MPI.rank() == 0):
                with open(directory + "/" + file_name + ".log", "a") as f:
                    f.write("\n")
                    json.dump(self.dicc, f)
                    f.write("\nduration: " + str(start_time - end_time))
        except:
            print(directory + "/" + file_name + "failed")


    def eval_fitness_1(self):
        # f = 0
        # for i in self.genes:
        #     if(i):
        #         f += 1
        # return f
        f = 0
        for i in range(BIT_LENGTH_CHROMOSOME):
            if(self.genes[i] and not(self.genes[(i+1) % BIT_LENGTH_CHROMOSOME])):
                f += 1
            elif(not(self.genes[i]) and self.genes[(i+1) % BIT_LENGTH_CHROMOSOME]):
                f += 1
            else:
                pass
        return f

    def eval_fitness(self):
        file_name = self.genes.bin
        if not(os.path.isfile(directory + "/" + file_name + ".log")):
            self.run_genome()
        data = []
        try:
            if (nk._C_netket.MPI.rank() == 0):
                with open(directory + "/" + file_name + ".log") as f:
                    #print(directory + "/" + file_name + ".log")
                    lines = f.readlines()
                for line in lines[-53:-3]:
                    try:
                        b = json.loads(line[0:len(line) - 2])
                        data.append(b)
                    except ValueError:
                        print(str(line) +"failed")
        except:
            print("fail")
            pass
        energy_sum = 0
        for iteration in data:
            energy_sum += iteration["Energy"]["Mean"]
        energy_mean = energy_sum/len(data)

        diff = np.abs(energy_mean-EXACT_GS_LANCZOS_L6)
        fitness = np.abs(np.log(1/diff))
        return fitness

    #     self.run_genome()
    #     name = str(self.genes.bin)
    #     with open(directory + "/" + name) as f:
    #         lines = f.readlines()
    #     for line in lines:
    #         try:
    #             b = json.loads(line[0:len(line) - 2])
    #             data.append(b)
    #         except ValueError as e:
    #             print(counter)
    #             pass




    def act_fitness(self):
        self.fitness = self.eval_fitness()


    @staticmethod
    def random_individual():
        bit_string = ""

        for _ in range(BIT_LENGTH_CHROMOSOME):
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
            print(str(counter)+": " + "genome: " +str(indiv.genes.bin) + " fitness: " + str(indiv.fitness))
            sum_fitness += indiv.fitness
        print("sum fitness: " + str(sum_fitness))
        print("---------------------------------")













def tournament_vs_roullete():
    pop1 = Population(Population.random_population_list())
    pop2 = Population(Population.random_population_list())
    fitnesslist1 = [[pop1.generation],[pop1.sum_fitness()]]
    fitnesslist2 = [[pop1.generation],[pop1.sum_fitness()]]

    for i in range(100):
        pop1.new_generation("tournament",tournament_size=7)
        fitnesslist1[0].append(pop1.generation)
        fitnesslist1[1].append(pop1.sum_fitness())

        pop2.new_generation("roullete")
        fitnesslist2[0].append(pop2.generation)
        fitnesslist2[1].append(pop2.sum_fitness())


    plt.plot(fitnesslist1[0],fitnesslist1[1],label="tournament")
    plt.plot(fitnesslist2[0], fitnesslist2[1],label="roullete")
    pop1.print_genes()
    pop2.print_genes()
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
        pop.print_genes()

    plt.legend()
    plt.show()
def test_tournament():
    pop = Population(Population.random_population_list())
    fitnesslist = [[pop.generation], [pop.sum_fitness()]]
    for gen in range(20):
        pop.new_generation("tournament", 4)
        fitnesslist[0].append(gen + 1)
        fitnesslist[1].append(pop.sum_fitness())
        # plt.plot(fitnesslist[0], fitnesslist[1], label="Tournament size" + str(3))
        # plt.show()
        pop.print_genes()
    plt.plot(fitnesslist[0], fitnesslist[1], label="Tournament size" + str(3))
    pop.print_genes()
def main():
    pass
    #tournament_vs_roullete()
    #tournament_pool_size()
    #test_tournament()
if __name__ == "__main__":
    main()