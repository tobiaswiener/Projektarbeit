import netket as nk
import time

def runFFNN(graph, hilbert, hamilton):
    L = graph.n_sites
    layers = (nk.layer.FullyConnected(input_size=L,output_size=int(2*L),use_bias=True),
            nk.layer.Tanh(input_size=int(2*L)),
            nk.layer.SumOutput(input_size=int(2*L))
            )
    for layer in layers:
        layer.init_random_parameters(seed=12345, sigma=0.01)

    ffnn = nk.machine.FFNN(hilbert, layers)

    sa = nk.sampler.MetropolisExchange(graph=graph, machine=ffnn)

    #different Sampler
    if(sampler == "ExactSampler"):
        sa = nk.sampler.ExactSampler(machine=ma)
    elif(sampler == "MetropolisExchange"):
        sa = nk.sampler.MetropolisExchange(graph=graph, machine=ma)
    elif (sampler == "MetropolisExchangePt"):
        sa = nk.sampler.MetropolisExchangePt(graph=graph, machine=ma, n_replicas=10)
    elif (sampler == "MetropolisLocal"):
        sa = nk.sampler.MetropolisLocal(machine=ma)
    elif (sampler == "MetropolisLocalPt"):
        sa = nk.sampler.MetropolisLocalPt(machine=ma,n_replicas=10)
    elif (sampler == "MetropolisHamiltonian"):
        sa = nk.sampler.MetropolisHamiltonian(machine=ma, hamiltonian=hamilton)
    elif (sampler == "MetropolisHamiltonianPt"):
        sa = nk.sampler.MetropolisHamiltonianPt(machine=ma, hamiltonian=hamilton, n_replicas=10)
    elif (sampler == "MetropolisHop"):
        sa = nk.sampler.MetropolisHop(machine=ma)

    #different optimizer
    if(opti == "Sgd"):
        opt = nk.optimizer.Sgd(learning_rate=0.05)
    elif(opti == "RmsProp"):
        opt = nk.optimizer.RmsProp(learning_rate=0.001,beta=0.9,epscut=1)
    elif (opti == "Momentum"):
        opt = nk.optimizer.Momentum(learning_rate=0.001,beta=0.9)
    elif (opti == "AmsGrad"):
        opt = nk.optimizer.AmsGrad(learning_rate=0.001,beta1=0.9,beta2=0.999,epscut=1)
    elif (opti == "AdaMax"):
        opt = nk.optimizer.AdaMax(alpha=0.001,beta1=0.9,beta2=0.999,epscut=1)
    elif (opti == "AdaGrad"):
        opt = nk.optimizer.AdaGrad(learning_rate=0.001,epscut=1)
    elif (opti == "AdaDelta"):
        opt = nk.optimizer.AdaDelta(rho=0.95,epscut=1)


    gs = nk.variational.Vmc(hamiltonian=hamilton,
                        sampler=sa,
                        optimizer=opt,
                        n_samples=1000,
                        use_iterative=True,
                        method='Sr')

    start = time.time()
    gs.run(output_prefix="FF", n_iter=300)

    end = time.time()
    print(end-start)