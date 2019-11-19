import json
import numpy as np





class spec_Variables():
    def __init__(self,input):
        """variables to specify"""
        self._L = input["L"]
        self._J = input["J"]

        """Network"""
        self._numberHiddenLayers = input["machine"]["numberHiddenLayers"]
        self._factorNeurons = input["machine"]["factorNeurons"]
        self._actFunk = input["machine"]["actFunc"]


        """Sampler"""
        self._sampler = input["sampler"]["type"]



        """Optimizer"""
        self._optimizer = input["optimizer"]["type"]
        self._alpha = input["optimizer"]["alpha"]
        self._beta1= input["optimizer"]["beta1"]
        self._beta2= input["optimizer"]["beta2"]
        self._epscut= input["optimizer"]["epscut"]



        """VMC"""
        self._discarded_samples = input["VMC"]["discarded_samples"]
        self._discarded_samples_on_init = input["VMC"]["discarded_samples_on_init"]
        self._target = input["VMC"]["target"]
        self._method = input["VMC"]["method"]
        self._n_samples =  input["VMC"]["n_samples"]
        self._diag_shift =  input["VMC"]["diag_shift"]
        self._use_iterative =  input["VMC"]["use_iterative"]
        self._use_cholesky =  input["VMC"]["use_cholesky"]

        self._n_iter =  input["n_iter"]

    @staticmethod
    def load_from_File(file):
        with open (file) as f:
            data = json.load(f)
        return data




