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
import SamplerTests.load as load
from typing import List




Y_MIN = -130
Y_MAX = 70
FONT_SIZE = 5
EXACT_ENERGY_PER_SITE_L_INFINTY =  -1.401484038970


def is_json(myjson: str):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def plot_file(file_name: str, folder:str):
    data = []
    with open(folder + "/" + file_name) as f:
        line = f.readlines()
    for line in line:
        try:
            b = json.loads(line[0:len(line) - 2])
            data.append(b)
        except ValueError as e:
            pass

    input = load.specs_runnable.log_to_input(folder=folder, file_name=file_name)
    try:
        L = input["input"]["L"]
    except KeyError:
        print(file_name + " is not yet finished")
    exact_gs_energy = EXACT_ENERGY_PER_SITE_L_INFINTY * L
    iters = []
    energy = []
    for iteration in data:
        iters.append(iteration["Iteration"])
        energy.append(iteration["Energy"]["Mean"])
    plt.rcParams.update({'font.size': FONT_SIZE})

    plt.plot(iters, energy, color='C8', label=file_name)
    plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
    plt.title(file_name)
    plt.ylabel('Energy')
    plt.xlabel('Iteration')
    plt.axis([0, iters[-1], Y_MIN, Y_MAX])
    plt.show()



def plot_all_log_file_from_folder(folder: str):
    filename_list = []
    for filename in os.listdir(folder + "/"):
        if filename.endswith(".log"):
            filename_list.append(filename)

    number_plots = len(filename_list)

    for counter, name in enumerate(filename_list):
        data = []
        input = load.specs_runnable.log_to_input(folder=folder,file_name=name)
        try:
            L = input["input"]["L"]
        except KeyError:
            print(name + " is not yet finished")
        exact_gs_energy = EXACT_ENERGY_PER_SITE_L_INFINTY*L
        with open(folder + "/" + name) as f:
            line = f.readlines()
        for line in line:
            try:
                b = json.loads(line[0:len(line) - 2])
                data.append(b)
            except ValueError as e:
                pass
        num_plots_horizontal = math.floor(math.sqrt(number_plots + 1)) + 1
        num_plots_vertical = math.floor(math.sqrt(number_plots + 1)) + 1

        iters = []
        energy = []
        for iteration in data:
            iters.append(iteration["Iteration"])
            energy.append(iteration["Energy"]["Mean"])
        plt.rcParams.update({'font.size': 5})
        ax1 = plt.subplot(num_plots_horizontal, num_plots_vertical, counter + 1)
        plt.plot(iters, energy, color='C8', label=name)
        plt.axhline(y=exact_gs_energy, xmin=0,
                    xmax=iters[-1], linewidth=2, color='k', label='Exact')
        #plt.plot(iters,np.zeros_like(iters))
        plt.title(name)
        ax1.set_ylabel('Energy')
        ax1.set_xlabel('Iteration')
        ax1.xaxis.set_visible(True)
        plt.axis([0, iters[-1], Y_MIN, Y_MAX])


    plt.show()