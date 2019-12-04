import netket as nk
import numpy as np
import Individual
import geneticMain



class Population():

    def __init__(self, list_of_individuals: [Individual]):
        self.__list_of_individuals = list_of_individuals
        self.__generation = 0

    @staticmethod
    def create_random_population():
        list_of_individuals = []
        for _ in range(geneticMain.POPULATION_SIZE):
            list_of_individuals.append(Individual.Individual.random_individual())
        random_population = Population(list_of_individuals=list_of_individuals)
        return random_population

    def print_genes(self):
        sum_fitness = 0
        print("generation " + str(self.__generation))
        for counter, indiv in enumerate(self.__list_of_individuals):
            print(str(counter)+": " + "genome: " +str(indiv.give_genes().bin) + " fitness: " + str(indiv.eval_fitness()))
            sum_fitness += indiv.eval_fitness()
        print("sum fitness: " + str(sum_fitness))
        print("---------------------------------")

    def sum_fitness(self):
        sum_fitness = 0
        for indiv in self.__list_of_individuals:
            sum_fitness += indiv.eval_fitness()
        return sum_fitness

    # def new_generation(self):
    #     new_population = []
    #     selection_method = geneticMain.SELECTION_METHOD
    #
    #
    #     if(selection_method == "tournament"):
    #         mating_pool = self.selection_tournament()
    #     elif(selection_method == "roullete"):
    #         mating_pool = self.selection_roullete()
    #
    #     for _ in range(int(geneticMain.POPULATION_SIZE/2)):
    #         r1 = np.random.randint(0,len(mating_pool))
    #         r2 = np.random.randint(0,len(mating_pool))
    #         mated, new1, new2 = self.two_point_crossover(mating_pool[r1],mating_pool[r2])
    #         new_population.append(new1)
    #         new_population.append(new2)
    #
    #     for indiv in new_population:
    #         indiv.mutate()
    #
    #     self.individual_list = new_population
    #     self.generation += 1

    @staticmethod
    def two_point_crossover(parent1: Individual, parent2: Individual):
        bit_length_chromosome = geneticMain.BIT_LENGTH_CHROMOSOME
        crossover_prob = geneticMain.CROSSOVER_PROP
        parent_1_genes = parent1.give_genes().bin
        parent_2_genes = parent2.give_genes().bin

        if (crossover_prob > np.random.rand()):
            first_co_point = np.random.randint(0, bit_length_chromosome)
            second_co_point = np.random.randint(0, bit_length_chromosome)
            if (first_co_point > second_co_point):
                temp = first_co_point
                first_co_point = second_co_point
                second_co_point = temp

            parent_1_genes_cutted = [parent_1_genes[0:first_co_point], parent_1_genes[first_co_point:second_co_point], parent_1_genes[second_co_point:]]
            parent_2_genes_cutted = [parent_2_genes[0:first_co_point], parent_2_genes[first_co_point:second_co_point], parent_2_genes[second_co_point: ]]

            genes_offspring_1 = parent_1_genes_cutted[0]
            genes_offspring_1 += parent_2_genes_cutted[1]
            genes_offspring_1 += parent_1_genes_cutted[2]

            genes_offspring_2 = parent_2_genes_cutted[0]
            genes_offspring_2 += parent_1_genes_cutted[1]
            genes_offspring_2 += parent_2_genes_cutted[2]

            return True, Individual.Individual(genes_offspring_1), Individual.Individual(genes_offspring_2)
        else:
            return False, parent1, parent2