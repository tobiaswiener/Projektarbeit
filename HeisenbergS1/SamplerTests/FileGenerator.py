import numpy as np
import netket as nk
import build
import json
import itertools
import os


directory = "ersteTests"
try:
    os.mkdir(directory)
except(FileExistsError):
    pass

"""variables to specify"""
_L = [20]
_J = [1]
_numberHiddenLayers = [3]
_factorNeurons = [7]
_actFunc = ["tanh"]



"""Optimizer"""
_optimizer = ["AdaMax","AmsGrad"]
_alpha=[0.001]
_beta1=[0.9]
_beta2=[0.999]
_epscut=[1e-07]

"""Sampler"""
_sampler = ["MetropolisHop"]    #["MetropolisLocal","MetropolisHop"]
_d_max = [1,5,30]


"""VMC"""
_discarded_samples = [-1,200]
_discarded_samples_on_init = [0]
_method = ["Gd"]                #["Gd","Sr"]
_n_samples = [1000]
_diag_shift = [0.01]
_use_iterative = [False]   #[False,True]
_use_cholesky = [False]         #[False,True]
_target = ["energy"]
_n_iter = [1000]







def create():
    """Creates .ip Files out of the specifications above"""
    all_comb = itertools.product(_L, _J, _sampler, _numberHiddenLayers, _factorNeurons, _actFunc,
                                 _optimizer, _alpha, _beta1, _beta2, _epscut, _discarded_samples,
                                 _discarded_samples_on_init, _method, _n_samples, _diag_shift, _use_iterative,
                                 _use_cholesky, _target,_n_iter,_d_max)

    for i in all_comb:

        if (i[2] == "MetropolisLocal"):

            dicc = {
                "input":{
                    "L":i[0], "J":i[1],"machine":{"type":"FFNN", "numberHiddenLayers":i[3], "factorNeurons":i[4], "actFunc":i[5]},
                    "sampler":{"type":i[2]},
                    "optimizer":{"type":i[6], "alpha":i[7], "beta1":i[8], "beta2":i[9], "epscut":i[10]},
                    "VMC": {"n_samples":i[14],"discarded_samples": i[11],"discarded_samples_on_init":i[12],"target": i[18], "method":i[13],
                            "diag_shift": i[15],"use_iterative": i[16],"use_cholesky": i[17]},
                    "n_iter":i[19]}
                     }

        elif(i[2] == "MetropolisHop"):
            dicc = {
                "input": {
                    "L": i[0], "J": i[1],
                    "machine": {"type": "FFNN", "numberHiddenLayers": i[3], "factorNeurons": i[4], "actFunc": i[5]},
                    "sampler": {"type": i[2], "d_max": i[20]},
                    "optimizer": {"type": i[6], "alpha": i[7], "beta1": i[8], "beta2": i[9], "epscut": i[10]},
                    "VMC": {"n_samples": i[14], "discarded_samples": i[11], "discarded_samples_on_init": i[12],
                            "target": i[18], "method": i[13],
                            "diag_shift": i[15], "use_iterative": i[16], "use_cholesky": i[17]},
                    "n_iter": i[19]}
                    }

        n = 1
        filename = directory + "/" + str(dicc["input"]["L"]) + "_" + "FFNN" + "_" + str(dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.ip'

        while (os.path.isfile(filename)):

            n += 1
            filename = directory + "/" + str(i[0]) + "_" + "FFNN" + "_" + i[6] + "_"  + i[2] + str(n) + '.ip'

        with open(filename, 'w') as outfile:
            json.dump(dicc, outfile)

create()