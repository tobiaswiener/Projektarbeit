import json
import numpy as np
import build
import netket as nk
import time
import os

class specs_runnable:

    def __init__(self,file_name:str, folder:str):


        self.input_dict = specs_runnable.file_to_dict(file_name, folder)


        self.file_name = file_name
        self.folder = folder




        input = self.input_dict["input"]
        """variables to specify"""
        self._L = input["L"]
        self._J = input["J"]

        """Network"""
        self._numberHiddenLayers = input["machine"]["numberHiddenLayers"]
        self._factorNeurons = input["machine"]["factorNeurons"]
        self._actFunk = input["machine"]["actFunc"]


        """Sampler"""
        self._sampler = input["sampler"]["type"]
        if(self._sampler == "MetropolisLocal"):
            pass
        elif(self._sampler == "MetropolisHop"):
            self._d_max = input["sampler"]["d_max"]



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




    def run_spec(self):
        graph, hilbert, hamilton = build.generateNN(length=self._L, coupling=self._J)

        layers = []
        layers.append(
            nk.layer.FullyConnected(input_size=self._L, output_size=int(self._factorNeurons * self._L), use_bias=True))
        for i in range(self._numberHiddenLayers):
            layers.append(nk.layer.Tanh(input_size=int(self._factorNeurons * self._L)))
        layers.append(nk.layer.SumOutput(input_size=int(self._factorNeurons * self._L)))
        layers = tuple(layers)  # layers must be tuple

        for layer in layers:
            layer.init_random_parameters(seed=12345, sigma=0.01)
        ma = nk.machine.FFNN(hilbert, layers)

        if (self._sampler == "MetropolisLocal"):
            sa = nk.sampler.MetropolisLocal(machine=ma)
        elif (self._sampler == "MetropolisHop"):
            sa = nk.sampler.MetropolisHop(machine=ma, d_max=self._d_max)

        if (self._optimizer == "AdaMax"):
            opt = nk.optimizer.AdaMax(alpha=self._alpha, beta1=self._beta1, beta2=self._beta2, epscut=self._epscut)
        elif (self._optimizer == "AmsGrad"):
            opt = nk.optimizer.AmsGrad(learning_rate=self._alpha, beta1=self._beta1, beta2=self._beta2,
                                       epscut=self._epscut)

        gs = nk.variational.Vmc(hamiltonian=hamilton,
                                sampler=sa,
                                optimizer=opt,
                                n_samples=self._n_samples,
                                use_iterative=self._use_iterative,
                                use_cholesky=self._use_cholesky,
                                method=self._method,
                                diag_shift=self._diag_shift,
                                discarded_samples=self._discarded_samples,
                                discarded_samples_on_init=self._discarded_samples_on_init,
                                target=self._target)

        start_time = time.time()
        gs.run(output_prefix=self.folder + "/" + self.file_name[:-3], n_iter=self._n_iter)
        end_time = time.time()

        if (nk._C_netket.MPI.rank() == 0):
            with open(self.folder + "/" + self.file_name[:-3] + ".log", "a") as f:
                f.write("\n")
                json.dump(self.input_dict, f)
                f.write("\nduration: " + str(start_time - end_time))

            try:
                os.remove(self.folder + "/" + self.file_name)
            except FileNotFoundError as err:
                print(err.filename)

    @staticmethod
    def file_to_dict(file_name: str, folder: str) -> dict:
        with open(folder + "/" + file_name) as f:
            input_dict = json.load(f)
        return input_dict


    @staticmethod
    def run_all_files(folder: str):
        for file_name in os.listdir(folder):
            if file_name.endswith(".ip"):
                todo = specs_runnable(file_name,folder)
                todo.run_spec()
            else:
                continue

    @staticmethod
    def run_file(folder: str, file_name: str):
        specs_runnable(file_name,folder).run_spec()

    @staticmethod
    def log_to_input(folder: str, file_name: str) -> dict:

        with open(folder + "/" + file_name) as f:
            lines = []
            for line in f:
                lines.append(line)
                pass
        return json.loads(lines[-2])
