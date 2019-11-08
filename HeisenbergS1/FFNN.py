import netket as nk
import time

def runFFNN(graph, hilbert, hamilton, sampler,opti,nhlayers, fneurons, nsamples, methode, niter):
    L = graph.n_sites
    filename = str(0) + str(L) + "_" + str(fneurons)+ "FFNN" + str(nhlayers) + "_" + sampler \
               + str(nsamples)  + "_"+ opti + "_" +  str(niter) + "_"+   methode




    #defining layers with var number hidden layers
    layers = []
    layers.append(nk.layer.FullyConnected(input_size=L,output_size=int(fneurons*L),use_bias=True))
    for i in range(nhlayers):
        layers.append(nk.layer.Tanh(input_size=int(fneurons*L)))
    layers.append(nk.layer.SumOutput(input_size=int(fneurons*L)))
    layers = tuple(layers) #layers must be tuple

    for layer in layers:
        layer.init_random_parameters(seed=12345, sigma=0.01)

    ma = nk.machine.FFNN(hilbert, layers)


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



    if (methode == "Sr"):
        gs = nk.variational.Vmc(hamiltonian=hamilton,
                                sampler=sa,
                                optimizer=opt,
                                n_samples=nsamples,
                                use_iterative=True,
                                method='Sr')
    elif (methode == "Gd"):
        gs = nk.variational.Vmc(hamiltonian=hamilton,
                                sampler=sa,
                                optimizer=opt,
                                n_samples=nsamples,
                                use_iterative=False,
                                method='Gd')



    start = time.time()
    gs.run(output_prefix=filename, n_iter=niter)
    end = time.time()
    print("time: ", end-start)
    return filename, end-start