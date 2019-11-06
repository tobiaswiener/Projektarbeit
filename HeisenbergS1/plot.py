# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
import math
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time

def plotFromLogFile(filename):
    data=json.load(open("1stResults/"+filename))
    exact_gs_energy = -34.46969272725688

# Extract the relevant information
    iters_Jastrow=[]
    energy_Jastrow=[]

    for iteration in data["Output"]:
        iters_Jastrow.append(iteration["Iteration"])
        energy_Jastrow.append(iteration["Energy"]["Mean"])

    fig, ax1 = plt.subplots()
    ax1.plot(iters_Jastrow, energy_Jastrow, color='C8', label=filename)
    ax1.set_ylabel('Energy')
    ax1.set_xlabel('Iteration')
    plt.axis([0,iters_Jastrow[-1],exact_gs_energy-1,exact_gs_energy+10])
    plt.axhline(y=exact_gs_energy, xmin=0,
                 xmax=iters_Jastrow[-1], linewidth=2, color='k', label='Exact')
    ax1.legend()
    plt.show()


def SubPlotFromFile(filename, N, i):
    data = json.load(open("1stResults/" + filename))
    exact_gs_energy = -34.46969272725688
    w = math.floor(math.sqrt(N+1))+1
    d = math.floor(math.sqrt(N+1))+1


    iters = []
    energy = []
    for iteration in data["Output"]:
        iters.append(iteration["Iteration"])
        energy.append(iteration["Energy"]["Mean"])
    plt.rcParams.update({'font.size': 4})
    ax1 = plt.subplot(w,d,i+1)

    plt.plot(iters, energy,  color='C8', label=filename)
    plt.title(filename)
    ax1.set_ylabel('Energy')
    ax1.set_xlabel('Iteration')
    ax1.xaxis.set_visible(False)
    plt.axis([0,iters[-1],exact_gs_energy-1,exact_gs_energy+20])
    plt.axhline(y=exact_gs_energy, xmin=0,
                 xmax=iters[-1], linewidth=2, color='k', label='Exact')

    if(i+1==N):
        plt.show()

