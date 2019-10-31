import netket as nk
import numpy as np
import build
import FFNN
import exactDiag
import RBM
L = 6
J = 2
ED = True
FFNeuralNet = True
RestrictedBM = False
graph, hilbert, hamilton = build.generateNN(length=L,coupling=J)


machine = ["Jastrow","JastrowSymm","FFNN", "RbmSpin", "RmbSpinSymm"]
sampler = ["ExactSampler", "MetropolisExchange","MetropolisExchangePt",
           "MetropolisLocal", "MetropolisLocalPt", "MetropolisHamiltonian",
           "MetropolisHamiltonianPt", "MetropolisHop"]
optimizer = ["Sgd","RmsProp", "Momentum", "AmsGrad", "AdaMax", "AdaGrad", "AdaDelta"]
methode = ["Gd", "Sr"]

n_samples = [1000,2000]
n_iterations = [500,1000]
nhlayer = [1,2,3]
i = 0
names = []
if(FFNeuralNet):
    FFNN.runFFNN(graph,hilbert,hamilton)
if(ED):
    gs_energy_exact = exactDiag.Lanczos(hamilton)
if(RestrictedBM):
    RBM.runRBM(graph,hilbert,hamilton)




