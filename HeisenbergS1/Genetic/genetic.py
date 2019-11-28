import numpy as np
import netket as nk
from bitstring import BitArray, BitStream, BitString
import math
import os
import json

directory = "test"
try:
    os.mkdir(directory)
except(FileExistsError):
    pass


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



class Chromosome:

    if(_MAX_NEURONS_PER_LAYER % 2 == 0):
        bit_length_per_layer = int(math.log2(_MAX_NEURONS_PER_LAYER))
    else:
        bit_length_per_layer = math.floor(math.log2(_MAX_NEURONS_PER_LAYER)) + 1
    bit_length_chromosome = (bit_length_per_layer) *_MAX_HIDDEN_LAYERS

    def __init__(self, genes:BitArray,generation:int):
        self.genes = genes
        self.generation = generation

    def give_layer(self, counter:int):
        begin = counter * Chromosome.bit_length_per_layer
        end = (counter+1)* Chromosome.bit_length_per_layer
        layer = self.genes[begin:end].uint
        return layer


    def give_config_json(self):
        config = [_ACTIVATION_FUNCTION,[]]
        for i in range(_MAX_HIDDEN_LAYERS):
            config[1].append(self.give_layer(i))
        return config

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