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


"""MPS"""
_BondDim = [5,7,9]
_SymmetryPeriod = [1]
_SigmaRand= [0.01]
_Diagonal= [False]



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
_n_iter = [100]


def create_ip():
    """Creates .ip Files out of the specifications above"""
    all_comb = itertools.product(_L, _J, _sampler, _BondDim,_SymmetryPeriod,_SigmaRand,_Diagonal,
                                 _optimizer, _alpha, _beta1, _beta2, _epscut, _discarded_samples,
                                 _discarded_samples_on_init, _method, _n_samples, _diag_shift, _use_iterative,
                                 _use_cholesky, _target,_n_iter,_d_max)

    for i in all_comb:

        if (i[2] == "MetropolisLocal"):

            dicc = {
                "input":{
                    "L":i[0], "J":i[1],
                    "machine":{"type":"MPS", "BondDim": i[3], "SymmetryPeriod":i[4], "SigmaRand":i[5],"Diagonal":i[6]},
                    "sampler":{"type":i[2]},
                    "optimizer":{"type":i[7], "alpha":i[8], "beta1":i[9], "beta2":i[10], "epscut":i[11]},
                    "VMC": {"n_samples":i[15],"discarded_samples": i[12],"discarded_samples_on_init":i[13],"target": i[19], "method":i[14],
                            "diag_shift": i[16],"use_iterative": i[17],"use_cholesky": i[18]},
                    "n_iter":i[20]}
                     }

        elif(i[2] == "MetropolisHop"):
            dicc = {
                "input":{
                    "L":i[0], "J":i[1],
                    "machine":{"type":"MPS", "BondDim": i[3], "SymmetryPeriod":i[4], "SigmaRand":i[5],"Diagonal":i[6]},
                    "sampler":{"type":i[2],"d_max":i[21]},
                    "optimizer":{"type":i[7], "alpha":i[8], "beta1":i[9], "beta2":i[10], "epscut":i[11]},
                    "VMC": {"n_samples":i[15],"discarded_samples": i[12],"discarded_samples_on_init":i[13],"target": i[19], "method":i[14],
                            "diag_shift": i[16],"use_iterative": i[17],"use_cholesky": i[18]},
                    "n_iter":i[20]}
                     }

        n = 1
        filename = directory + "/" + str(dicc["input"]["L"]) + "_" + "MPS" + "_" + str(dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.ip'
        filenamelog = directory + "/" + str(dicc["input"]["L"]) + "_" + "MPS" + "_" + str(dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.log'

        while (os.path.isfile(filename) or os.path.isfile(filenamelog)):

            n += 1
            filename = directory + "/" + str(dicc["input"]["L"]) + "_" + "MPS" + "_" + str(
                dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.ip'
            filenamelog = directory + "/" + str(dicc["input"]["L"]) + "_" + "MPS" + "_" + str(
                dicc["input"]["optimizer"]["type"]) + "_" + str(dicc["input"]["sampler"]["type"]) + str(n) + '.log'

        with open(filename, 'w') as outfile:
            json.dump(dicc, outfile)

create_ip()