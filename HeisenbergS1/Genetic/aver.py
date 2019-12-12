import os
import numpy as np
import copy

directory = "hypertest/L6_256_16"
list_seeds = []
average_list = []
list_seeds_res = []
for counter, filename in enumerate(os.listdir(directory)):
    if filename.endswith(".txt") and filename != "fitnesses.txt":
        with open(directory + "/" +filename) as f:
            content = f.read().splitlines()
            list_seeds.append(content)

for seedsscounter, seedss in enumerate(list_seeds):
    oneseedlist = []
    for lines in seedss:
        oneseedlist.append(lines.strip("[]").split(", "))
    list_seeds_res.append(oneseedlist)

average_list = copy.deepcopy(list_seeds_res[0])

for l in average_list:
    l[1] = 0.
    l[2] = 0.
    l[3] = 0.




for counter, seed in enumerate(list_seeds_res):
    for linecounter, line in enumerate(seed):
        average_list[linecounter][1] += float(line[1])
        average_list[linecounter][2] += float(line[2])
        average_list[linecounter][3] += float(line[3])

nseeds = len(list_seeds_res)
for nline in average_list:
    nline[1] /= nseeds
    nline[2] /= nseeds
    nline[3] /= nseeds




sorted_by_steps = sorted(average_list, key=lambda tup: tup[1], reverse=True)
sorted_by_fitness = sorted(average_list, key=lambda tup: tup[2], reverse=True)
sorted_by_calcnetworks = sorted(average_list, key=lambda tup: tup[3], reverse=True)


file_steps = directory + "/sorted_by_steps.txt"
file_fitness = directory + "/sorted_by_fitness.txt"
file_calcnetworks = directory + "/sorted_by_calcnetworks.txt"
with open(file_steps, 'w') as f:
    for item in sorted_by_steps:
        f.write("%s\n" % item)

with open(file_fitness, 'w') as f:
    for item in sorted_by_fitness:
        f.write("%s\n" % item)

with open(file_calcnetworks, 'w') as f:
    for item in sorted_by_calcnetworks:
        f.write("%s\n" % item)
