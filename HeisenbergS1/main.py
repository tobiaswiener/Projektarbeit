import netket as nk
import numpy as np
import build
import FFNN
import exactDiag
import RBM
L = 6
J = 1
ED = True
FFNeuralNet = True
RestrictedBM = False
graph, hilbert, hamilton = build.generateNN(length=L,coupling=J)
testing = True

if(testing):
    machine = ["Jastrow","JastrowSymm","FFNN", "RbmSpin", "RmbSpinSymm"]
    sampler = ["ExactSampler"]
    optimizer = ["AdaMax"]
    methode = ["Gd"]
    n_samples = [1000]
    n_iterations = [500]
    nhlayer = [5,6,7]
else:
    machine = ["Jastrow", "JastrowSymm", "FFNN", "RbmSpin", "RmbSpinSymm"]
    sampler = ["ExactSampler", "MetropolisExchange", "MetropolisExchangePt",
               "MetropolisLocal", "MetropolisLocalPt", "MetropolisHamiltonian",
               "MetropolisHamiltonianPt", "MetropolisHop"]
    optimizer = ["Sgd", "RmsProp", "Momentum", "AmsGrad", "AdaMax", "AdaGrad", "AdaDelta"]
    methode = ["Gd", "Sr"]
    n_samples = [1000, 2000]
    n_iterations = [500, 1000]
    nhlayer = [1, 2, 3,]


names = [[] for _ in range(2)]
if(FFNeuralNet):
    for s in sampler:
        for o in optimizer:
            for nhl in nhlayer:
                for n in n_samples:
                    for m in methode:
                        for ni in n_iterations:
                            name, time = FFNN.runFFNN(graph=graph, hilbert=hilbert, hamilton=hamilton, sampler=s,opti=o, nhlayers=nhl, nsamples=n, methode=m, niter=ni)
                            names[0].append(name)
                            names[1].append(time)
if(ED):
    gs_energy_exact = exactDiag.Lanczos(graph=graph, ha=hamilton)
if(RestrictedBM):
    RBM.runRBM(graph,hilbert,hamilton)


