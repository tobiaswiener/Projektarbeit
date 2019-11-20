# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
import math
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from typing import List



def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def SubPlotFromFile(filenameList: List[str], folder: str):
    """plots"""

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
        plt.axis([0, iters[-1], -130, 70])
        #plt.axis([0, iters[-1], exact_gs_energy - 1, exact_gs_energy + 50])
        #plt.axhline(y=exact_gs_energy, xmin=0,
        #            xmax=iters[-1], linewidth=2, color='k', label='Exact')


    plt.show()

def plot_Folder(folder: str):
    """Plots all .log Files from a Folder in different subplots"""
    filenameList = []
    for filename in os.listdir(folder+"/"):
        if filename.endswith(".log"):
            filenameList.append(filename)
    SubPlotFromFile(filenameList, folder+"/")