import netket as nk
import numpy as np
import csv
import build
import FFNN
import exactDiag
import RBM
L = 22
J = 1
ED = False
FFNeuralNet = True
RestrictedBM = False
graph, hilbert, hamilton = build.generateNN(length=L,coupling=J)
testing = True

if(testing):
    machine = ["Jastrow","JastrowSymm","FFNN", "RbmSpin", "RmbSpinSymm"]
    sampler = ["MetropolisLocal"]
    optimizer = ["AdaMax"]
    methode = ["Gd"]
    n_samples = [1000]
    n_iterations = [5000]
    nhlayer = [3]
    fneuron =[7]
else:
    machine = ["Jastrow", "JastrowSymm", "FFNN", "RbmSpin", "RmbSpinSymm"]
    sampler = ["ExactSampler", "MetropolisExchange", "MetropolisExchangePt",
               "MetropolisLocal", "MetropolisLocalPt", "MetropolisHamiltonian",
               "MetropolisHamiltonianPt", "MetropolisHop"]
    optimizer = ["Sgd", "RmsProp", "Momentum", "AmsGrad", "AdaMax", "AdaGrad", "AdaDelta"]
    methode = ["Gd", "Sr"]
    n_samples = [1000, 2000]
    n_iterations = [500, 1000]
    nhlayer = [1, 2]
    fneuron = [3]

names = [[] for _ in range(2)]
if(FFNeuralNet):
    for s in sampler:
        for o in optimizer:
            for nhl in nhlayer:
                for fn in fneuron:
                    for n in n_samples:
                        for m in methode:
                            for ni in n_iterations:
                                name, time = FFNN.runFFNN(graph=graph, hilbert=hilbert, hamilton=hamilton, sampler=s,opti=o, nhlayers=nhl, fneurons= fn , nsamples=n, methode=m, niter=ni)
                                names[0].append(name)
                                names[1].append(time)

if(ED):
    gs_energy_exact = exactDiag.Lanczos(graph=graph, ha=hamilton)
if(RestrictedBM):
    RBM.runRBM(graph,hilbert,hamilton)

with open("times.csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(names)
