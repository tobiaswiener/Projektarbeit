# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time
import plot
import os.path



testing = True
folder = ""

if(testing):
    sampler = ["ExactSampler",
               "MetropolisLocal", "MetropolisHop"]
    optimizer = ["AdaMax"]
    methode = ["Gd"]
    n_samples = [200,500,1000]
    n_iterations = [1000,5000,7000,11000]
    nhlayer = [3]
    fneuron =[7]
    L = [6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
else: #all that were done
    sampler = ["ExactSampler", "MetropolisExchange", "MetropolisExchangePt",
               "MetropolisLocal", "MetropolisLocalPt", "MetropolisHamiltonian",
               "MetropolisHamiltonianPt", "MetropolisHop"]
    optimizer = ["AdaMax","Sgd", "RmsProp"]
    methode = ["Gd","Sr"]
    n_samples = [200,500,1000]
    n_iterations = [7000]
    nhlayer = [3,5]
    fneuron =[3,5,7]

N=len(sampler)*len(optimizer)*len(nhlayer)*len(fneuron)*len(n_samples)*len(methode)*len(n_iterations)
i = 0
filenameList = []
for l in L:
    for s in sampler:
        for o in optimizer:
            for nhl in nhlayer:
                for fn in fneuron:
                    for n in n_samples:
                        for m in methode:
                            for ni in n_iterations:
                                filename = str(0) + str(l) + "_" + str(fn) + "FFNN" + str(nhl) + "_" + s \
                                          + str(n) + "_" + str(o) + "_" + str(ni) + "_" + m +".log"

                                if(os.path.isfile(folder + filename)):
                                    filenameList.append(filename)

plot.SubPlotFromFile(filenameList, folder)

