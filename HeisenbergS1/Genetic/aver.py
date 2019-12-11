import os
import numpy as np

directory = "hypertest/L6_256_16"
list_seeds = []

for counter, filename in enumerate(os.listdir(directory)):
    if filename.endswith(".txt") and filename != "fitnesses.txt":
        lineList = np.load(directory +"/"+filename)
        list_seeds.append(lineList)
        continue
    else:
        continue