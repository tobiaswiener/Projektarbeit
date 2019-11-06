import netket as nk
import time

def runRBM(graph, hilbert, hamilton):
    RBM = nk.machine.RbmSpin(alpha=1, hilbert=hilbert)

    # Sampler
    sa = nk.sampler.MetropolisExchange(machine=RBM, graph=graph)
    RBM.init_random_parameters(seed=123, sigma=0.01)

    # Optimizer
    opti = nk.optimizer.Sgd(learning_rate=0.05)
    # Stochastic reconfiguration
    gs = nk.variational.Vmc(
        hamiltonian=hamilton,
        sampler=sa,
        optimizer=opti,
        n_samples=1000,
        diag_shift=0.1,
        use_iterative=True,
        method='Sr')

    start = time.time()
    gs.run(output_prefix='RBM', n_iter=600)
    end = time.time()
    print(end - start)