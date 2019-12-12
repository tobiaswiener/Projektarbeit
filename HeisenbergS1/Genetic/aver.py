import os
import numpy as np

directory = "hypertest/L6_256_16"
list_seeds = []
average_list = []
list_seeds_res = []
for counter, filename in enumerate(os.listdir(directory)):
    if filename.endswith(".txt") and filename != "fitnesses.txt":
        with open(directory + "/" +filename) as f:
            content = f.read().splitlines()
            list_seeds.append(content)

for seedss in list_seeds:
    for lines in seedss:
        list_seeds_res.append(lines.strip("[]").split(", "))
average_list = list_seeds_res[0].copy()

for l in average_list:
    l[1] = 0
    l[2] = 0
    l[3] = 0
    l[4] = 0

for counter, seed in enumerate(list_seeds):
    for linecounter, line in enumerate(seed):
        average_list[linecounter][1] += line[1]
        average_list[linecounter][2] += line[2]
        average_list[linecounter][3] += line[3]
        average_list[linecounter][4] += line[4]

