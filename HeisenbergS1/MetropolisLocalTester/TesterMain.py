import numpy as np
import netket as nk
import build
import loader

filename = "templateAdaMax.ip"

todo = loader.spec_Variables(loader.spec_Variables.load_from_File(filename))



def run_it(todo):
    """build Graph, Hilbert Space and Hamiltonian"""

    graph, hilbert, hamilton = build.generateNN(length=todo._L, coupling=todo._J)

    """defining layers with var number hidden layers"""

    layers = []
    layers.append(nk.layer.FullyConnected(input_size=todo._L, output_size=int(todo._factorNeurons * todo._L), use_bias=True))
    for i in range(todo._numberHiddenLayers):
        layers.append(nk.layer.Tanh(input_size=int(todo._factorNeurons * todo._L)))
    layers.append(nk.layer.SumOutput(input_size=int(todo._factorNeurons * todo._L)))
    layers = tuple(layers)  # layers must be tuple

    for layer in layers:
        layer.init_random_parameters(seed=12345, sigma=0.01)
    ma = nk.machine.FFNN(hilbert, layers)

    """Sampler Metropolis Local"""
    sa = nk.sampler.MetropolisLocal(machine=ma)

    """Optimizer AdaMax"""
    opt = nk.optimizer.AdaMax(alpha=todo._alpha,beta1=todo._beta1,beta2=todo._beta2,epscut=todo._epscut)

    """VMC"""
    gs = nk.variational.Vmc(hamiltonian=hamilton,
                                    sampler=sa,
                                    optimizer=opt,
                                    n_samples=todo._n_samples,
                                    use_iterative=todo._use_iterative,
                                    use_cholesky=todo._use_cholesky,
                                    method=todo._method,
                                    diag_shift=todo._diag_shift,
                                    discarded_samples=todo._discarded_samples,
                                    discarded_samples_on_init=todo._discarded_samples_on_init,
                                    target=todo._target)

    gs.run(output_prefix=filename, n_iter=todo._n_iter)

run_it(todo=todo)