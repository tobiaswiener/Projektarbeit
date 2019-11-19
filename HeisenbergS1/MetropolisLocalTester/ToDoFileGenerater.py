import numpy as np
import netket as nk
import build
import json
import itertools

"""variables to specify"""
_L = [10,12]
_J = [1]
_numberHiddenLayers = [3]
_factorNeurons = [7]
_actFunc = ["tanh"]



"""Optimizer"""
_optimizer = ["AdaMax"]
_alpha=[0.001,0.005]
_beta1=[0.9]
_beta2=[0.999]
_epscut=[1]

"""Sampler"""
_sampler = ["MetropolisLocal"]

"""VMC"""
_discarded_samples = [-1]
_discarded_samples_on_init = [0]
_method = ["Gd"]
_n_samples = [1000,2000]
_diag_shift = [0.01]
_use_iterative = [False]
_use_cholesky = [True]
_target = ["energy"]
_n_iter = [500,100]




class Create:

    @staticmethod
    def create():
        all_comb = itertools.product(_L, _J, _sampler, _numberHiddenLayers, _factorNeurons, _actFunc,
                                     _optimizer, _alpha, _beta1, _beta2, _epscut, _discarded_samples,
                                     _discarded_samples_on_init, _method, _n_samples, _diag_shift, _use_iterative,
                                     _use_cholesky, _target,_n_iter)

        for i i all_comb:
            print(i)

            dicc = {
                "input":{
                    "L":i[0], "J":i[1],"machine":{"type":"FFNN", "numberHiddenLayers":i[3], "factorNeurons":i[4], "actFunc":i[5]},
                    "sampler":{"type":i[2]},
                    "optimizer":{"type":i[6], "alpha":i[7], "beta1":i[8], "beta2":i[9], "epscut":i[10]},
                    "VMC": {"n_samples":i[14],"discarded_samples": i[11],"discarded_samples_on_init":i[12],"target": i[18], "method":i[13],
                            "diag_shift": i[15],"use_iterative": i[16],"use_cholesky": i[17]},
                    "n_iter":i[19]}
                }
            with open(str(j)+'.txt', 'w') as outfile:
                json.dump(dicc, outfile)

            j =+ 1


Create.create()