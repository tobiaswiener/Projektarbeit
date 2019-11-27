import numpy as np
import netket as nk
import build
import json
import itertools
import os


directory = "MPSTests"
try:
    os.mkdir(directory)
except(FileExistsError):
    pass

"""variables to specify"""
_L = [10]
_J = [1]

_seed = [12345]
_model = [
        [10,["tanh","tanh","tanh"]],
        [15,["tanh","tanh","tanh"]],
        [6, ["tanh", "tanh", "tanh"]]
        ]



"""Optimizer"""
_optimizer = ["AdaMax"]
_alpha=[0.001] #0.001
_beta1=[0.9] #0.9
_beta2=[0.999] #0.999
_epscut=[1e-07] #1e-07

"""Sampler"""
_sampler = ["MetropolisHop"]    #["MetropolisLocal","MetropolisHop"]
_d_max = [5]


"""VMC"""
_discarded_samples = [500]
_discarded_samples_on_init = [0]
_method = ["Gd"]                #["Gd","Sr"]
_n_samples = [2000]
_diag_shift = [0.01]
_use_iterative = [False]   #[False,True]
_use_cholesky = [False]         #[False,True]
_target = ["energy"]
_n_iter = [5000]







def create_ip():
    """Creates .ip Files out of the specifications above"""
    all_comb = itertools.product(_L, _J, _sampler, _model,
                                 _optimizer, _alpha, _beta1, _beta2, _epscut, _discarded_samples,
                                 _discarded_samples_on_init, _method, _n_samples, _diag_shift, _use_iterative,
                                 _use_cholesky, _target,_n_iter,_d_max)

    for i in all_comb:

        if (i[2] == "MetropolisLocal"):

            dicc = {
                "input":{
                    "L":i[0], "J":i[1],
                    "machine":{"type":"FFNN", "model": i[3]},
                    "sampler":{"type":i[2]},
                    "optimizer":{"type":i[4], "alpha":i[5], "beta1":i[6], "beta2":i[7], "epscut":i[8]},
                    "VMC": {"n_samples":i[12],"discarded_samples": i[9],"discarded_samples_on_init":i[10],"target": i[16], "method":i[11],
                            "diag_shift": i[13],"use_iterative": i[14],"use_cholesky": i[15]},
                    "n_iter":i[17]}
                     }

        elif(i[2] == "MetropolisHop"):
            dicc = {
                "input": {
                    "L": i[0], "J": i[1],
                    "machine": {"type": "FFNN", "model": i[3]},
                    "sampler": {"type": i[2], "d_max": i[18]},
                    "optimizer": {"type": i[4], "alpha": i[5], "beta1": i[6], "beta2": i[7], "epscut": i[8]},
                    "VMC": {"n_samples": i[12], "discarded_samples": i[9], "discarded_samples_on_init": i[10],
                            "target": i[16], "method": i[11],
                            "diag_shift": i[13], "use_iterative": i[14], "use_cholesky": i[15]},
                    "n_iter": i[17]}
                    }

        n = 1
        filename = directory + "/" + str(dicc["input"]["L"]) + "_" + "FFNN" + "_" + str(dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.ip'
        filenamelog = directory + "/" + str(dicc["input"]["L"]) + "_" + "FFNN" + "_" + str(dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.log'

        while (os.path.isfile(filename) or os.path.isfile(filenamelog)):

            n += 1
            filename = directory + "/" + str(i[0]) + "_" + "FFNN" + "_" + i[4] + "_"  + i[2] + str(n) + '.ip'
            filenamelog = directory + "/" + str(i[0]) + "_" + "FFNN" + "_" + i[4] + "_"  + i[2] + str(n) + '.log'

        with open(filename, 'w') as outfile:
            json.dump(dicc, outfile)



create_ip()


#_model = [
#         [1,["tanh"]],
#         [1,["lncosh"]],
#         [1,["Relu"]],
#         [2,["tanh"]],
#         [2,["lncosh"]],
#         [2,["Relu"]],
#         [3,["tanh"]],
#         [3,["lncosh"]],
#         [3,["Relu"]],
#         [1,["tanh","tanh"]],
#         [1,["lncosh","lncosh"]],
#         [1,["Relu","Relu"]],
#         [2,["tanh","tanh"]],
#         [2,["lncosh","lncosh"]],
#         [2,["Relu""Relu"]],
#         [3,["tanh","tanh"]],
#         [3,["lncosh","lncosh"]],
#         [3,["Relu""Relu"]],
#         [1, ["tanh", "tanh", "tanh"]],
#         [1, ["lncosh", "lncosh", "lncosh"]],
#         [1, ["Relu", "Relu", "Relu"]],
#         [2, ["tanh", "tanh", "tanh"]],
#         [2, ["lncosh", "lncosh", "lncosh"]],
#         [2, ["Relu""Relu", "Relu"]],
#         [3, ["tanh", "tanh", "tanh"]],
#         [3, ["lncosh", "lncosh", "lncosh"]],
#         [3, ["Relu""Relu", "Relu"]],
#         [1, ["tanh", "lncosh"]],
#         [1, ["lncosh", "tanh"]],
#         [1, ["Relu", "tanh"]],
#         [2, ["lncosh", "tanh"]],
#         [2, ["lncosh", "Relu"]],
#         [2, ["Relu","lncosh"]],
#         [3, ["lncosh", "tanh"]],
#         [3, ["lncosh", "Relu"]],
#         [3, ["Relu""tanh"]],
#         [1, ["tanh", "Relu", "tanh"]],
#         [1, ["lncosh", "lncosh", "Relu"]],
#         [1, ["lncosh", "Relu", "Relu"]],
#         [2, ["tanh", "Relu", "lncosh"]],
#         [2, ["Relu", "lncosh", "lncosh"]],
#         [2, ["Relu","Relu", "Relu"]],
#         [3, ["tanh", "lncosh", "tanh"]],
#         [3, ["lncosh", "Relu", "lncosh"]],
#         [3, ["Relu""lncosh", "Relu"]],
#          ]