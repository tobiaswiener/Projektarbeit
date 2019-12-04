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



