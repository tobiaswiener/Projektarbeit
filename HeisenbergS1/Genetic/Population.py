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