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
folder = "5/"

if(testing):
    machine = ["Jastrow","JastrowSymm","FFNN", "RbmSpin", "RmbSpinSymm"]
    sampler = ["MetropolisHop","MetropolisLocal"]
    optimizer = ["AdaMax"]
    methode = ["Gd"]
    #n_samples = [1000]
    f_samples = [100,150,200]
    n_iterations = [1000]
    nhlayer = [3]
    fneuron =[7]
    L = [26,30,40,50,60,70,80,90,100]
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

N=len(sampler)*len(optimizer)*len(nhlayer)*len(fneuron)*len(f_samples)*len(methode)*len(n_iterations)
filenameList = []
for l in L:
    for s in sampler:
        for o in optimizer:
            for nhl in nhlayer:
                for fn in fneuron:
                    for f in f_samples:
                        for m in methode:
                            for ni in n_iterations:
                                filename = str(0) + str(l) + "_" + str(fn) + "FFNN" + str(nhl) + "_" + s \
                                          + str(f*l) + "_" + str(o) + "_" + str(ni) + "_" + m +".log"
                                if(os.path.isfile(folder + filename)):
                                    filenameList.append(filename)

plot.SubPlotFromFile(filenameList, folder)

