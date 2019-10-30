import netket as nk
import numpy as np
import build
import FFNN
import exactDiag
L = 6
J = 2
ED = True
FFNeuralNet = True

graph, hilbert, hamilton = build.generateNN(length=L,coupling=J)

if(FFNeuralNet):
    FFNN.runFFNN(graph,hilbert,hamilton)
if(ED):
    gs_energy_exact = exactDiag.Lanczos(hamilton)




