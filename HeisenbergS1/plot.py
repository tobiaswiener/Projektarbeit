import numpy as np
import matplotlib.pyplot as plt
import time
import json

# import the data from log file
data=json.load(open("RBM.log"))
exact_gs_energy = -45.34782431158947
# Extract the relevant information
iters=[]
energy_RBM=[]

for iteration in data["Output"]:
    iters.append(iteration["Iteration"])
    energy_RBM.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
ax1.plot(iters, energy_RBM, color='red', label='Energy (RBM)')
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters[-1],exact_gs_energy-0.03,exact_gs_energy+0.2])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
ax1.legend()
plt.show()