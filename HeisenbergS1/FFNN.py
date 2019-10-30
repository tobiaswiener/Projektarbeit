import netket as nk
import time

def runFFNN(graph, hilbert, hamilton):
    L = graph.n_sites
    layers = (nk.layer.FullyConnected(input_size=L,output_size=int(2*L),use_bias=True),
            nk.layer.Lncosh(input_size=int(2*L)),
            nk.layer.SumOutput(input_size=int(2*L))
            )
    for layer in layers:
        layer.init_random_parameters(seed=12345, sigma=0.01)

    ffnn = nk.machine.FFNN(hilbert, layers)

    sa = nk.sampler.MetropolisExchange(graph=graph, machine=ffnn)

    opt = nk.optimizer.Sgd(learning_rate=0.05)

    gs = nk.variational.Vmc(hamiltonian=hamilton,
                        sampler=sa,
                        optimizer=opt,
                        n_samples=1000,
                        use_iterative=True,
                        method='Sr')

    start = time.time()
    gs.run(output_prefix="blaFF", n_iter=300)
    end = time.time()
    print(end-start)