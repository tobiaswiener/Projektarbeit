# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
import math
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time



def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def plotFromLogFile(filename):
    data=json.load(open(filename))
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
    #plt.axis([0,iters_Jastrow[-1],exact_gs_energy-1,exact_gs_energy+10])
    #plt.axhline(y=exact_gs_energy, xmin=0,
    #             xmax=iters_Jastrow[-1], linewidth=2, color='k', label='Exact')
    plt.axis([0, iters[-1], -130, 70])
    ax1.legend()
    plt.show()


def SubPlotFromFile(filenameList, folder=""):

    N = len(filenameList)

    for counter, name in enumerate(filenameList):
        data = []
        with open(folder + name) as f:
            print(folder + name)
            a = f.readlines()
        for line in a:
            try:
                b = json.loads(line[0:len(line)-2])
                data.append(b)
            except ValueError as e:
                pass




        w = math.floor(math.sqrt(N + 1)) + 1
        d = math.floor(math.sqrt(N + 1)) + 1

        iters = []
        energy = []
        for iteration in data:
            iters.append(iteration["Iteration"])
            energy.append(iteration["Energy"]["Mean"])
        plt.rcParams.update({'font.size': 5})
        ax1 = plt.subplot(w, d, counter + 1)

        plt.plot(iters, energy, color='C8', label=name)
        plt.title(name)
        ax1.set_ylabel('Energy')
        ax1.set_xlabel('Iteration')
        ax1.xaxis.set_visible(True)
        print(iters)
        plt.axis([0, iters[-1], -130, 70])
        #plt.axis([0, iters[-1], exact_gs_energy - 1, exact_gs_energy + 50])
        #plt.axhline(y=exact_gs_energy, xmin=0,
        #            xmax=iters[-1], linewidth=2, color='k', label='Exact')


    plt.show()

