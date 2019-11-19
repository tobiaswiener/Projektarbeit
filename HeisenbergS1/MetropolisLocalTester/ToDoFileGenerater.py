import numpy as np
import netket as nk
import build

"""variables to specify"""
_L = 10
_J = 1
_sampler = "MetropolisExchange"
_numberHiddenLayers = 3
_factorNeurons = 7
_actFunc = "tanh"



"""Optimizer"""
_optimizer = "AdaMax"
_alpha=0.001
_beta1=0.9
_beta2=0.999
_epscut=1

"""Sampler"""
_sampler = "MetropolisLocal"



"""VMC"""
_discarded_samples = -1
_discarded_samples_on_init = 0
_method = "Gd"
_n_samples = 1000
_diag_shift = 0.01
_use_iterative = False
_use_cholesky = True
_target = "energy"


