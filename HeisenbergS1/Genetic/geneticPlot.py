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
import geneticLoad as load
import geneticMain
from typing import List
import configparser

#todo clean up

Y_MIN_From_Exact = -1
Y_MAX_From_Exact = 30
FONT_SIZE = 5


def is_json(myjson: str):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def plot_file(file_name: str, folder:str):
    if nk.MPI.rank() == 0:
        data = []

        with open(folder + "/" + file_name) as f:
            lines = f.readlines()

        try:
            data = json.loads(lines[0])
        except ValueError as err:
            print(err)

        iters = []
        energy = []
        try:
            for it in data["Output"]:
                iters.append(it["Iteration"])
                energy.append(it["Energy"]["Mean"])
        except:
            print(file_name, "failed")
        input = load.specs_runnable.log_to_input(folder=folder, file_name=file_name)
        try:
            L = input["input"]["L"]
        except KeyError:
            print(file_name + " is not yet finished")

        iters = []
        energy = []
        for iteration in data["Output"]:
            iters.append(iteration["Iteration"])
            energy.append(iteration["Energy"]["Mean"])
        plt.rcParams.update({'font.size': FONT_SIZE})

        plt.plot(iters, energy, color='red', label=input["input"]["machine"],linewidth=4)
        plt.axhline(y=geneticMain.EXACT_GS, xmin=0,
                    xmax=iters[-1], linewidth=2, color='k', label='ExactInfinity')
        plt.title(file_name)
        plt.ylabel('Energy')
        plt.xlabel('Iteration')
        plt.axis([0, iters[-1], geneticMain.EXACT_GS+Y_MIN_From_Exact, geneticMain.EXACT_GS+Y_MAX_From_Exact])
        plt.legend()
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
        exact_gs_energy = geneticMain.EXACT_GS
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
        plt.axhline(y=geneticMain.EXACT_GS, xmin=0,
                    xmax=iters[-1], linewidth=2, color='k', label='Exact')
        #plt.plot(iters,np.zeros_like(iters))
        plt.title(name)
        ax1.set_ylabel('Energy')
        ax1.set_xlabel('Iteration')
        ax1.xaxis.set_visible(True)
        plt.axis([0, iters[-1], geneticMain.EXACT_GS+Y_MIN_From_Exact, geneticMain.EXACT_GS+Y_MAX_From_Exact])


    plt.show()


def plot_folder_in_same_plot20(folder: str,label:str = "name"):  #legend=["name","machine","sampler","optimizer","VMC"]

    filename_list = []
    for filename in os.listdir(folder + "/"):
        if filename.endswith(".log"):
            filename_list.append(filename)

    number_plots = len(filename_list)
    all_iters = []
    all_energy = []
    all_names = []
    L = -1
    machine = "machine"
    sampler = "sampler"
    optimizer = "optimizer"
    VMC = "VMC"
    seed = 0
    for counter, name in enumerate(filename_list):
        all_names.append(name)
        data = []
        input = load.specs_runnable.log_to_input(folder=folder,file_name=name)
        try:
            L = input["input"]["L"]
            machine = input["input"]["machine"]
            sampler = input["input"]["sampler"]
            optimizer = input["input"]["optimizer"]
            VMC = input["input"]["VMC"]
        except KeyError:
            print(name + " is not yet finished")

        with open(folder + "/" + name) as f:
            lines = f.readlines()
        for line in lines:
            try:
                b = json.loads(line[0:len(line) - 2])
                data.append(b)
            except ValueError as e:
                pass
        iters = []
        energy = []

        for iteration in data:
            iters.append(iteration["Iteration"])
            energy.append(iteration["Energy"]["Mean"])
        if label == "name":
            plt.plot(iters, energy, label=name)
        elif label == "machine":
            plt.plot(iters, energy, label=machine)
        elif label == "sampler":
            plt.plot(iters, energy, label=sampler)
        elif label == "optimizer":
            plt.plot(iters, energy, label=optimizer)
        elif label == "VMC":
            plt.plot(iters, energy, label=VMC)

        all_iters.append(iters)
        all_energy.append(energy)
        all_names.append(name)
    plt.rcParams.update({'font.size': 8})
    #plt.plot(iters,np.zeros_like(iters))
    plt.title(name)
    plt.ylabel('Energy')
    plt.xlabel('Iteration')
    plt.axis([0, iters[-1], geneticMain.EXACT_GS+Y_MIN_From_Exact, geneticMain.EXACT_GS+Y_MAX_From_Exact])

    plt.legend()
    plt.show()


def plot_folder_in_same_plot(folder: str,label:str = "name"):
    if nk.MPI.rank() == 0:
        filename_list = []
        for filename in os.listdir(folder + "/"):
            if filename.endswith(".log"):
                filename_list.append(filename)
        number_plots = len(filename_list)
        all_iters = []
        all_energy = []
        all_names = []
        L = -1
        machine = "machine"
        sampler = "sampler"
        optimizer = "optimizer"
        VMC = "VMC"
        for counter, name in enumerate(filename_list):
            all_names.append(name)
            data = []
            input = load.specs_runnable.log_to_input(folder=folder,file_name=name)
            try:
                L = input["input"]["L"]
                machine = input["input"]["machine"]
                sampler = input["input"]["sampler"]
                optimizer = input["input"]["optimizer"]
                VMC = input["input"]["VMC"]
            except KeyError:
                if nk.MPI.rank() == 0:
                    print(name + " is not yet finished")
                pass



            with open(folder + "/" + name) as f:
                lines = f.readlines()

            try:
                data = json.loads(lines[0])
            except ValueError as err:
                print(err)

            iters = []
            energy = []
            try:
                for it in data["Output"]:
                    iters.append(it["Iteration"])
                    energy.append(it["Energy"]["Mean"])
            except:
                if nk.MPI.rank() == 0:
                    print("failed to load %s from log file in plot" %(filename))
                pass

            if label == "name":
                plt.plot(iters, energy, label=name)
            elif label == "machine":
                plt.plot(iters, energy, label=machine)
            elif label == "sampler":
                plt.plot(iters, energy, label=sampler)
            elif label == "optimizer":
                plt.plot(iters, energy, label=optimizer)
            elif label == "VMC":
                plt.plot(iters, energy, label=VMC)

            all_iters.append(iters)
            all_energy.append(energy)
            all_names.append(name)
        plt.rcParams.update({'font.size': 8})
        plt.axhline(y=geneticMain.EXACT_GS, xmin=0,
                     xmax=iters[-1], linewidth=2, color='blue', label='ExactLanczos')
        plt.plot(iters,np.zeros_like(iters))
        plt.title(name)
        plt.ylabel('Energy')
        plt.xlabel('Iteration')
        plt.axis([0, iters[-1], geneticMain.EXACT_GS+Y_MIN_From_Exact, geneticMain.EXACT_GS+Y_MAX_From_Exact])

        plt.legend()
        plt.show()

