import geneticMain
import numpy as np
import netket as nk
from bitstring import BitArray
import build
import time
import json
import os
import math


#List of calculated Networks
CALCULATED_NETWORKS = []

class Individual:

    def __init__(self, genes: str):
        self.__genes = BitArray("0b" + genes)
        self.__fitness = self.eval_fitness()
        global CALCULATED_NETWORKS
        if not(self.__genes.bin in CALCULATED_NETWORKS):
            CALCULATED_NETWORKS.append(self.__genes.bin)

    @staticmethod
    def random_individual():
        bit_string = ""
        for _ in range(geneticMain.BIT_LENGTH_CHROMOSOME):
            r = np.random.randint(0, 2)
            bit_string += str(r)
        indiv = Individual(bit_string)
        return indiv

    def give_genes(self):
        return self.__genes

    def decode_genome(self):
        config = []
        act_func = geneticMain.ACTIVATION_FUNCTION

        begin_npl = 0
        end_npl = geneticMain.BIT_LENGTH_NO_LAYER
        neurons_per_layer = self.__genes[begin_npl:end_npl].uint+1

        begin_hl = geneticMain.BIT_LENGTH_NO_LAYER
        end_hl = begin_hl + geneticMain.BIT_LENGTH_HIDDEN_LAYER + 1
        hidden_layer = self.__genes[begin_hl:end_hl].uint+1

        config.append(act_func)
        config.append(neurons_per_layer)
        config.append(hidden_layer)
        return config

    def create_dicc(self):
        model = self.decode_genome()
        dicc = {
            "input": {
                "L": geneticMain.L, "J": geneticMain.J,
                "machine": {"type": "FFNN", "model": model},
                "sampler": {"type": geneticMain.SAMPLER, "d_max": geneticMain.D_MAX},
                "optimizer": {"type": geneticMain.OPTIMIZER, "alpha": geneticMain.ALPHA, "beta1": geneticMain.BETA1,
                              "beta2": geneticMain.BETA2, "epscut": geneticMain.EPSCUT},
                "VMC": {"n_samples": geneticMain.N_SAMPLES, "discarded_samples": geneticMain.DISCARDED_SAMPLES,
                        "discarded_samples_on_init": geneticMain.DISCARDED_SAMPLES_ON_INIT,
                        "target": geneticMain.TARGET, "method": geneticMain.METHOD,
                        "diag_shift": geneticMain.DIAG_SHIFT, "use_iterative": geneticMain.USE_ITERATIVE,
                        "use_cholesky": geneticMain.USE_CHOLESKY},
                "n_iter": geneticMain.N_ITER}
        }
        return dicc

    def run_genome(self):
        graph, hilbert, hamilton = build.generateNN(length=geneticMain.L, coupling=geneticMain.J)
        config = self.decode_genome()
        neurons_per_layer = config[1]
        hidden_layer =config[2]
        layers = []
        layers.append(
            nk.layer.FullyConnected(input_size=geneticMain.L, output_size=neurons_per_layer, use_bias=True))
        for _ in range(hidden_layer):
            if(geneticMain.ACTIVATION_FUNCTION == "tanh"):
                layers.append(nk.layer.Tanh(input_size=neurons_per_layer))
            if (geneticMain.ACTIVATION_FUNCTION == "lncosh"):
                layers.append(nk.layer.Tanh(input_size=neurons_per_layer))
            if (geneticMain.ACTIVATION_FUNCTION == "relu"):
                layers.append(nk.layer.Tanh(input_size=neurons_per_layer))
        layers.append(nk.layer.SumOutput(input_size=neurons_per_layer))
        layers = tuple(layers)  # layers must be tuple
        for layer in layers:
            layer.init_random_parameters(seed=1234,sigma=0.01)
        ma = nk.machine.FFNN(hilbert, layers)

        if (geneticMain.SAMPLER == "MetropolisLocal"):
            sa = nk.sampler.MetropolisLocal(machine=ma)
        elif (geneticMain.SAMPLER == "MetropolisHop"):
            sa = nk.sampler.MetropolisHop(machine=ma, d_max=geneticMain.D_MAX)
        if (geneticMain.OPTIMIZER == "AdaMax"):
            opt = nk.optimizer.AdaMax(alpha=geneticMain.ALPHA, beta1=geneticMain.BETA1, beta2=geneticMain.BETA2,
                                      epscut=geneticMain.EPSCUT)
        elif (geneticMain.OPTIMIZER == "AmsGrad"):
            opt = nk.optimizer.AmsGrad(learning_rate=geneticMain.ALPHA, beta1=geneticMain.BETA1, beta2=geneticMain.BETA2,
                                       epscut=geneticMain.EPSCUT)


        gs = nk.variational.Vmc(hamiltonian=hamilton,
                                sampler=sa,
                                optimizer=opt,
                                n_samples=geneticMain.N_SAMPLES,
                                use_iterative=geneticMain.USE_ITERATIVE,
                                use_cholesky=geneticMain.USE_CHOLESKY,
                                method=geneticMain.METHOD,
                                diag_shift=geneticMain.DIAG_SHIFT,
                                discarded_samples=geneticMain.DISCARDED_SAMPLES,
                                discarded_samples_on_init=geneticMain.DISCARDED_SAMPLES_ON_INIT,
                                target=geneticMain.TARGET)
        file_name = str(self.give_genes().bin)
        try:
            start_time = time.time()
            gs.run(output_prefix=geneticMain.DIRECTORY + "/" + file_name, n_iter=geneticMain.N_ITER)
            end_time = time.time()

            if (nk._C_netket.MPI.rank() == 0):
                with open(geneticMain.DIRECTORY + "/" + file_name + ".log", "a") as f:
                    f.write("\n")
                    json.dump(self.create_dicc(), f)
                    f.write("\nduration: " + str(start_time - end_time))
        except:
            print(geneticMain.DIRECTORY + "/" + file_name + "failed")

    def eval_fitness(self):
        #todo punish heavy oscillations
        #todo render flat line invalid (maybe, maybe rerun?)
        fitness = 0
        file_name = self.__genes.bin
        if not(os.path.isfile(geneticMain.DIRECTORY + "/" + file_name + ".log")):
            self.run_genome()
        data=[]


        if not geneticMain.CLUSTER:
            try:
                with open(geneticMain.DIRECTORY + "/" + file_name + ".log") as f:
                    lines = f.readlines()
                for line in lines[:-3]:
                    try:
                        b = json.loads(line[0:len(line) - 2])
                        data.append(b)
                    except ValueError:
                        pass
            except:
                print("%s/%s.log failed" %(geneticMain.DIRECTORY,file_name))
                pass

            x = 50
            #Difference between Energy Mean of last x Iterations and Exact Value
            delta_energy_mean = math.inf
            energy_mean = math.inf
            energy_sum = 0
            try:
                for iteration in data[-x:]:          #last 50 iterations
                    energy_sum += iteration["Energy"]["Mean"]
                energy_mean = energy_sum/len(data[-x:])
                delta_energy_mean = np.abs(energy_mean-geneticMain.EXACT_GS)
            except ZeroDivisionError:
                delta_energy_mean = math.inf
                print("fitness evaluation (mean) for %s/%s failed" % (geneticMain.DIRECTORY,file_name))


            #Varianz of last x Iterations
            variance = 0
            try:
                for iteration in data[-x:]:
                    #variance += (iteration["Energy"]["Mean"]-energy_mean)**2          #todo try which one
                    variance += (iteration["Energy"]["Mean"]-geneticMain.EXACT_GS)**2
                variance = variance / len(data[-x:])
            except ZeroDivisionError:
                variance= math.inf
                print("fitness evaluation (varianz) for %s/%s failed" % (geneticMain.DIRECTORY,file_name))
            fitness = 1/(delta_energy_mean+variance)
        return fitness

    def mutate(self):
        for i in range(geneticMain.BIT_LENGTH_CHROMOSOME):
            if geneticMain.MUTATE_PROB > np.random.rand():
                self.__genes[i] = not(self.__genes[i])

        self.__fitness = self.eval_fitness()

    def give_fitness(self):
        return self.__fitness
